#!/usr/bin/env python3
# (C) 2025 GoodData Corporation
"""
GDC-NAS API-based Diff Analyzer

Analyzes gdc-nas repository changes using GitHub API (no clone required).
Identifies changes that may require updates to gooddata-python-sdk.

Usage:
    # Analyze last N commits
    python gdc_nas_api_analyzer.py --commits 50 --output-dir ./reports

    # Analyze since a specific commit
    python gdc_nas_api_analyzer.py --since abc123 --output-dir ./reports

    # List commits only (dry run)
    python gdc_nas_api_analyzer.py --commits 50 --list-only

Requires:
    - gh CLI installed and authenticated
    - Read access to gooddata/gdc-nas repository
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

SDK_RELEVANT_PATTERNS = {
    "openapi_specs": {
        "description": "OpenAPI specifications - CRITICAL for Python SDK generation",
        "patterns": [
            r"microservices/[^/]+/src/test/resources/openapi/open-api-spec\.json$",
            r".*/openapi/.*\.json$",
            r".*/openapi/.*\.ya?ml$",
        ],
        "priority": 0,
        "critical": True,
    },
    "controllers": {
        "description": "REST API endpoint definitions",
        "patterns": [
            r"microservices/[^/]+/src/main/kotlin/.*[Cc]ontroller\.kt$",
            r"microservices/[^/]+/src/main/kotlin/controller/.*\.kt$",
        ],
        "priority": 1,
        "critical": False,
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
        "critical": False,
    },
    "api_examples": {
        "description": "API request/response examples for SDK testing",
        "patterns": [
            r"microservices/[^/]+/src/test/resources/metadata/.*\.json$",
            r"microservices/[^/]+/src/test/resources/.*[Rr]equest.*\.json$",
            r"microservices/[^/]+/src/test/resources/.*[Rr]esponse.*\.json$",
        ],
        "priority": 2,
        "critical": False,
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
    patch: str = ""  # The actual diff content


@dataclass
class CommitAnalysis:
    """Analysis of a single commit."""

    sha: str
    message: str
    author: str
    date: str
    files: list[FileChange] = field(default_factory=list)
    sdk_relevant: bool = False
    categories: dict[str, list[FileChange]] = field(default_factory=dict)
    services: set[str] = field(default_factory=set)


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


def get_commits(repo: str, count: int = 50, since_sha: str | None = None) -> list[dict]:
    """Fetch recent commits from the repository."""
    print(f"Fetching commits from {repo}...", file=sys.stderr)

    if since_sha:
        # Get commits since a specific SHA using compare
        endpoint = f"repos/{repo}/compare/{since_sha}...HEAD"
        data = gh_api(endpoint)
        if data and "commits" in data:
            return data["commits"]
        return []
    else:
        # Get last N commits
        endpoint = f"repos/{repo}/commits?per_page={count}"
        commits = gh_api(endpoint)
        return commits if commits else []


def get_commit_details(repo: str, sha: str) -> dict | None:
    """Fetch detailed commit info including files changed."""
    endpoint = f"repos/{repo}/commits/{sha}"
    return gh_api(endpoint)


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================


def categorize_file(path: str) -> str | None:
    """Determine which SDK-relevant category a file belongs to."""
    for category, info in SDK_RELEVANT_PATTERNS.items():
        for pattern in info["patterns"]:
            if re.search(pattern, path):
                return category
    return None


def extract_service(path: str) -> str | None:
    """Extract microservice name from path."""
    match = re.match(r"microservices/([^/]+)/", path)
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


def analyze_commit(repo: str, commit_data: dict) -> CommitAnalysis:
    """Analyze a single commit for SDK relevance."""
    sha = commit_data["sha"]
    message = commit_data["commit"]["message"].split("\n")[0]  # First line only
    author = commit_data["commit"]["author"]["name"]
    date = commit_data["commit"]["author"]["date"]

    analysis = CommitAnalysis(
        sha=sha,
        message=message,
        author=author,
        date=date,
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

        # Check if SDK-relevant
        category = categorize_file(file_change.path)
        if category:
            analysis.sdk_relevant = True
            if category not in analysis.categories:
                analysis.categories[category] = []
            analysis.categories[category].append(file_change)

        # Track services
        service = extract_service(file_change.path)
        if service:
            analysis.services.add(service)

    return analysis


# =============================================================================
# REPORT GENERATION
# =============================================================================


def generate_summary_report(
    commits: list[CommitAnalysis],
    repo: str,
    latest_sha: str,
) -> str:
    """Generate the summary markdown report."""
    sdk_commits = [c for c in commits if c.sdk_relevant]

    lines = [
        "# GDC-NAS SDK-Relevant Changes Report",
        "",
        f"**Repository:** `{repo}`",
        f"**Commits scanned:** {len(commits)}",
        f"**SDK-relevant:** {len(sdk_commits)}",
        f"**Latest commit:** `{latest_sha[:12]}`",
        "",
    ]

    if not sdk_commits:
        lines.append("*No SDK-relevant changes detected.*")
        return "\n".join(lines)

    # Summary table
    lines.extend(
        [
            "## Summary",
            "",
            "| Commit | JIRA | Message | Categories |",
            "|--------|------|---------|------------|",
        ]
    )

    for commit in sdk_commits:
        jira_ids = extract_jira_ids(commit.message)
        jira_str = ", ".join(jira_ids) if jira_ids else "-"
        categories = ", ".join(commit.categories.keys())
        msg = commit.message[:80] + "..." if len(commit.message) > 80 else commit.message
        lines.append(f"| `{commit.sha[:8]}` | {jira_str} | {msg} | {categories} |")

    lines.append("")

    # Category breakdown
    lines.extend(["## Categories", ""])

    category_totals: dict[str, int] = {}
    for commit in sdk_commits:
        for cat in commit.categories:
            category_totals[cat] = category_totals.get(cat, 0) + 1

    for cat, count in sorted(category_totals.items(), key=lambda x: SDK_RELEVANT_PATTERNS[x[0]]["priority"]):
        info = SDK_RELEVANT_PATTERNS[cat]
        critical = "🔴 CRITICAL" if info["critical"] else "🟡 REVIEW"
        lines.append(f"- **{cat}** ({count} commits) - {critical}: {info['description']}")

    lines.append("")

    return "\n".join(lines)


def generate_commit_report(commit: CommitAnalysis) -> str:
    """Generate detailed report for a single commit."""
    lines = [
        f"# Commit `{commit.sha[:12]}`",
        "",
        f"**Message:** {commit.message}",
        f"**Author:** {commit.author}",
        f"**Date:** {commit.date}",
        f"**Full SHA:** `{commit.sha}`",
    ]

    jira_ids = extract_jira_ids(commit.message)
    if jira_ids:
        jira_links = ", ".join(f"[{jid}](https://gooddata.atlassian.net/browse/{jid})" for jid in jira_ids)
        lines.append(f"**JIRA:** {jira_links}")

    lines.extend(["", "## SDK-Relevant Changes", ""])

    # Group by category
    for cat_name, files in sorted(commit.categories.items(), key=lambda x: SDK_RELEVANT_PATTERNS[x[0]]["priority"]):
        info = SDK_RELEVANT_PATTERNS[cat_name]
        critical = "🔴" if info["critical"] else "🟡"
        lines.extend(
            [
                f"### {critical} {cat_name.replace('_', ' ').title()}",
                "",
                f"*{info['description']}*",
                "",
            ]
        )

        for f in files:
            status_icon = {"added": "🆕", "modified": "📝", "removed": "🗑️", "renamed": "📋"}.get(f.status, "❓")
            lines.append(f"- {status_icon} `{f.path}` (+{f.additions}/-{f.deletions})")

            # Show patch for OpenAPI files (if not too large)
            if cat_name == "openapi_specs" and f.patch and len(f.patch) < 5000:
                lines.extend(
                    [
                        "",
                        "<details>",
                        "<summary>Diff (click to expand)</summary>",
                        "",
                        "```diff",
                        f.patch,
                        "```",
                        "",
                        "</details>",
                        "",
                    ]
                )

        lines.append("")

    # Services affected
    if commit.services:
        lines.extend(
            [
                "## Services Affected",
                "",
            ]
        )
        for svc in sorted(commit.services):
            lines.append(f"- {svc}")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Analyze gdc-nas changes via GitHub API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--repo",
        default="gooddata/gdc-nas",
        help="Repository to analyze (default: gooddata/gdc-nas)",
    )
    parser.add_argument(
        "--commits",
        type=int,
        default=50,
        help="Number of commits to analyze (default: 50)",
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

    # List-only mode
    if args.list_only:
        print(f"\n# Commits from {args.repo} ({len(raw_commits)} total)\n")
        for i, c in enumerate(raw_commits, 1):
            sha = c["sha"][:12]
            msg = c["commit"]["message"].split("\n")[0][:60]
            print(f"{i}. `{sha}` - {msg}")
        sys.exit(0)

    # Analyze each commit
    print("Analyzing commits for SDK relevance...", file=sys.stderr)
    analyses: list[CommitAnalysis] = []

    for i, commit_data in enumerate(raw_commits, 1):
        sha = commit_data["sha"][:12]
        print(f"  [{i}/{len(raw_commits)}] {sha}...", file=sys.stderr, end="\r")
        analysis = analyze_commit(args.repo, commit_data)
        analyses.append(analysis)

    print("", file=sys.stderr)  # Clear line

    # Filter to SDK-relevant
    sdk_analyses = [a for a in analyses if a.sdk_relevant]
    print(f"Found {len(sdk_analyses)} SDK-relevant commits", file=sys.stderr)

    if not sdk_analyses:
        print("No SDK-relevant changes found", file=sys.stderr)
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            # Still create summary for state tracking
            latest_sha = raw_commits[0]["sha"] if raw_commits else "unknown"
            summary = generate_summary_report(analyses, args.repo, latest_sha)
            (output_dir / "00-summary.md").write_text(summary)
            print(f"Summary saved to {output_dir}/00-summary.md", file=sys.stderr)
        sys.exit(0)

    # Generate reports
    latest_sha = raw_commits[0]["sha"]
    summary = generate_summary_report(analyses, args.repo, latest_sha)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save summary
        (output_dir / "00-summary.md").write_text(summary)
        print("Saved: 00-summary.md", file=sys.stderr)

        # Save individual commit reports
        for i, analysis in enumerate(sdk_analyses, 1):
            filename = f"{analysis.sha[:12]}.md"
            filepath = output_dir / filename
            if not filepath.exists():
                report = generate_commit_report(analysis)
                filepath.write_text(report)
                print(f"Saved: {filename}", file=sys.stderr)
            else:
                print(f"Skip (exists): {filename}", file=sys.stderr)

        print(f"\nReports saved to {output_dir}/", file=sys.stderr)
    else:
        # Print to stdout
        print(summary)
        print("\n---\n")
        for analysis in sdk_analyses:
            print(generate_commit_report(analysis))
            print("\n---\n")


if __name__ == "__main__":
    main()
