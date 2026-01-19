#!/usr/bin/env python3
# (C) 2026 GoodData Corporation
"""
GDC-NAS REST API Diff Analyzer

A deterministic program that analyzes git diffs in the gdc-nas repository
and categorizes changes by REST API component type. Designed to identify
changes that require updates to gooddata-python-sdk.

================================================================================
USAGE EXAMPLES
================================================================================

1. SINGLE COMMIT ANALYSIS
   ----------------------
   # Analyze a single commit (compares to its parent)
   python gdc-nas-diff-analyzer.py abc123 --repo-path ./gdc-nas

   # Analyze a specific commit range (shows which commit modified each file)
   python gdc-nas-diff-analyzer.py abc123..def456 --repo-path ./gdc-nas

   # Analyze last 50 commits
   python gdc-nas-diff-analyzer.py HEAD~50..HEAD --repo-path ./gdc-nas

2. INCREMENTAL ANALYSIS (--since)
   ------------------------------
   # Step 1: List commits since last analyzed commit (dry run)
   python gdc-nas-diff-analyzer.py --since abc123 --list-commits --repo-path ./gdc-nas

   # Step 2a: Analyze all new commits as combined diff
   python gdc-nas-diff-analyzer.py --since abc123 --repo-path ./gdc-nas

   # Step 2b: OR analyze each commit individually (shows SDK impact per commit)
   python gdc-nas-diff-analyzer.py --since abc123 --per-commit --repo-path ./gdc-nas

3. SDK-DETAILS MODE (RECOMMENDED FOR SDK SYNC)
   --------------------------------------------
   # Scan commits, find SDK-relevant ones, output full details for each
   python gdc-nas-diff-analyzer.py --since abc123 --sdk-details --repo-path ./gdc-nas

   # Save each SDK-relevant commit report to a separate file
   python gdc-nas-diff-analyzer.py --since abc123 --sdk-details --output-dir ./reports --repo-path ./gdc-nas

   # This creates:
   #   ./reports/00-summary.md        - Overview with latest commit hash
   #   ./reports/01-cf1832f1.md       - Full report for first SDK commit
   #   ./reports/02-dff345f1.md       - Full report for second SDK commit
   #   ...

4. SAVE OUTPUT TO FILE
   --------------------
   python gdc-nas-diff-analyzer.py abc123 --repo-path ./gdc-nas -o report.md

5. FILTER TO SDK-RELEVANT ONLY (--sdk-only)
   -----------------------------------------
   # Only output if there are SDK-relevant changes (skips chore/docs commits)
   python gdc-nas-diff-analyzer.py abc123 --sdk-only --repo-path ./gdc-nas

   # Analyze many commits, only show SDK-relevant ones
   python gdc-nas-diff-analyzer.py --since abc123 --per-commit --sdk-only --repo-path ./gdc-nas

6. COMMIT ATTRIBUTION
   -------------------
   # By default, ranges show which commit(s) modified each file
   python gdc-nas-diff-analyzer.py HEAD~50..HEAD --repo-path ./gdc-nas
   # Output: - 📝 `SomeFile.kt` (+10/-5) [abc123]
   #         - 📝 `OtherFile.kt` (+20/-3) [2 commits]
   #           - `abc123` feat: first change
   #           - `def456` fix: second change

   # Disable commit attribution for cleaner output
   python gdc-nas-diff-analyzer.py HEAD~50..HEAD --no-commits --repo-path ./gdc-nas

================================================================================
WORKFLOW FOR TRACKING SDK CHANGES
================================================================================

1. Run --sdk-details with --output-dir to analyze and save reports
2. Note the "Latest commit analyzed" hash from 00-summary.md
3. Save this hash for next run
4. Next time, use: --since <saved_hash> --sdk-details --output-dir ./new-reports

Example workflow:
   # First run - analyze recent changes and save reports
   python gdc-nas-diff-analyzer.py --since HEAD~100 --sdk-details --output-dir ./sdk-reports --repo-path ./gdc-nas
   # Check 00-summary.md for "Latest commit analyzed: abc123"

   # Later - analyze new commits since abc123
   python gdc-nas-diff-analyzer.py --since abc123 --sdk-details --output-dir ./sdk-reports-new --repo-path ./gdc-nas

================================================================================
OUTPUT SECTIONS
================================================================================

- **Summary**: Total files, lines changed, services impacted
- **Commits Included**: List of commits in the analysis (with --since)
- **Changes by Category**: Files grouped by type (controllers, models, etc.)
  - Each file shows [commit_hash] or [N commits] with details
- **Impact Analysis**: Breaking changes, API surface, test coverage
- **Python SDK Impact**:
  - 🔴 CRITICAL: OpenAPI spec changes (must regenerate gooddata-api-client)
  - 🟡 REVIEW: Controllers, models, API examples to check
  - SDK Action Items: Concrete next steps

================================================================================
SDK-RELEVANT FILE CATEGORIES
================================================================================

CRITICAL (requires SDK regeneration):
  - openapi_specs: OpenAPI JSON specs that generate gooddata-api-client

REVIEW (may need SDK updates):
  - controllers: REST endpoint definitions
  - models: Data transfer objects
  - api_examples: Test JSON files showing API payloads

NOT SDK-RELEVANT (internal implementation):
  - services, repositories, proto_files, grpc_clients
  - database_migrations, configuration, tests, build_files
  - ignored: lockfiles, helm charts, docker-compose, etc.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# =============================================================================
# FILE PATTERN DEFINITIONS
# =============================================================================

# These patterns define what files are relevant for REST API changes
# and how they should be categorized

FILE_CATEGORIES = {
    "openapi_specs": {
        "description": "OpenAPI specifications - CRITICAL for Python SDK generation",
        "patterns": [
            r"microservices/[^/]+/src/test/resources/openapi/open-api-spec\.json$",
            r".*/openapi/.*\.json$",
            r".*/openapi/.*\.ya?ml$",
        ],
        "priority": 0,  # Highest priority - most important for SDK
        "sdk_relevant": True,
    },
    "controllers": {
        "description": "REST API endpoint definitions",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/.*[Cc]ontroller\.kt$",
            r"microservices/[^/]+/src/main/kotlin/controller/.*\.kt$",
        ],
        "priority": 1,  # Higher priority = more important for understanding changes
        "sdk_relevant": True,
    },
    "models": {
        "description": "Data transfer objects and request/response models",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/model/.*\.kt$",
            r"microservices/[^/]+/src/main/kotlin/.*[Rr]equest\.kt$",
            r"microservices/[^/]+/src/main/kotlin/.*[Rr]esponse\.kt$",
            r"microservices/[^/]+/src/main/kotlin/service/pojo/.*\.kt$",
            r"libraries/metadata-model/src/main/kotlin/.*\.kt$",
        ],
        "priority": 2,
        "sdk_relevant": True,
    },
    "api_examples": {
        "description": "API request/response examples for SDK testing",
        "patterns": [
            r"microservices/[^/]+/src/test/resources/metadata/.*\.json$",
            r"microservices/[^/]+/src/test/resources/.*[Rr]equest.*\.json$",
            r"microservices/[^/]+/src/test/resources/.*[Rr]esponse.*\.json$",
            r"microservices/[^/]+/src/test/resources/.*[Rr]esult.*\.json$",
        ],
        "priority": 2,
        "sdk_relevant": True,
    },
    "services": {
        "description": "Business logic and service implementations",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/service/.*[Ss]ervice\.kt$",
            r"microservices/[^/]+/src/main/kotlin/service/.*[Pp]rovider\.kt$",
            r"microservices/[^/]+/src/main/kotlin/service/(?!pojo/).*\.kt$",
        ],
        "priority": 3,
        "sdk_relevant": False,  # Internal implementation, not directly exposed
    },
    "proto_files": {
        "description": "gRPC protocol buffer definitions",
        "patterns": [
            r"proto-files/[^/]+/proto/.*\.proto$",
        ],
        "priority": 2,
        "sdk_relevant": False,  # SDK uses REST API, not gRPC directly
    },
    "grpc_clients": {
        "description": "gRPC client library implementations",
        "patterns": [
            r"libraries/grpc/[^/]+-client-grpc/.*\.kt$",
            r"proto-stubs/[^/]+-stub/.*\.kt$",
        ],
        "priority": 4,
        "sdk_relevant": False,
    },
    "repositories": {
        "description": "Data access layer and database operations",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/repository/.*\.kt$",
            r"microservices/[^/]+/src/main/kotlin/.*[Rr]epository\.kt$",
        ],
        "priority": 4,
        "sdk_relevant": False,
    },
    "database_migrations": {
        "description": "Liquibase database schema changes",
        "patterns": [
            r"microservices/[^/]+/src/main/resources/db/changelog/.*\.ya?ml$",
            r"microservices/[^/]+/src/main/resources/db/changelog/.*\.xml$",
            r"microservices/[^/]+/src/main/resources/db/changelog/.*\.sql$",
        ],
        "priority": 3,
        "sdk_relevant": False,
    },
    "configuration": {
        "description": "Application and OpenAPI configuration",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/configuration/.*\.kt$",
            r"microservices/[^/]+/src/main/kotlin/config/.*\.kt$",
            r"microservices/[^/]+/src/main/kotlin/.*[Cc]onfig(uration)?\.kt$",
            r"microservices/[^/]+/src/main/resources/application.*\.ya?ml$",
            r"microservices/[^/]+/src/main/resources/application.*\.properties$",
        ],
        "priority": 5,
        "sdk_relevant": False,
    },
    "tests": {
        "description": "Unit and integration tests",
        "patterns": [
            r"microservices/[^/]+/src/test/kotlin/.*[Tt]est\.kt$",
            r"microservices/[^/]+/src/test/kotlin/controller/.*\.kt$",
            r"microservices/[^/]+/src/test/.*\.kt$",
            # Library tests (including nested libraries like execution/execution-preprocessing)
            r"libraries/.+/src/test/kotlin/.*[Tt]est\.kt$",
            r"libraries/.+/src/test/.*\.kt$",
        ],
        "priority": 6,
        "sdk_relevant": False,
    },
    "build_files": {
        "description": "Gradle build configuration",
        "patterns": [
            r"microservices/[^/]+/build\.gradle\.kts$",
            r"libraries/[^/]+/build\.gradle\.kts$",
            # Nested library build files (libraries/execution/execution-preprocessing/build.gradle.kts)
            r"libraries/.+/build\.gradle\.kts$",
            r"build\.gradle\.kts$",
            r"settings\.gradle\.kts$",
        ],
        "priority": 7,
        "sdk_relevant": False,
    },
    "shared_libraries": {
        "description": "Shared utility libraries",
        "patterns": [
            # Direct library subdirectories (libraries/common/src/...)
            r"libraries/(?!grpc/)[^/]+/src/main/kotlin/.*\.kt$",
            # Nested library structures (libraries/execution/execution-preprocessing/src/...)
            r"libraries/(?!grpc/).+/src/main/kotlin/.*\.kt$",
        ],
        "priority": 5,
        "sdk_relevant": False,
    },
    "ignored": {
        "description": "Files not relevant for SDK implementation",
        "patterns": [
            r".*\.lockfile$",
            r"helm-charts/.*",
            r"docker-compose.*\.ya?ml$",
            r"components/.*\.py$",  # Internal Python components
            r"components/gateway/.*",  # Gateway internals
            r"\.cursor/.*",
            r"gradle/.*",
            r"docs/.*",
        ],
        "priority": 99,
        "sdk_relevant": False,
    },
}

# Services/microservices in gdc-nas
KNOWN_SERVICES = [
    "metadata-api",
    "afm-exec-api",
    "api-gateway",
    "export-controller",
    "scan-model",
    "result-cache",
    "automation",
    "sql-executor",
    "export-builder",
    "llm-processor",
    "flight-server",
    "user-data-filter",
    "notification",
    "auth",
    "organization-controller",
]


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class FileChange:
    """Represents a single file change in the diff."""

    path: str
    status: str  # A=added, M=modified, D=deleted, R=renamed
    additions: int = 0
    deletions: int = 0
    old_path: Optional[str] = None  # For renames
    commits: list[dict] = field(default_factory=list)  # List of {hash, message} dicts

    @property
    def is_kotlin(self) -> bool:
        return self.path.endswith(".kt")

    @property
    def is_proto(self) -> bool:
        return self.path.endswith(".proto")

    @property
    def is_config(self) -> bool:
        return self.path.endswith((".yaml", ".yml", ".properties", ".xml"))

    @property
    def commit_str(self) -> str:
        """Return formatted commit attribution string."""
        if not self.commits:
            return ""
        if len(self.commits) == 1:
            return f" [{self.commits[0]['hash'][:8]}]"
        return f" [{len(self.commits)} commits]"

    @property
    def commit_details(self) -> str:
        """Return detailed commit list for tooltip/expansion."""
        if not self.commits:
            return ""
        return ", ".join(c["hash"][:8] for c in self.commits)


@dataclass
class CategoryResult:
    """Results for a single category of files."""

    name: str
    description: str
    files: list[FileChange] = field(default_factory=list)

    @property
    def total_additions(self) -> int:
        return sum(f.additions for f in self.files)

    @property
    def total_deletions(self) -> int:
        return sum(f.deletions for f in self.files)

    @property
    def file_count(self) -> int:
        return len(self.files)


@dataclass
class ServiceImpact:
    """Tracks which microservices are affected."""

    name: str
    files: list[FileChange] = field(default_factory=list)
    categories_affected: set[str] = field(default_factory=set)


@dataclass
class DiffAnalysis:
    """Complete analysis of a diff."""

    commit_range: str
    repo_path: str
    categories: dict[str, CategoryResult] = field(default_factory=dict)
    services_impacted: dict[str, ServiceImpact] = field(default_factory=dict)
    uncategorized_files: list[FileChange] = field(default_factory=list)
    total_files: int = 0
    total_additions: int = 0
    total_deletions: int = 0


@dataclass
class OpenAPIChange:
    """Represents a single OpenAPI endpoint or schema change."""

    name: str  # Path for endpoints, schema name for models
    change_type: str  # 'added', 'removed', 'modified'
    details: dict = field(default_factory=dict)  # Additional info (methods, fields, etc.)


@dataclass
class OpenAPIAnalysis:
    """Analysis of OpenAPI specification changes."""

    endpoints: list[OpenAPIChange] = field(default_factory=list)
    schemas: list[OpenAPIChange] = field(default_factory=list)
    parameters: list[OpenAPIChange] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.endpoints or self.schemas or self.parameters)

    @property
    def summary(self) -> str:
        """Return a one-line summary of changes."""
        parts = []
        if self.endpoints:
            added = len([e for e in self.endpoints if e.change_type == "added"])
            removed = len([e for e in self.endpoints if e.change_type == "removed"])
            modified = len([e for e in self.endpoints if e.change_type == "modified"])
            if added:
                parts.append(f"+{added} endpoints")
            if removed:
                parts.append(f"-{removed} endpoints")
            if modified:
                parts.append(f"~{modified} endpoints")
        if self.schemas:
            added = len([s for s in self.schemas if s.change_type == "added"])
            removed = len([s for s in self.schemas if s.change_type == "removed"])
            modified = len([s for s in self.schemas if s.change_type == "modified"])
            if added:
                parts.append(f"+{added} schemas")
            if removed:
                parts.append(f"-{removed} schemas")
            if modified:
                parts.append(f"~{modified} schemas")
        return ", ".join(parts) if parts else "No semantic changes detected"


# =============================================================================
# GIT OPERATIONS
# =============================================================================


def run_git_command(args: list[str], repo_path: str) -> str:
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(["git"] + args, cwd=repo_path, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: git {' '.join(args)}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def get_diff_files(commit_range: str, repo_path: str) -> list[FileChange]:
    """Get list of changed files with their status and stats."""
    # Handle single commit (compare to parent)
    if ".." not in commit_range:
        commit_range = f"{commit_range}^..{commit_range}"

    # Get file status (added/modified/deleted/renamed)
    status_output = run_git_command(["diff", "--name-status", commit_range], repo_path)

    # Get numstat for additions/deletions
    numstat_output = run_git_command(["diff", "--numstat", commit_range], repo_path)

    # Parse status
    file_status = {}
    for line in status_output.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0][0]  # First char is status (R100 -> R)
        if status == "R":
            old_path, new_path = parts[1], parts[2]
            file_status[new_path] = {"status": status, "old_path": old_path}
        else:
            file_status[parts[1]] = {"status": status, "old_path": None}

    # Parse numstat
    file_stats = {}
    for line in numstat_output.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        additions = int(parts[0]) if parts[0] != "-" else 0
        deletions = int(parts[1]) if parts[1] != "-" else 0
        path = parts[2]
        # Handle renames (format: old_path => new_path or {old => new}/rest)
        if " => " in path:
            # Extract actual path from rename syntax
            if "{" in path:
                # Format: path/{old => new}/rest
                match = re.match(r"(.*){\S+ => (\S+)}(.*)", path)
                if match:
                    path = match.group(1) + match.group(2) + match.group(3)
            else:
                # Format: old_path => new_path
                path = path.split(" => ")[1]
        file_stats[path] = {"additions": additions, "deletions": deletions}

    # Combine into FileChange objects
    changes = []
    for path, status_info in file_status.items():
        stats = file_stats.get(path, {"additions": 0, "deletions": 0})
        changes.append(
            FileChange(
                path=path,
                status=status_info["status"],
                additions=stats["additions"],
                deletions=stats["deletions"],
                old_path=status_info["old_path"],
            )
        )

    return changes


def extract_jira_ids(message: str) -> list[str]:
    """Extract JIRA ticket IDs from a commit message.

    Matches patterns like: GDAI-1045, CQ-1794, QA-26284, LX-1885
    """
    pattern = r"\b([A-Z]{2,}-\d+)\b"
    matches = re.findall(pattern, message, re.IGNORECASE)
    # Normalize to uppercase and deduplicate while preserving order
    seen = set()
    result = []
    for m in matches:
        upper = m.upper()
        if upper not in seen:
            seen.add(upper)
            result.append(upper)
    return result


def get_file_diff_content(commit_range: str, file_path: str, repo_path: str) -> str:
    """Get the actual diff content for a specific file."""
    if ".." not in commit_range:
        commit_range = f"{commit_range}^..{commit_range}"

    return run_git_command(["diff", commit_range, "--", file_path], repo_path)


def get_file_commit_mapping(commit_range: str, repo_path: str) -> dict[str, list[dict]]:
    """Get mapping of file paths to the commits that modified them.

    Returns dict: {file_path: [{hash, message}, ...]}
    """
    # Get all commits in the range
    if ".." not in commit_range:
        commit_range = f"{commit_range}^..{commit_range}"

    # Get commit list with files
    output = run_git_command(["log", "--name-only", "--format=COMMIT:%H|%s", commit_range], repo_path)

    file_to_commits: dict[str, list[dict]] = defaultdict(list)
    current_commit = None

    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("COMMIT:"):
            parts = line[7:].split("|", 1)
            current_commit = {"hash": parts[0], "message": parts[1] if len(parts) > 1 else ""}
        elif current_commit:
            # This is a file path
            file_to_commits[line].append(current_commit)

    return dict(file_to_commits)


# =============================================================================
# CATEGORIZATION LOGIC
# =============================================================================


def categorize_file(file_path: str) -> Optional[str]:
    """Determine which category a file belongs to."""
    for category_name, category_info in FILE_CATEGORIES.items():
        for pattern in category_info["patterns"]:
            if re.search(pattern, file_path):
                return category_name
    return None


def extract_service_name(file_path: str) -> Optional[str]:
    """Extract the microservice name from a file path."""
    # Match microservices/{service}/...
    match = re.match(r"microservices/([^/]+)/", file_path)
    if match:
        return match.group(1)

    # Match proto-files/{service}/...
    match = re.match(r"proto-files/([^/]+)/", file_path)
    if match:
        return match.group(1)

    # Match libraries/grpc/{service}-client-grpc/...
    match = re.match(r"libraries/grpc/([^/]+)-client-grpc/", file_path)
    if match:
        return match.group(1)

    return None


def analyze_diff(commit_range: str, repo_path: str, track_commits: bool = False) -> DiffAnalysis:
    """Perform complete analysis of a git diff.

    Args:
        commit_range: Git commit range to analyze
        repo_path: Path to git repository
        track_commits: If True, track which commits modified each file
    """
    analysis = DiffAnalysis(commit_range=commit_range, repo_path=repo_path)

    # Initialize categories
    for cat_name, cat_info in FILE_CATEGORIES.items():
        analysis.categories[cat_name] = CategoryResult(name=cat_name, description=cat_info["description"])

    # Get all changed files
    changes = get_diff_files(commit_range, repo_path)
    analysis.total_files = len(changes)

    # Get file-to-commit mapping if tracking commits
    file_commits = {}
    if track_commits:
        file_commits = get_file_commit_mapping(commit_range, repo_path)

    for change in changes:
        analysis.total_additions += change.additions
        analysis.total_deletions += change.deletions

        # Add commit attribution if tracking
        if track_commits and change.path in file_commits:
            change.commits = file_commits[change.path]

        # Categorize file
        category = categorize_file(change.path)
        if category:
            analysis.categories[category].files.append(change)
        else:
            analysis.uncategorized_files.append(change)

        # Track service impact
        service = extract_service_name(change.path)
        if service:
            if service not in analysis.services_impacted:
                analysis.services_impacted[service] = ServiceImpact(name=service)
            analysis.services_impacted[service].files.append(change)
            if category:
                analysis.services_impacted[service].categories_affected.add(category)

    return analysis


# =============================================================================
# CONTENT ANALYSIS
# =============================================================================


def extract_endpoint_changes(diff_content: str) -> list[dict]:
    """Extract REST endpoint changes from a controller diff."""
    endpoints = []

    # Patterns to match REST endpoint annotations
    endpoint_patterns = [
        (r'\+\s*@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\s*\(\s*["\']([^"\']+)["\']', "added"),
        (r'-\s*@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\s*\(\s*["\']([^"\']+)["\']', "removed"),
    ]

    for pattern, change_type in endpoint_patterns:
        matches = re.findall(pattern, diff_content)
        for method, path in matches:
            endpoints.append(
                {"method": method.replace("Mapping", "").upper(), "path": path, "change_type": change_type}
            )

    return endpoints


def extract_function_changes(diff_content: str) -> list[dict]:
    """Extract function/method changes from Kotlin diff."""
    functions = []

    # Pattern for Kotlin function definitions
    func_pattern = r"^([+-])\s*(suspend\s+)?(fun\s+\w+)\s*\("

    for match in re.finditer(func_pattern, diff_content, re.MULTILINE):
        change_type = "added" if match.group(1) == "+" else "removed"
        is_suspend = bool(match.group(2))
        func_name = match.group(3).replace("fun ", "")
        functions.append({"name": func_name, "is_suspend": is_suspend, "change_type": change_type})

    return functions


def extract_proto_changes(diff_content: str) -> list[dict]:
    """Extract proto message and service changes."""
    changes = []

    # Message definitions
    msg_pattern = r"^([+-])\s*message\s+(\w+)"
    for match in re.finditer(msg_pattern, diff_content, re.MULTILINE):
        changes.append(
            {"type": "message", "name": match.group(2), "change_type": "added" if match.group(1) == "+" else "removed"}
        )

    # RPC definitions
    rpc_pattern = r"^([+-])\s*rpc\s+(\w+)"
    for match in re.finditer(rpc_pattern, diff_content, re.MULTILINE):
        changes.append(
            {"type": "rpc", "name": match.group(2), "change_type": "added" if match.group(1) == "+" else "removed"}
        )

    return changes


def get_file_content_at_commit(commit: str, file_path: str, repo_path: str) -> Optional[str]:
    """Get file content at a specific commit."""
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{file_path}"], cwd=repo_path, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def analyze_openapi_diff(commit_range: str, file_path: str, repo_path: str) -> OpenAPIAnalysis:
    """
    Analyze OpenAPI specification changes between two commits.

    Compares the JSON structure to identify:
    - New/removed/modified endpoints (paths)
    - New/removed/modified schemas (components/schemas)
    - New/removed/modified parameters
    """
    analysis = OpenAPIAnalysis()

    # Parse commit range
    if ".." not in commit_range:
        before_commit = f"{commit_range}^"
        after_commit = commit_range
    else:
        before_commit, after_commit = commit_range.split("..", 1)

    # Get file content before and after
    before_content = get_file_content_at_commit(before_commit, file_path, repo_path)
    after_content = get_file_content_at_commit(after_commit, file_path, repo_path)

    # Parse JSON
    before_spec = {}
    after_spec = {}

    try:
        if before_content:
            before_spec = json.loads(before_content)
    except json.JSONDecodeError:
        pass

    try:
        if after_content:
            after_spec = json.loads(after_content)
    except json.JSONDecodeError:
        pass

    # If we couldn't parse either, return empty analysis
    if not before_spec and not after_spec:
        return analysis

    # Analyze paths (endpoints)
    before_paths = before_spec.get("paths", {})
    after_paths = after_spec.get("paths", {})

    all_paths = set(before_paths.keys()) | set(after_paths.keys())

    for path in sorted(all_paths):
        before_path_data = before_paths.get(path, {})
        after_path_data = after_paths.get(path, {})

        if path not in before_paths:
            # New endpoint
            methods = [
                m.upper() for m in after_path_data if m in ("get", "post", "put", "delete", "patch", "options", "head")
            ]
            analysis.endpoints.append(OpenAPIChange(name=path, change_type="added", details={"methods": methods}))
        elif path not in after_paths:
            # Removed endpoint
            methods = [
                m.upper() for m in before_path_data if m in ("get", "post", "put", "delete", "patch", "options", "head")
            ]
            analysis.endpoints.append(OpenAPIChange(name=path, change_type="removed", details={"methods": methods}))
        else:
            # Check for method changes within the path
            before_methods = set(
                m for m in before_path_data if m in ("get", "post", "put", "delete", "patch", "options", "head")
            )
            after_methods = set(
                m for m in after_path_data if m in ("get", "post", "put", "delete", "patch", "options", "head")
            )

            added_methods = after_methods - before_methods
            removed_methods = before_methods - after_methods

            # Check for modifications in existing methods
            modified_methods = []
            for method in before_methods & after_methods:
                if before_path_data.get(method) != after_path_data.get(method):
                    modified_methods.append(method.upper())

            if added_methods or removed_methods or modified_methods:
                analysis.endpoints.append(
                    OpenAPIChange(
                        name=path,
                        change_type="modified",
                        details={
                            "added_methods": [m.upper() for m in added_methods],
                            "removed_methods": [m.upper() for m in removed_methods],
                            "modified_methods": modified_methods,
                        },
                    )
                )

    # Analyze schemas (components/schemas)
    before_schemas = before_spec.get("components", {}).get("schemas", {})
    after_schemas = after_spec.get("components", {}).get("schemas", {})

    all_schemas = set(before_schemas.keys()) | set(after_schemas.keys())

    for schema_name in sorted(all_schemas):
        before_schema = before_schemas.get(schema_name)
        after_schema = after_schemas.get(schema_name)

        if schema_name not in before_schemas:
            # New schema
            schema_type = after_schema.get("type", "object")
            properties = list(after_schema.get("properties", {}).keys()) if after_schema else []
            analysis.schemas.append(
                OpenAPIChange(
                    name=schema_name,
                    change_type="added",
                    details={"type": schema_type, "properties": properties[:10]},  # Limit to first 10 properties
                )
            )
        elif schema_name not in after_schemas:
            # Removed schema
            schema_type = before_schema.get("type", "object")
            analysis.schemas.append(
                OpenAPIChange(name=schema_name, change_type="removed", details={"type": schema_type})
            )
        elif before_schema != after_schema:
            # Modified schema - find what changed
            before_props = set(before_schema.get("properties", {}).keys()) if before_schema else set()
            after_props = set(after_schema.get("properties", {}).keys()) if after_schema else set()

            added_props = after_props - before_props
            removed_props = before_props - after_props

            # Check for modified properties
            modified_props = []
            for prop in before_props & after_props:
                if before_schema.get("properties", {}).get(prop) != after_schema.get("properties", {}).get(prop):
                    modified_props.append(prop)

            analysis.schemas.append(
                OpenAPIChange(
                    name=schema_name,
                    change_type="modified",
                    details={
                        "added_properties": list(added_props)[:10],
                        "removed_properties": list(removed_props)[:10],
                        "modified_properties": modified_props[:10],
                    },
                )
            )

    # Analyze parameters (components/parameters)
    before_params = before_spec.get("components", {}).get("parameters", {})
    after_params = after_spec.get("components", {}).get("parameters", {})

    all_params = set(before_params.keys()) | set(after_params.keys())

    for param_name in sorted(all_params):
        if param_name not in before_params:
            analysis.parameters.append(OpenAPIChange(name=param_name, change_type="added", details={}))
        elif param_name not in after_params:
            analysis.parameters.append(OpenAPIChange(name=param_name, change_type="removed", details={}))
        elif before_params.get(param_name) != after_params.get(param_name):
            analysis.parameters.append(OpenAPIChange(name=param_name, change_type="modified", details={}))

    return analysis


def format_openapi_analysis(analysis: OpenAPIAnalysis) -> list[str]:
    """Format OpenAPI analysis results as markdown lines."""
    lines = []

    if not analysis.has_changes:
        lines.append("*No semantic API changes detected (possibly formatting/comments only)*")
        return lines

    # Endpoints section
    if analysis.endpoints:
        lines.append("**Endpoint Changes:**")
        lines.append("")

        # Group by change type
        added = [e for e in analysis.endpoints if e.change_type == "added"]
        removed = [e for e in analysis.endpoints if e.change_type == "removed"]
        modified = [e for e in analysis.endpoints if e.change_type == "modified"]

        if added:
            lines.append("*Added:*")
            for ep in added:
                methods = ", ".join(ep.details.get("methods", []))
                lines.append(f"- ➕ `{ep.name}` [{methods}]")
            lines.append("")

        if removed:
            lines.append("*Removed:*")
            for ep in removed:
                methods = ", ".join(ep.details.get("methods", []))
                lines.append(f"- ➖ `{ep.name}` [{methods}]")
            lines.append("")

        if modified:
            lines.append("*Modified:*")
            for ep in modified:
                changes = []
                if ep.details.get("added_methods"):
                    changes.append(f"+{','.join(ep.details['added_methods'])}")
                if ep.details.get("removed_methods"):
                    changes.append(f"-{','.join(ep.details['removed_methods'])}")
                if ep.details.get("modified_methods"):
                    changes.append(f"~{','.join(ep.details['modified_methods'])}")
                lines.append(f"- 📝 `{ep.name}` [{', '.join(changes)}]")
            lines.append("")

    # Schemas section
    if analysis.schemas:
        lines.append("**Schema Changes:**")
        lines.append("")

        added = [s for s in analysis.schemas if s.change_type == "added"]
        removed = [s for s in analysis.schemas if s.change_type == "removed"]
        modified = [s for s in analysis.schemas if s.change_type == "modified"]

        if added:
            lines.append("*Added:*")
            for schema in added:
                props = schema.details.get("properties", [])
                prop_hint = f" ({len(props)} props)" if props else ""
                lines.append(f"- ➕ `{schema.name}`{prop_hint}")
            lines.append("")

        if removed:
            lines.append("*Removed:*")
            for schema in removed:
                lines.append(f"- ➖ `{schema.name}`")
            lines.append("")

        if modified:
            lines.append("*Modified:*")
            for schema in modified:
                changes = []
                if schema.details.get("added_properties"):
                    changes.append(f"+{len(schema.details['added_properties'])} props")
                if schema.details.get("removed_properties"):
                    changes.append(f"-{len(schema.details['removed_properties'])} props")
                if schema.details.get("modified_properties"):
                    changes.append(f"~{len(schema.details['modified_properties'])} props")
                change_str = f" [{', '.join(changes)}]" if changes else ""
                lines.append(f"- 📝 `{schema.name}`{change_str}")

                # Show property details for modified schemas
                if schema.details.get("added_properties"):
                    for prop in schema.details["added_properties"][:5]:
                        lines.append(f"    - ➕ `{prop}`")
                    if len(schema.details["added_properties"]) > 5:
                        lines.append(f"    - ... and {len(schema.details['added_properties']) - 5} more")
                if schema.details.get("removed_properties"):
                    for prop in schema.details["removed_properties"][:5]:
                        lines.append(f"    - ➖ `{prop}`")
                    if len(schema.details["removed_properties"]) > 5:
                        lines.append(f"    - ... and {len(schema.details['removed_properties']) - 5} more")
            lines.append("")

    # Parameters section (brief)
    if analysis.parameters:
        added = len([p for p in analysis.parameters if p.change_type == "added"])
        removed = len([p for p in analysis.parameters if p.change_type == "removed"])
        modified = len([p for p in analysis.parameters if p.change_type == "modified"])

        parts = []
        if added:
            parts.append(f"+{added}")
        if removed:
            parts.append(f"-{removed}")
        if modified:
            parts.append(f"~{modified}")

        lines.append(f"**Parameter Changes:** {', '.join(parts)}")
        lines.append("")

    return lines


def deduplicate_diff_blocks(diff_lines: list[str], min_block_size: int = 2) -> list[str]:
    """
    Deduplicate repeated diff blocks and collapse them with a count.

    A "block" is a sequence of consecutive lines with the same change type (+/-)
    that forms a logical unit. Identical blocks are shown once with a count.

    Args:
        diff_lines: List of diff lines (starting with + or -)
        min_block_size: Minimum number of lines to consider as a repeatable block

    Returns:
        Deduplicated list of diff lines with count annotations
    """
    if not diff_lines:
        return []

    # Parse diff lines into blocks based on change type and content structure
    # A block is a group of consecutive lines that share the same prefix (+/-)
    # and appear to be part of the same logical structure (e.g., JSON object)

    blocks = []
    current_block = []
    current_prefix = None

    for line in diff_lines:
        prefix = line[0] if line else ""

        # Check if this continues the current block or starts a new one
        if prefix != current_prefix and current_block:
            blocks.append(current_block)
            current_block = []

        current_prefix = prefix
        current_block.append(line)

    # Don't forget the last block
    if current_block:
        blocks.append(current_block)

    # Now identify repeated blocks
    # Convert blocks to tuples for hashing
    block_tuples = [tuple(block) for block in blocks]

    # Count occurrences of each block
    block_counts = Counter(block_tuples)

    # Build output with deduplication
    output_lines = []
    seen_blocks = set()

    for block_tuple in block_tuples:
        if block_tuple in seen_blocks:
            continue

        count = block_counts[block_tuple]
        block_lines = list(block_tuple)

        if count > 1 and len(block_lines) >= min_block_size:
            # Add count annotation before the block
            output_lines.append(f"# ⟳ Following block repeated {count}x:")
            output_lines.extend(block_lines)
            seen_blocks.add(block_tuple)
        else:
            output_lines.extend(block_lines)
            if count > 1:
                seen_blocks.add(block_tuple)

    return output_lines


def deduplicate_diff_content_smart(diff_lines: list[str], context_lines: int = 1) -> list[str]:
    """
    Smart deduplication that identifies repeated multi-line patterns across the diff.

    This handles cases where the same JSON/YAML block is added/removed in multiple
    locations, showing it once with a count of occurrences.

    Args:
        diff_lines: List of diff lines (starting with + or -)
        context_lines: Number of context lines to group together

    Returns:
        Deduplicated list of diff lines with count annotations
    """
    if not diff_lines:
        return []

    # Strategy: Look for repeated sequences of N consecutive lines
    # Start with larger sequences and work down

    # Normalize lines for comparison (strip trailing whitespace but preserve leading)
    normalized = [line.rstrip() for line in diff_lines]

    # Find repeated sequences of various lengths (from longest to shortest)
    max_seq_len = min(20, len(normalized) // 2)  # Don't look for sequences longer than half the content
    min_seq_len = 2

    # Track which line indices have been "consumed" by a repeated block
    consumed = set()

    # Store (start_idx, length, count) for repeated blocks we find
    repeated_blocks = []

    for seq_len in range(max_seq_len, min_seq_len - 1, -1):
        # Find all sequences of this length
        sequences = {}
        for i in range(len(normalized) - seq_len + 1):
            if any(j in consumed for j in range(i, i + seq_len)):
                continue
            seq = tuple(normalized[i : i + seq_len])
            if seq not in sequences:
                sequences[seq] = []
            sequences[seq].append(i)

        # Find sequences that appear more than once
        for seq, indices in sequences.items():
            if len(indices) > 1:
                # Check that none of these indices overlap with already consumed lines
                valid_indices = [idx for idx in indices if not any(j in consumed for j in range(idx, idx + seq_len))]
                if len(valid_indices) > 1:
                    # Mark first occurrence as the "keeper", mark rest as consumed
                    first_idx = valid_indices[0]
                    repeated_blocks.append((first_idx, seq_len, len(valid_indices)))
                    # Consume all occurrences
                    for idx in valid_indices:
                        for j in range(idx, idx + seq_len):
                            consumed.add(j)

    # Sort repeated blocks by their position
    repeated_blocks.sort(key=lambda x: x[0])

    # Build output
    output_lines = []
    i = 0
    block_idx = 0

    while i < len(diff_lines):
        # Check if we're at a repeated block
        if block_idx < len(repeated_blocks) and i == repeated_blocks[block_idx][0]:
            start_idx, length, count = repeated_blocks[block_idx]
            output_lines.append(f"# ⟳ Following block repeated {count}x:")
            output_lines.extend(diff_lines[start_idx : start_idx + length])
            i = start_idx + length
            block_idx += 1
        elif i in consumed:
            # Skip lines that were part of repeated blocks (not the first occurrence)
            i += 1
        else:
            output_lines.append(diff_lines[i])
            i += 1

    return output_lines


# =============================================================================
# MARKDOWN OUTPUT
# =============================================================================


def generate_markdown_report(analysis: DiffAnalysis, repo_path: str) -> str:
    """Generate a comprehensive markdown report."""
    lines = []

    # Header
    lines.append("# GDC-NAS REST API Diff Analysis")
    lines.append("")
    lines.append(f"**Commit Range:** `{analysis.commit_range}`")
    lines.append(f"**Repository:** `{analysis.repo_path}`")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total Files Changed:** {analysis.total_files}")
    lines.append(f"- **Lines Added:** +{analysis.total_additions}")
    lines.append(f"- **Lines Removed:** -{analysis.total_deletions}")
    lines.append(f"- **Services Impacted:** {len(analysis.services_impacted)}")
    lines.append("")

    # Services impacted (quick overview)
    if analysis.services_impacted:
        lines.append("### Services Affected")
        lines.append("")
        for service_name in sorted(analysis.services_impacted.keys()):
            service = analysis.services_impacted[service_name]
            categories = ", ".join(sorted(service.categories_affected))
            lines.append(f"- **{service_name}** ({len(service.files)} files): {categories}")
        lines.append("")

    # Detailed category breakdown
    lines.append("## Changes by Category")
    lines.append("")

    # Sort categories by priority
    sorted_categories = sorted(
        [(name, cat) for name, cat in analysis.categories.items() if cat.files],
        key=lambda x: FILE_CATEGORIES[x[0]]["priority"],
    )

    for cat_name, category in sorted_categories:
        lines.append(f"### {cat_name.replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"*{category.description}*")
        lines.append("")
        lines.append(
            f"**Files:** {category.file_count} | **+{category.total_additions}** / **-{category.total_deletions}**"
        )
        lines.append("")

        # List files with status indicators
        for file in sorted(category.files, key=lambda f: f.path):
            status_icon = {"A": "🆕", "M": "📝", "D": "🗑️", "R": "📋"}.get(file.status, "❓")
            commit_info = file.commit_str if file.commits else ""
            lines.append(f"- {status_icon} `{file.path}` (+{file.additions}/-{file.deletions}){commit_info}")
            # Show commit details if multiple commits
            if len(file.commits) > 1:
                for c in file.commits:
                    lines.append(f"  - `{c['hash'][:8]}` {c['message'][:60]}{'...' if len(c['message']) > 60 else ''}")

            # For controllers, try to extract endpoint changes
            if cat_name == "controllers" and file.status in ("A", "M"):
                try:
                    diff_content = get_file_diff_content(analysis.commit_range, file.path, repo_path)
                    endpoints = extract_endpoint_changes(diff_content)
                    for ep in endpoints:
                        ep_icon = "➕" if ep["change_type"] == "added" else "➖"
                        lines.append(f"  - {ep_icon} `{ep['method']} {ep['path']}`")
                except Exception:
                    pass

            # For proto files, extract message/rpc changes
            if cat_name == "proto_files" and file.status in ("A", "M"):
                try:
                    diff_content = get_file_diff_content(analysis.commit_range, file.path, repo_path)
                    proto_changes = extract_proto_changes(diff_content)
                    for pc in proto_changes:
                        pc_icon = "➕" if pc["change_type"] == "added" else "➖"
                        lines.append(f"  - {pc_icon} `{pc['type']} {pc['name']}`")
                except Exception:
                    pass

        lines.append("")

    # Uncategorized files
    if analysis.uncategorized_files:
        lines.append("### Other Files")
        lines.append("")
        lines.append("*Files not matching REST API patterns*")
        lines.append("")
        for file in sorted(analysis.uncategorized_files, key=lambda f: f.path):
            status_icon = {"A": "🆕", "M": "📝", "D": "🗑️", "R": "📋"}.get(file.status, "❓")
            commit_info = file.commit_str if file.commits else ""
            lines.append(f"- {status_icon} `{file.path}` (+{file.additions}/-{file.deletions}){commit_info}")
            # Show commit details if multiple commits
            if len(file.commits) > 1:
                for c in file.commits:
                    lines.append(f"  - `{c['hash'][:8]}` {c['message'][:60]}{'...' if len(c['message']) > 60 else ''}")
        lines.append("")

    # Impact analysis
    lines.append("## Impact Analysis")
    lines.append("")

    # Check for breaking changes indicators
    breaking_indicators = []

    # Deleted controllers or endpoints
    deleted_controllers = [
        f for f in analysis.categories.get("controllers", CategoryResult("", "")).files if f.status == "D"
    ]
    if deleted_controllers:
        breaking_indicators.append(f"- ⚠️ **Deleted Controllers:** {len(deleted_controllers)} controller(s) removed")

    # Proto file changes (potentially breaking)
    proto_changes = analysis.categories.get("proto_files", CategoryResult("", ""))
    if proto_changes.files:
        breaking_indicators.append(
            f"- ⚠️ **Proto Changes:** {proto_changes.file_count} proto file(s) modified - check for breaking contract changes"
        )

    # Database migrations
    db_changes = analysis.categories.get("database_migrations", CategoryResult("", ""))
    if db_changes.files:
        breaking_indicators.append(
            f"- ℹ️ **Database Migrations:** {db_changes.file_count} migration(s) - ensure backwards compatibility"
        )

    if breaking_indicators:
        lines.append("### Potential Breaking Changes")
        lines.append("")
        lines.extend(breaking_indicators)
        lines.append("")

    # API surface changes
    api_additions = analysis.categories.get("controllers", CategoryResult("", "")).total_additions
    api_deletions = analysis.categories.get("controllers", CategoryResult("", "")).total_deletions
    model_additions = analysis.categories.get("models", CategoryResult("", "")).total_additions
    model_deletions = analysis.categories.get("models", CategoryResult("", "")).total_deletions

    lines.append("### API Surface")
    lines.append("")
    lines.append(f"- Controller changes: +{api_additions}/-{api_deletions} lines")
    lines.append(f"- Model changes: +{model_additions}/-{model_deletions} lines")
    lines.append("")

    # Testing coverage
    test_changes = analysis.categories.get("tests", CategoryResult("", ""))
    if test_changes.files:
        lines.append("### Test Coverage")
        lines.append("")
        lines.append(f"- {test_changes.file_count} test file(s) modified")
        lines.append(f"- +{test_changes.total_additions}/-{test_changes.total_deletions} test lines")
        lines.append("")
    else:
        lines.append("### Test Coverage")
        lines.append("")
        lines.append("- ⚠️ **No test changes detected** - consider if tests are needed for these changes")
        lines.append("")

    # Python SDK Impact Section
    lines.append("## Python SDK Impact")
    lines.append("")

    sdk_relevant_categories = [
        (name, cat)
        for name, cat in analysis.categories.items()
        if cat.files and FILE_CATEGORIES.get(name, {}).get("sdk_relevant", False)
    ]

    if sdk_relevant_categories:
        # OpenAPI specs first - CRITICAL section with full diff if small
        openapi_changes = analysis.categories.get("openapi_specs", CategoryResult("", ""))
        if openapi_changes.files:
            lines.append("### 🔴 CRITICAL: OpenAPI Spec Changes")
            lines.append("")
            lines.append("*These changes directly affect `gooddata-api-client` generation*")
            lines.append("")

            for file in sorted(openapi_changes.files, key=lambda f: f.path):
                status_icon = {"A": "🆕", "M": "📝", "D": "🗑️", "R": "📋"}.get(file.status, "❓")
                lines.append(f"#### {status_icon} `{file.path}`")
                lines.append("")
                lines.append(f"**Changes:** +{file.additions}/-{file.deletions} lines")
                lines.append("")

                # Perform semantic OpenAPI analysis
                if file.status in ("A", "M"):
                    try:
                        openapi_analysis = analyze_openapi_diff(analysis.commit_range, file.path, repo_path)
                        if openapi_analysis.has_changes:
                            lines.append(f"**API Summary:** {openapi_analysis.summary}")
                            lines.append("")
                            lines.extend(format_openapi_analysis(openapi_analysis))
                    except Exception as e:
                        lines.append(f"*Unable to analyze OpenAPI structure: {e}*")
                        lines.append("")

                # Show full diff if under 100 lines of changes
                total_changes = file.additions + file.deletions
                if total_changes <= 100 and file.status in ("A", "M"):
                    try:
                        diff_content = get_file_diff_content(analysis.commit_range, file.path, repo_path)
                        # Extract only the actual changes (lines starting with + or -)
                        diff_lines = []
                        for line in diff_content.split("\n"):
                            if (
                                line.startswith("+")
                                and not line.startswith("+++")
                                or line.startswith("-")
                                and not line.startswith("---")
                            ):
                                diff_lines.append(line)

                        if diff_lines:
                            lines.append("<details>")
                            lines.append("<summary>Raw diff (click to expand)</summary>")
                            lines.append("")
                            # Deduplicate repeated blocks (e.g., same property added to multiple locations)
                            deduped_lines = deduplicate_diff_content_smart(diff_lines)
                            lines.append("```diff")
                            lines.extend(deduped_lines[:100])  # Cap at 100 lines just in case
                            lines.append("```")
                            lines.append("")
                            lines.append("</details>")
                            lines.append("")
                    except Exception:
                        lines.append("*Unable to retrieve diff content*")
                        lines.append("")
                else:
                    lines.append(f"*Diff too large ({total_changes} lines) - review manually*")
                    lines.append("")

        # Review section for other SDK-relevant files
        review_categories = [(name, cat) for name, cat in sdk_relevant_categories if name != "openapi_specs"]

        if review_categories:
            lines.append("### 🟡 REVIEW: Files to Check")
            lines.append("")
            lines.append("*Review these files and update SDK if needed*")
            lines.append("")

            for cat_name, category in sorted(review_categories, key=lambda x: FILE_CATEGORIES[x[0]]["priority"]):
                lines.append(f"#### {cat_name.replace('_', ' ').title()}")
                lines.append("")
                for file in sorted(category.files, key=lambda f: f.path):
                    status_icon = {"A": "🆕", "M": "📝", "D": "🗑️", "R": "📋"}.get(file.status, "❓")
                    commit_info = file.commit_str if file.commits else ""
                    lines.append(f"- {status_icon} `{file.path}` (+{file.additions}/-{file.deletions}){commit_info}")
                lines.append("")

        # SDK action items
        lines.append("### SDK Action Items")
        lines.append("")

        if openapi_changes.files:
            lines.append("1. **Regenerate API Client**: OpenAPI specs changed - run `make generate-client`")

        controller_changes = analysis.categories.get("controllers", CategoryResult("", ""))
        if controller_changes.files:
            lines.append(
                "2. **Review New Endpoints**: Check if new REST endpoints need SDK wrapper methods in `gooddata-sdk`"
            )

        model_changes = analysis.categories.get("models", CategoryResult("", ""))
        if model_changes.files:
            lines.append("3. **Update Models**: Data models changed - verify SDK model mappings match")

        api_examples = analysis.categories.get("api_examples", CategoryResult("", ""))
        if api_examples.files:
            lines.append("4. **Update Tests**: API examples changed - update SDK integration tests")

        lines.append("")
    else:
        lines.append("*No SDK-relevant changes detected in this commit.*")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("*Generated by gdc-nas-diff-analyzer*")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================


def get_commits_since(since_commit: str, repo_path: str) -> list[dict]:
    """Get list of commits from HEAD until (not including) the specified commit."""
    # Get commit log from HEAD to the since commit
    output = run_git_command(["log", "--oneline", "--format=%H|%s", f"{since_commit}..HEAD"], repo_path)

    commits = []
    for line in output.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 1)
        if len(parts) == 2:
            commits.append({"hash": parts[0], "message": parts[1]})

    return commits


def main():
    parser = argparse.ArgumentParser(
        description="Analyze git diffs in gdc-nas for REST API changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze a single commit
    python gdc-nas-diff-analyzer.py abc123 --repo-path ./gdc-nas

    # Analyze a commit range (with commit attribution)
    python gdc-nas-diff-analyzer.py HEAD~50..HEAD --repo-path ./gdc-nas

    # List commits since a specific commit (dry run)
    python gdc-nas-diff-analyzer.py --since abc123 --list-commits --repo-path ./gdc-nas

    # Analyze each commit individually
    python gdc-nas-diff-analyzer.py --since abc123 --per-commit --repo-path ./gdc-nas

    # [RECOMMENDED] Find SDK-relevant commits and show full details
    python gdc-nas-diff-analyzer.py --since abc123 --sdk-details --repo-path ./gdc-nas

    # Save each SDK-relevant commit to separate files
    python gdc-nas-diff-analyzer.py --since abc123 --sdk-details --output-dir ./reports --repo-path ./gdc-nas

    # Disable commit attribution on files
    python gdc-nas-diff-analyzer.py HEAD~50..HEAD --no-commits --repo-path ./gdc-nas
""",
    )
    parser.add_argument(
        "commit_range", nargs="?", help="Git commit SHA or range (e.g., abc123, HEAD~5..HEAD, main..feature-branch)"
    )
    parser.add_argument(
        "--since",
        metavar="COMMIT",
        help="Analyze all commits from this commit (exclusive) to HEAD. "
        "Useful for incremental analysis - remember last analyzed commit.",
    )
    parser.add_argument(
        "--list-commits", action="store_true", help="Only list commits that would be analyzed (use with --since)"
    )
    parser.add_argument(
        "--per-commit",
        action="store_true",
        help="Analyze each commit individually instead of as a combined diff (use with --since)",
    )
    parser.add_argument("--repo-path", default="./gdc-nas", help="Path to the gdc-nas repository (default: ./gdc-nas)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument(
        "--output-dir",
        metavar="DIR",
        help="Save each SDK-relevant commit report to a separate file in this directory. "
        "Use with --sdk-details. Files are named by commit hash.",
    )
    parser.add_argument(
        "--sdk-only",
        action="store_true",
        help="Only output if SDK-relevant changes are found (openapi_specs, controllers, models, api_examples). "
        "Useful when analyzing many commits to filter out noise.",
    )
    parser.add_argument(
        "--sdk-details",
        action="store_true",
        help="Scan commits to find SDK-relevant ones, then output full detailed analysis for each. "
        "Use with --since to analyze a range of commits.",
    )
    parser.add_argument(
        "--show-commits",
        action="store_true",
        default=True,
        help="Show which commit(s) modified each file (default: enabled for ranges)",
    )
    parser.add_argument("--no-commits", action="store_true", help="Disable commit attribution on files")

    args = parser.parse_args()

    # Handle --no-commits flag
    if args.no_commits:
        args.show_commits = False

    # Validate arguments
    if not args.commit_range and not args.since:
        parser.error("Either commit_range or --since is required")

    # Resolve repo path
    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)

    if not (repo_path / ".git").exists():
        print(f"Error: Not a git repository: {repo_path}", file=sys.stderr)
        sys.exit(1)

    # Handle --since mode
    if args.since:
        commits = get_commits_since(args.since, str(repo_path))

        if not commits:
            print(f"No commits found between {args.since} and HEAD", file=sys.stderr)
            sys.exit(0)

        # List commits mode
        if args.list_commits:
            print(f"# Commits since {args.since} ({len(commits)} commits)")
            print("")
            for i, commit in enumerate(commits, 1):
                print(f"{i}. `{commit['hash'][:12]}` - {commit['message']}")
            print("")
            print("# To analyze all as combined diff:")
            print(f"python gdc-nas-diff-analyzer.py {args.since}..HEAD --repo-path {args.repo_path}")
            print("")
            print("# To analyze each commit individually:")
            print(f"python gdc-nas-diff-analyzer.py --since {args.since} --per-commit --repo-path {args.repo_path}")
            sys.exit(0)

        # SDK-details mode: find SDK-relevant commits, then show full analysis for each
        if args.sdk_details:
            sdk_relevant_commits = []

            print(f"Scanning {len(commits)} commits for SDK-relevant changes...", file=sys.stderr)
            for i, commit in enumerate(commits, 1):
                print(f"  [{i}/{len(commits)}] {commit['hash'][:12]}...", file=sys.stderr, end="\r")

                analysis = analyze_diff(commit["hash"], str(repo_path))

                # Check if SDK-relevant
                has_sdk_changes = any(
                    analysis.categories.get(cat, CategoryResult("", "")).files
                    for cat in ["openapi_specs", "controllers", "models", "api_examples"]
                )

                if has_sdk_changes:
                    sdk_relevant_commits.append({"commit": commit, "analysis": analysis})

            print(f"\nFound {len(sdk_relevant_commits)} SDK-relevant commits", file=sys.stderr)

            if not sdk_relevant_commits:
                print(f"No SDK-relevant changes found in {len(commits)} commits since {args.since}", file=sys.stderr)
                sys.exit(0)

            # Build report with full details for each SDK-relevant commit
            all_reports = []
            all_reports.append("# GDC-NAS SDK-Relevant Changes Report")
            all_reports.append("")
            all_reports.append(f"**Range:** `{args.since}..HEAD`")
            all_reports.append(f"**Scanned:** {len(commits)} commits")
            all_reports.append(f"**SDK-relevant:** {len(sdk_relevant_commits)} commits")
            all_reports.append("")
            all_reports.append(f"**Latest commit analyzed:** `{commits[0]['hash'][:12]}`")
            all_reports.append("")

            # Quick summary table
            # Sort: merge commits (PRs) first, then others
            def is_merge_commit(item):
                msg = item["commit"]["message"].lower()
                return msg.startswith(("merge pull request", "merge branch"))

            sorted_commits = sorted(sdk_relevant_commits, key=lambda x: (0 if is_merge_commit(x) else 1))

            all_reports.append("## Summary")
            all_reports.append("")
            all_reports.append("| Commit | JIRA | Message | Impact |")
            all_reports.append("|--------|------|---------|--------|")
            for item in sorted_commits:
                c = item["commit"]
                a = item["analysis"]
                jira_ids = extract_jira_ids(c["message"])
                jira_str = ", ".join(jira_ids) if jira_ids else "-"
                impacts = []
                for cat in ["openapi_specs", "controllers", "models", "api_examples"]:
                    cat_files = a.categories.get(cat, CategoryResult("", "")).files
                    if cat_files:
                        impacts.append(f"{cat}({len(cat_files)})")
                all_reports.append(
                    f"| `{c['hash'][:8]}` | {jira_str} | {c['message'][:150]}{'...' if len(c['message']) > 150 else ''} | {', '.join(impacts)} |"
                )
            all_reports.append("")

            all_reports.append("---")
            all_reports.append("")

            # Full detailed report for each SDK-relevant commit
            # If --output-dir specified, save each report separately
            if args.output_dir:
                output_dir = Path(args.output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)

                # Save summary file
                summary_report = "\n".join(all_reports)
                summary_file = output_dir / "00-summary.md"
                summary_file.write_text(summary_report)
                print(f"Saved summary to: {summary_file}", file=sys.stderr)

                # Save individual reports
                new_count = 0
                skip_count = 0
                for i, item in enumerate(sdk_relevant_commits, 1):
                    commit = item["commit"]
                    filename = f"{commit['hash'][:12]}.md"
                    filepath = output_dir / filename

                    # Skip if report already exists
                    if filepath.exists():
                        print(f"  [{i}/{len(sdk_relevant_commits)}] Skip (exists): {filename}", file=sys.stderr)
                        skip_count += 1
                        continue

                    commit_report = []
                    commit_report.append(f"# Commit `{commit['hash'][:12]}`")
                    commit_report.append("")
                    commit_report.append(f"**Message:** {commit['message']}")
                    commit_report.append(f"**Full hash:** `{commit['hash']}`")
                    jira_ids = extract_jira_ids(commit["message"])
                    if jira_ids:
                        jira_links = ", ".join(
                            f"[{jid}](https://gooddata.atlassian.net/browse/{jid})" for jid in jira_ids
                        )
                        commit_report.append(f"**JIRA:** {jira_links}")
                    commit_report.append("")

                    # Generate full report for this commit
                    full_report = generate_markdown_report(item["analysis"], str(repo_path))
                    # Skip the header (first few lines) since we added our own
                    lines = full_report.split("\n")
                    start_idx = next((idx for idx, line in enumerate(lines) if line.startswith("## Summary")), 0)
                    commit_report.extend(lines[start_idx:])

                    # Save to file
                    filepath.write_text("\n".join(commit_report))
                    print(f"  [{i}/{len(sdk_relevant_commits)}] Saved: {filename}", file=sys.stderr)
                    new_count += 1

                print(f"\nDone! {new_count} new reports, {skip_count} skipped (already exist)", file=sys.stderr)
                print(f"Reports in: {output_dir}/", file=sys.stderr)
                sys.exit(0)

            # Otherwise, build combined report
            for i, item in enumerate(sdk_relevant_commits, 1):
                commit = item["commit"]
                all_reports.append(f"# [{i}/{len(sdk_relevant_commits)}] Commit `{commit['hash'][:12]}`")
                all_reports.append("")
                all_reports.append(f"**Message:** {commit['message']}")
                all_reports.append("")

                # Generate full report for this commit
                full_report = generate_markdown_report(item["analysis"], str(repo_path))
                # Skip the header (first few lines) since we added our own
                lines = full_report.split("\n")
                start_idx = next((idx for idx, line in enumerate(lines) if line.startswith("## Summary")), 0)
                all_reports.extend(lines[start_idx:])
                all_reports.append("")
                all_reports.append("---")
                all_reports.append("")

            report = "\n".join(all_reports)

        # Per-commit analysis
        elif args.per_commit:
            sdk_relevant_commits = []

            for i, commit in enumerate(commits, 1):
                print(f"Analyzing commit {i}/{len(commits)}: {commit['hash'][:12]}...", file=sys.stderr)

                analysis = analyze_diff(commit["hash"], str(repo_path))

                # Check if SDK-relevant
                has_sdk_changes = any(
                    analysis.categories.get(cat, CategoryResult("", "")).files
                    for cat in ["openapi_specs", "controllers", "models", "api_examples"]
                )

                if has_sdk_changes:
                    sdk_relevant_commits.append({"commit": commit, "analysis": analysis})

            # With --sdk-only, exit if no SDK-relevant commits
            if args.sdk_only and not sdk_relevant_commits:
                print(f"No SDK-relevant changes found in {len(commits)} commits since {args.since}", file=sys.stderr)
                sys.exit(0)

            # Build report
            all_reports = []
            all_reports.append("# GDC-NAS Multi-Commit Analysis")
            all_reports.append("")

            if args.sdk_only:
                all_reports.append(
                    f"**SDK-relevant commits:** {len(sdk_relevant_commits)} (of {len(commits)} total since `{args.since}`)"
                )
            else:
                all_reports.append(f"**Commits analyzed:** {len(commits)} (since `{args.since}`)")

            all_reports.append("")
            all_reports.append("---")
            all_reports.append("")

            # Summary of SDK-relevant commits
            all_reports.append("## Summary: SDK-Relevant Commits")
            all_reports.append("")

            if sdk_relevant_commits:
                all_reports.append(f"**{len(sdk_relevant_commits)} of {len(commits)} commits** require SDK attention:")
                all_reports.append("")
                for item in sdk_relevant_commits:
                    c = item["commit"]
                    all_reports.append(f"- `{c['hash'][:12]}` - {c['message']}")
                all_reports.append("")
            else:
                all_reports.append("*No SDK-relevant changes found in any commit.*")
                all_reports.append("")

            all_reports.append("---")
            all_reports.append("")

            # With --sdk-only, only show SDK-relevant commits
            # Without --sdk-only, show all commits
            commits_to_show = (
                sdk_relevant_commits
                if args.sdk_only
                else [{"commit": c, "analysis": analyze_diff(c["hash"], str(repo_path))} for c in commits]
                if not args.sdk_only
                else sdk_relevant_commits
            )

            # Re-analyze if needed (for non-sdk-only mode we need all analyses)
            if not args.sdk_only:
                commits_to_show = []
                for commit in commits:
                    analysis = analyze_diff(commit["hash"], str(repo_path))
                    commits_to_show.append({"commit": commit, "analysis": analysis})

            for i, item in enumerate(commits_to_show, 1):
                commit = item["commit"]
                analysis = item["analysis"]

                all_reports.append(f"## Commit {i}: `{commit['hash'][:12]}`")
                all_reports.append("")
                all_reports.append(f"**Message:** {commit['message']}")
                all_reports.append("")
                all_reports.append(
                    f"**Files:** {analysis.total_files} | **+{analysis.total_additions}/-{analysis.total_deletions}**"
                )

                # Show SDK-relevant changes
                sdk_cats = []
                for cat_name in ["openapi_specs", "controllers", "models", "api_examples"]:
                    cat = analysis.categories.get(cat_name, CategoryResult("", ""))
                    if cat.files:
                        sdk_cats.append(f"{cat_name} ({len(cat.files)})")

                if sdk_cats:
                    all_reports.append("")
                    all_reports.append(f"**🔴 SDK Impact:** {', '.join(sdk_cats)}")

                    # With --sdk-only, show more details
                    if args.sdk_only:
                        for cat_name in ["openapi_specs", "controllers", "models", "api_examples"]:
                            cat = analysis.categories.get(cat_name, CategoryResult("", ""))
                            if cat.files:
                                all_reports.append("")
                                all_reports.append(f"*{cat_name}:*")
                                for f in cat.files:
                                    all_reports.append(f"  - `{f.path}`")

                all_reports.append("")
                all_reports.append("---")
                all_reports.append("")

            report = "\n".join(all_reports)
        else:
            # Combined diff analysis (default for --since)
            commit_range = f"{args.since}..HEAD"
            analysis = analyze_diff(commit_range, str(repo_path), track_commits=args.show_commits)
            report = generate_markdown_report(analysis, str(repo_path))

            # Add commit list to the report
            commit_list = [f"## Commits Included ({len(commits)})", ""]
            for commit in commits:
                commit_list.append(f"- `{commit['hash'][:12]}` - {commit['message']}")
            commit_list.append("")

            # Insert after summary
            lines = report.split("\n")
            insert_pos = next(
                (i for i, line in enumerate(lines) if line.startswith("## Changes by Category")), len(lines)
            )
            lines = lines[:insert_pos] + commit_list + lines[insert_pos:]
            report = "\n".join(lines)
    else:
        # Standard single commit/range analysis
        # Enable commit tracking for ranges (contains ..)
        track = args.show_commits and ".." in args.commit_range
        analysis = analyze_diff(args.commit_range, str(repo_path), track_commits=track)
        report = generate_markdown_report(analysis, str(repo_path))

    # Check for SDK-relevant changes if --sdk-only flag is set
    def has_sdk_relevant_changes(analysis: DiffAnalysis) -> bool:
        """Check if analysis contains any SDK-relevant file changes."""
        sdk_categories = ["openapi_specs", "controllers", "models", "api_examples"]
        return any(analysis.categories.get(cat, CategoryResult("", "")).files for cat in sdk_categories)

    # For --per-commit mode, we already filtered in the loop above
    # For other modes, check if we should skip output
    if args.sdk_only and not args.per_commit:
        if args.since:
            # For --since mode, check the combined analysis
            combined_analysis = analyze_diff(f"{args.since}..HEAD", str(repo_path))
            if not has_sdk_relevant_changes(combined_analysis):
                print(f"No SDK-relevant changes found since {args.since}", file=sys.stderr)
                sys.exit(0)
        else:
            # For single commit/range mode
            if not has_sdk_relevant_changes(analysis):
                print(f"No SDK-relevant changes found in {args.commit_range}", file=sys.stderr)
                sys.exit(0)

    # Output
    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
