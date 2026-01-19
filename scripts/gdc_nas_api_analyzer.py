#!/usr/bin/env python3
# (C) 2025 GoodData Corporation
"""
GDC-NAS API-based Diff Analyzer

Analyzes gdc-nas repository changes using GitHub API (no clone required).
Identifies changes that require updates to gooddata-python-sdk.

Based on gdc-nas-diff-analyzer.py but uses GitHub API instead of local git.

Usage:
    # Analyze last N commits (default: 200)
    python gdc_nas_api_analyzer.py --commits 200 --output-dir ./reports

    # Analyze since a specific commit
    python gdc_nas_api_analyzer.py --since abc123 --output-dir ./reports

    # List commits only (dry run)
    python gdc_nas_api_analyzer.py --commits 50 --list-only

Requires:
    - gh CLI installed and authenticated
    - Read access to the target repository
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# =============================================================================
# FILE PATTERN DEFINITIONS (same as original analyzer)
# =============================================================================

FILE_CATEGORIES = {
    "openapi_specs": {
        "description": "OpenAPI specifications - CRITICAL for Python SDK generation",
        "patterns": [
            r"microservices/[^/]+/src/test/resources/openapi/open-api-spec\.json$",
            r".*/openapi/.*\.json$",
            r".*/openapi/.*\.ya?ml$",
        ],
        "priority": 0,
        "sdk_relevant": True,
    },
    "controllers": {
        "description": "REST API endpoint definitions",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/.*[Cc]ontroller\.kt$",
            r"microservices/[^/]+/src/main/kotlin/controller/.*\.kt$",
        ],
        "priority": 1,
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
        "sdk_relevant": False,
    },
    "proto_files": {
        "description": "gRPC protocol buffer definitions",
        "patterns": [
            r"proto-files/[^/]+/proto/.*\.proto$",
        ],
        "priority": 2,
        "sdk_relevant": False,
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
            r"libraries/(?!grpc/)[^/]+/src/main/kotlin/.*\.kt$",
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
            r"components/.*\.py$",
            r"components/gateway/.*",
            r"\.cursor/.*",
            r"gradle/.*",
            r"docs/.*",
        ],
        "priority": 99,
        "sdk_relevant": False,
    },
}

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
    """Represents a single file change."""

    path: str
    status: str  # added, modified, removed, renamed
    additions: int = 0
    deletions: int = 0
    patch: str = ""


@dataclass
class CommitAnalysis:
    """Analysis of a single commit."""

    sha: str
    message: str
    author: str
    date: str
    url: str = ""
    files: list[FileChange] = field(default_factory=list)
    sdk_relevant: bool = False
    categories: dict[str, list[FileChange]] = field(default_factory=dict)
    services: set[str] = field(default_factory=set)
    total_additions: int = 0
    total_deletions: int = 0


# =============================================================================
# GITHUB API FUNCTIONS
# =============================================================================


def gh_api(endpoint: str, method: str = "GET") -> dict | list | None:
    """Call GitHub API using gh CLI."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint, "--method", method],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout) if result.stdout else None
    except subprocess.CalledProcessError as e:
        print(f"API error for {endpoint}: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        return None


def get_commits(repo: str, count: int = 200, since_sha: str | None = None) -> list[dict]:
    """Fetch commits from the repository."""
    print(f"Fetching commits from {repo}...", file=sys.stderr)

    if since_sha:
        # Get commits since a specific SHA using compare
        endpoint = f"repos/{repo}/compare/{since_sha}...HEAD"
        data = gh_api(endpoint)
        if data and "commits" in data:
            return data["commits"]
        return []
    else:
        # Get last N commits (paginate if needed)
        all_commits = []
        page = 1
        per_page = min(count, 100)  # GitHub max is 100 per page

        while len(all_commits) < count:
            endpoint = f"repos/{repo}/commits?per_page={per_page}&page={page}"
            commits = gh_api(endpoint)
            if not commits:
                break
            all_commits.extend(commits)
            if len(commits) < per_page:
                break
            page += 1

        return all_commits[:count]


def get_commit_details(repo: str, sha: str) -> dict | None:
    """Fetch detailed commit info including files changed."""
    endpoint = f"repos/{repo}/commits/{sha}"
    return gh_api(endpoint)


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================


def categorize_file(path: str) -> str | None:
    """Determine which category a file belongs to."""
    for category, info in FILE_CATEGORIES.items():
        for pattern in info["patterns"]:
            if re.search(pattern, path):
                return category
    return None


def extract_service(path: str) -> str | None:
    """Extract microservice name from path."""
    match = re.match(r"microservices/([^/]+)/", path)
    if match:
        return match.group(1)
    match = re.match(r"proto-files/([^/]+)/", path)
    if match:
        return match.group(1)
    match = re.match(r"libraries/grpc/([^/]+)-client-grpc/", path)
    if match:
        return match.group(1)
    return None


def extract_jira_ids(message: str) -> list[str]:
    """Extract JIRA ticket IDs from commit message."""
    pattern = r"\b([A-Z]{2,}-\d+)\b"
    matches = re.findall(pattern, message, re.IGNORECASE)
    seen = set()
    result = []
    for m in matches:
        upper = m.upper()
        if upper not in seen:
            seen.add(upper)
            result.append(upper)
    return result


def format_jira_links(jira_ids: list[str]) -> str:
    """Format JIRA IDs as clickable markdown links."""
    if not jira_ids:
        return "-"
    return ", ".join(f"[{jid}](https://gooddata.atlassian.net/browse/{jid})" for jid in jira_ids)


def is_merge_commit(message: str) -> bool:
    """Check if commit message indicates a merge commit."""
    msg_lower = message.lower()
    return msg_lower.startswith(("merge pull request", "merge branch"))


def analyze_commit(repo: str, commit_data: dict) -> CommitAnalysis:
    """Analyze a single commit for SDK relevance."""
    sha = commit_data["sha"]
    message = commit_data["commit"]["message"].split("\n")[0]  # First line only
    author = commit_data["commit"]["author"]["name"]
    date = commit_data["commit"]["author"]["date"]
    url = commit_data.get("html_url", "")

    analysis = CommitAnalysis(
        sha=sha,
        message=message,
        author=author,
        date=date,
        url=url,
    )

    # Get detailed commit info with files
    details = get_commit_details(repo, sha)
    if not details or "files" not in details:
        return analysis

    for file_data in details["files"]:
        file_change = FileChange(
            path=file_data["filename"],
            status=file_data["status"],
            additions=file_data.get("additions", 0),
            deletions=file_data.get("deletions", 0),
            patch=file_data.get("patch", ""),
        )
        analysis.files.append(file_change)
        analysis.total_additions += file_change.additions
        analysis.total_deletions += file_change.deletions

        # Categorize file
        category = categorize_file(file_change.path)
        if category:
            if category not in analysis.categories:
                analysis.categories[category] = []
            analysis.categories[category].append(file_change)

            # Check if SDK-relevant
            if FILE_CATEGORIES[category]["sdk_relevant"]:
                analysis.sdk_relevant = True

        # Track services
        service = extract_service(file_change.path)
        if service:
            analysis.services.add(service)

    return analysis


# =============================================================================
# REPORT GENERATION
# =============================================================================


def generate_summary_report(
    all_commits: list[CommitAnalysis],
    sdk_commits: list[CommitAnalysis],
    repo: str,
    latest_sha: str,
    since_sha: str | None = None,
) -> str:
    """Generate the summary markdown report."""
    lines = [
        "# GDC-NAS SDK-Relevant Changes Report",
        "",
        f"**Repository:** `{repo}`",
        f"**Scanned:** {len(all_commits)} commits",
        f"**SDK-relevant:** {len(sdk_commits)} commits",
        f"**Latest commit analyzed:** `{latest_sha[:12]}`",
        "",
    ]

    if since_sha:
        lines.insert(3, f"**Range:** `{since_sha[:12]}..HEAD`")

    if not sdk_commits:
        lines.append("*No SDK-relevant changes detected in the analyzed commits.*")
        return "\n".join(lines)

    # Sort: merge commits (PRs) first, then others
    sorted_commits = sorted(sdk_commits, key=lambda x: (0 if is_merge_commit(x.message) else 1, x.date), reverse=True)

    # Summary table
    lines.extend(
        [
            "## Summary",
            "",
            "| Commit | JIRA | Message | Impact |",
            "|--------|------|---------|--------|",
        ]
    )

    for commit in sorted_commits:
        jira_ids = extract_jira_ids(commit.message)
        jira_str = format_jira_links(jira_ids)
        msg = commit.message[:100] + "..." if len(commit.message) > 100 else commit.message
        # Escape pipe characters in message
        msg = msg.replace("|", "\\|")

        impacts = []
        for cat in ["openapi_specs", "controllers", "models", "api_examples"]:
            if cat in commit.categories:
                impacts.append(f"{cat}({len(commit.categories[cat])})")

        lines.append(f"| [`{commit.sha[:8]}`]({commit.url}) | {jira_str} | {msg} | {', '.join(impacts)} |")

    lines.extend(["", "---", ""])

    # Category breakdown
    lines.extend(["## Impact by Category", ""])

    category_commits: dict[str, list[CommitAnalysis]] = {}
    for commit in sdk_commits:
        for cat in commit.categories:
            if FILE_CATEGORIES[cat]["sdk_relevant"]:
                if cat not in category_commits:
                    category_commits[cat] = []
                category_commits[cat].append(commit)

    for cat in ["openapi_specs", "controllers", "models", "api_examples"]:
        if cat in category_commits:
            info = FILE_CATEGORIES[cat]
            icon = "🔴" if cat == "openapi_specs" else "🟡"
            lines.append(f"### {icon} {cat.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"*{info['description']}*")
            lines.append("")
            lines.append(f"**{len(category_commits[cat])} commits** affect this category")
            lines.append("")

    # Services affected
    all_services: set[str] = set()
    for commit in sdk_commits:
        all_services.update(commit.services)

    if all_services:
        lines.extend(
            [
                "## Services Affected",
                "",
            ]
        )
        for svc in sorted(all_services):
            lines.append(f"- {svc}")
        lines.append("")

    # SDK Action Items
    lines.extend(
        [
            "## SDK Action Items",
            "",
        ]
    )

    if "openapi_specs" in category_commits:
        lines.append("1. **🔴 Regenerate API Client**: OpenAPI specs changed - run `make generate-client`")

    if "controllers" in category_commits:
        lines.append("2. **Review New Endpoints**: Check if new REST endpoints need SDK wrapper methods")

    if "models" in category_commits:
        lines.append("3. **Update Models**: Data models changed - verify SDK model mappings match")

    if "api_examples" in category_commits:
        lines.append("4. **Update Tests**: API examples changed - update SDK integration tests")

    lines.append("")

    return "\n".join(lines)


def generate_commit_report(commit: CommitAnalysis, repo: str) -> str:
    """Generate detailed report for a single commit."""
    lines = [
        f"# Commit `{commit.sha[:12]}`",
        "",
        f"**Message:** {commit.message}",
        f"**Author:** {commit.author}",
        f"**Date:** {commit.date}",
        f"**Full SHA:** [`{commit.sha}`]({commit.url})",
    ]

    jira_ids = extract_jira_ids(commit.message)
    if jira_ids:
        lines.append(f"**JIRA:** {format_jira_links(jira_ids)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- **Total Files Changed:** {len(commit.files)}",
            f"- **Lines Added:** +{commit.total_additions}",
            f"- **Lines Removed:** -{commit.total_deletions}",
            f"- **Services Impacted:** {len(commit.services)}",
            "",
        ]
    )

    # Services affected
    if commit.services:
        lines.append("### Services Affected")
        lines.append("")
        for svc in sorted(commit.services):
            lines.append(f"- **{svc}**")
        lines.append("")

    # Changes by category
    lines.extend(["## Changes by Category", ""])

    # Sort categories by priority
    sorted_cats = sorted(
        [(cat, files) for cat, files in commit.categories.items()],
        key=lambda x: FILE_CATEGORIES[x[0]]["priority"],
    )

    for cat_name, files in sorted_cats:
        info = FILE_CATEGORIES[cat_name]
        sdk_icon = "🔴" if cat_name == "openapi_specs" else ("🟡" if info["sdk_relevant"] else "")

        lines.extend(
            [
                f"### {sdk_icon} {cat_name.replace('_', ' ').title()}",
                "",
                f"*{info['description']}*",
                "",
            ]
        )

        total_add = sum(f.additions for f in files)
        total_del = sum(f.deletions for f in files)
        lines.append(f"**Files:** {len(files)} | **+{total_add}** / **-{total_del}**")
        lines.append("")

        for f in files:
            status_icon = {"added": "🆕", "modified": "📝", "removed": "🗑️", "renamed": "📋"}.get(f.status, "❓")
            lines.append(f"- {status_icon} `{f.path}` (+{f.additions}/-{f.deletions})")

        lines.append("")

        # Show patch for OpenAPI files
        if cat_name == "openapi_specs":
            for f in files:
                if f.patch and len(f.patch) < 10000:
                    lines.extend(
                        [
                            f"#### Diff: `{f.path.split('/')[-1]}`",
                            "",
                            "<details>",
                            "<summary>Click to expand diff</summary>",
                            "",
                            "```diff",
                            f.patch,
                            "```",
                            "",
                            "</details>",
                            "",
                        ]
                    )

    # Python SDK Impact section
    sdk_cats = [cat for cat in commit.categories if FILE_CATEGORIES[cat]["sdk_relevant"]]
    if sdk_cats:
        lines.extend(
            [
                "## Python SDK Impact",
                "",
            ]
        )

        if "openapi_specs" in commit.categories:
            lines.extend(
                [
                    "### 🔴 CRITICAL: OpenAPI Spec Changes",
                    "",
                    "*These changes directly affect `gooddata-api-client` generation*",
                    "",
                ]
            )

        review_cats = [c for c in sdk_cats if c != "openapi_specs"]
        if review_cats:
            lines.extend(
                [
                    "### 🟡 REVIEW: Files to Check",
                    "",
                    "*Review these files and update SDK if needed*",
                    "",
                ]
            )
            for cat in review_cats:
                lines.append(f"- **{cat}**: {len(commit.categories[cat])} file(s)")
            lines.append("")

        # Action items
        lines.extend(
            [
                "### SDK Action Items",
                "",
            ]
        )
        if "openapi_specs" in commit.categories:
            lines.append("1. **Regenerate API Client**: Run `make generate-client`")
        if "controllers" in commit.categories:
            lines.append("2. **Review New Endpoints**: Check if new REST endpoints need SDK wrapper methods")
        if "models" in commit.categories:
            lines.append("3. **Update Models**: Verify SDK model mappings match")
        if "api_examples" in commit.categories:
            lines.append("4. **Update Tests**: Update SDK integration tests")
        lines.append("")

    lines.extend(
        [
            "---",
            "*Generated by gdc-nas-api-analyzer*",
        ]
    )

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Analyze gdc-nas changes via GitHub API (no clone required)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Analyze last 200 commits (default)
    python gdc_nas_api_analyzer.py --output-dir ./reports

    # Analyze specific number of commits
    python gdc_nas_api_analyzer.py --commits 100 --output-dir ./reports

    # Analyze since a specific commit
    python gdc_nas_api_analyzer.py --since abc123 --output-dir ./reports

    # List commits only (dry run)
    python gdc_nas_api_analyzer.py --commits 50 --list-only
""",
    )
    parser.add_argument(
        "--repo",
        default="gooddata/gdc-nas",
        help="Repository to analyze (default: gooddata/gdc-nas)",
    )
    parser.add_argument(
        "--commits",
        type=int,
        default=200,
        help="Number of commits to analyze (default: 200)",
    )
    parser.add_argument(
        "--since",
        metavar="SHA",
        help="Analyze commits since this SHA (exclusive)",
    )
    parser.add_argument(
        "--output-dir",
        metavar="DIR",
        help="Save reports to this directory",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Only list commits, don't analyze",
    )

    args = parser.parse_args()

    # Fetch commits
    print(f"Fetching commits from {args.repo}...", file=sys.stderr)
    raw_commits = get_commits(args.repo, args.commits, args.since)

    if not raw_commits:
        print("No commits found", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(raw_commits)} commits", file=sys.stderr)
    latest_sha = raw_commits[0]["sha"]

    # List-only mode
    if args.list_only:
        print(f"\n# Commits from {args.repo} ({len(raw_commits)} total)\n")
        for i, c in enumerate(raw_commits, 1):
            sha = c["sha"][:12]
            msg = c["commit"]["message"].split("\n")[0][:60]
            jira_ids = extract_jira_ids(c["commit"]["message"])
            jira_str = f" [{', '.join(jira_ids)}]" if jira_ids else ""
            print(f"{i}. `{sha}` - {msg}{jira_str}")
        sys.exit(0)

    # Analyze each commit
    print(f"Scanning {len(raw_commits)} commits for SDK-relevant changes...", file=sys.stderr)
    all_analyses: list[CommitAnalysis] = []
    sdk_analyses: list[CommitAnalysis] = []

    for i, commit_data in enumerate(raw_commits, 1):
        sha = commit_data["sha"][:12]
        print(f"  [{i}/{len(raw_commits)}] {sha}...", file=sys.stderr, end="\r")
        analysis = analyze_commit(args.repo, commit_data)
        all_analyses.append(analysis)
        if analysis.sdk_relevant:
            sdk_analyses.append(analysis)

    print(f"\nFound {len(sdk_analyses)} SDK-relevant commits", file=sys.stderr)

    # Generate reports
    summary = generate_summary_report(all_analyses, sdk_analyses, args.repo, latest_sha, args.since)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save summary
        (output_dir / "00-summary.md").write_text(summary)
        print("Saved: 00-summary.md", file=sys.stderr)

        # Save individual commit reports
        new_count = 0
        skip_count = 0
        for i, analysis in enumerate(sdk_analyses, 1):
            filename = f"{analysis.sha[:12]}.md"
            filepath = output_dir / filename
            if not filepath.exists():
                report = generate_commit_report(analysis, args.repo)
                filepath.write_text(report)
                print(f"  [{i}/{len(sdk_analyses)}] Saved: {filename}", file=sys.stderr)
                new_count += 1
            else:
                print(f"  [{i}/{len(sdk_analyses)}] Skip (exists): {filename}", file=sys.stderr)
                skip_count += 1

        print(f"\nDone! {new_count} new reports, {skip_count} skipped (already exist)", file=sys.stderr)
        print(f"Reports in: {output_dir}/", file=sys.stderr)
    else:
        # Print to stdout
        print(summary)
        if sdk_analyses:
            print("\n" + "=" * 80 + "\n")
            for analysis in sdk_analyses:
                print(generate_commit_report(analysis, args.repo))
                print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
