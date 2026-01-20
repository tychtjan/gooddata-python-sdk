#!/usr/bin/env python3
# (C) 2024 GoodData Corporation
"""
Cluster SDK diff reports by similarity to enable batch processing.

Groups similar commits together so agents can handle multiple related changes
in a single run instead of processing each commit separately.

Clustering strategies:
1. Heuristic-based (default): Groups by JIRA ticket, services, change types
2. Claude-enhanced (optional): Uses Claude API for semantic similarity analysis

Usage:
    # Heuristic clustering only
    python cluster_sdk_reports.py --input-dir ./reports --output-dir ./clustered

    # With Claude enhancement (requires ANTHROPIC_API_KEY env var)
    python cluster_sdk_reports.py --input-dir ./reports --output-dir ./clustered --use-claude
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReportMetadata:
    """Extracted metadata from a report for clustering."""

    filename: str
    commit_sha: str
    message: str
    jira_tickets: list[str]
    services: list[str]
    change_categories: list[str]
    openapi_changes: dict  # endpoints added/removed/modified, schemas changed
    proto_changes: list[str]
    files_changed: list[str]
    impact_level: str  # critical, high, medium, low

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "commit_sha": self.commit_sha,
            "message": self.message,
            "jira_tickets": self.jira_tickets,
            "services": self.services,
            "change_categories": self.change_categories,
            "openapi_changes": self.openapi_changes,
            "proto_changes": self.proto_changes,
            "impact_level": self.impact_level,
        }


@dataclass
class Cluster:
    """A cluster of similar reports."""

    cluster_id: str
    name: str
    description: str
    reports: list[ReportMetadata]
    merge_rationale: str
    suggested_action: str
    priority: int = 1  # 1 = highest priority

    def to_dict(self) -> dict:
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "description": self.description,
            "reports": [r.to_dict() for r in self.reports],
            "merge_rationale": self.merge_rationale,
            "suggested_action": self.suggested_action,
            "priority": self.priority,
        }


def parse_report(report_path: Path) -> ReportMetadata | None:
    """Parse a markdown report and extract metadata for clustering."""
    content = report_path.read_text()

    # Skip summary file
    if report_path.name == "00-summary.md":
        return None

    # Extract commit SHA from filename or content
    commit_sha = report_path.stem
    sha_match = re.search(r"Full SHA.*`([a-f0-9]{40})`", content)
    if sha_match:
        commit_sha = sha_match.group(1)[:12]

    # Extract commit message
    msg_match = re.search(r"\*\*Message:\*\* (.+)", content)
    message = msg_match.group(1) if msg_match else ""

    # Extract JIRA tickets
    jira_pattern = r"\[([A-Z]+-\d+)\]"
    jira_tickets = list(set(re.findall(jira_pattern, content)))

    # Extract services affected
    services = []
    services_match = re.search(r"### Services Affected\n\n((?:- \*\*.+\*\*\n?)+)", content)
    if services_match:
        services = re.findall(r"\*\*([^*]+)\*\*", services_match.group(1))

    # Determine change categories
    change_categories = []
    category_patterns = [
        (r"### 🔴 Openapi Specs", "openapi_specs"),
        (r"### 🟡 Controllers", "controllers"),
        (r"### 🟡 Models", "models"),
        (r"###  Proto Files", "proto_files"),
        (r"###  Api Examples", "api_examples"),
        (r"###  Grpc Clients", "grpc_clients"),
    ]
    for pattern, category in category_patterns:
        if re.search(pattern, content):
            change_categories.append(category)

    # Extract OpenAPI changes
    openapi_changes = {
        "endpoints_added": [],
        "endpoints_removed": [],
        "endpoints_modified": [],
        "schemas_added": [],
        "schemas_removed": [],
        "schemas_modified": [],
    }

    # Parse endpoint changes
    endpoint_section = re.search(r"\*\*Endpoint Changes:\*\*(.+?)(?=\*\*Schema Changes:|###|$)", content, re.DOTALL)
    if endpoint_section:
        section = endpoint_section.group(1)
        openapi_changes["endpoints_added"] = re.findall(r"➕ `([^`]+)`", section)
        openapi_changes["endpoints_removed"] = re.findall(r"➖ `([^`]+)`", section)
        openapi_changes["endpoints_modified"] = re.findall(r"~️ `([^`]+)`", section)

    # Parse schema changes
    schema_section = re.search(r"\*\*Schema Changes:\*\*(.+?)(?=###|$)", content, re.DOTALL)
    if schema_section:
        section = schema_section.group(1)
        openapi_changes["schemas_added"] = re.findall(r"➕ `([^`]+)`", section)
        openapi_changes["schemas_removed"] = re.findall(r"➖ `([^`]+)`", section)
        openapi_changes["schemas_modified"] = re.findall(r"~️ `([^`]+)`", section)

    # Extract proto changes
    proto_changes = []
    proto_section = re.search(r"## Proto Changes\n\n((?:- .+\n?)+)", content)
    if proto_section:
        proto_changes = re.findall(r"- (.+)", proto_section.group(1))

    # Extract changed files
    files_changed = re.findall(r"[📝🆕] `([^`]+)`", content)

    # Determine impact level
    if "openapi_specs" in change_categories:
        impact_level = "critical"
    elif "controllers" in change_categories or "models" in change_categories:
        impact_level = "high"
    elif "proto_files" in change_categories:
        impact_level = "medium"
    else:
        impact_level = "low"

    return ReportMetadata(
        filename=report_path.name,
        commit_sha=commit_sha,
        message=message,
        jira_tickets=jira_tickets,
        services=services,
        change_categories=change_categories,
        openapi_changes=openapi_changes,
        proto_changes=proto_changes,
        files_changed=files_changed,
        impact_level=impact_level,
    )


def heuristic_cluster(reports: list[ReportMetadata]) -> list[Cluster]:
    """
    Cluster reports using heuristic rules.

    Each report is assigned to exactly ONE cluster (the highest priority match).

    Clustering priority:
    1. Same JIRA ticket (strongest signal)
    2. Same OpenAPI spec file modified
    3. Same service + same change type (using primary service only)
    4. Related proto files
    5. Singleton (no cluster match)
    """
    clusters: list[Cluster] = []
    used_reports: set[str] = set()

    # Strategy 1: Group by JIRA ticket
    jira_groups: dict[str, list[ReportMetadata]] = defaultdict(list)
    for report in reports:
        for ticket in report.jira_tickets:
            jira_groups[ticket].append(report)

    for ticket, group in jira_groups.items():
        # Filter out already-used reports
        unique_group = [r for r in group if r.filename not in used_reports]
        if len(unique_group) > 1:
            cluster_id = f"jira-{ticket.lower()}"
            clusters.append(
                Cluster(
                    cluster_id=cluster_id,
                    name=f"JIRA {ticket} Changes",
                    description=f"All commits related to {ticket}",
                    reports=unique_group,
                    merge_rationale=f"These {len(unique_group)} commits are all part of the same JIRA ticket {ticket}",
                    suggested_action=f"Review and implement SDK changes for {ticket} as a single unit",
                    priority=1,
                )
            )
            for r in unique_group:
                used_reports.add(r.filename)

    # Strategy 2: Group by OpenAPI spec file
    openapi_groups: dict[str, list[ReportMetadata]] = defaultdict(list)
    for report in reports:
        if report.filename in used_reports:
            continue
        for f in report.files_changed:
            if "openapi" in f.lower() and f.endswith(".json"):
                # Normalize to service name
                service_match = re.search(r"microservices/([^/]+)/", f)
                if service_match:
                    openapi_groups[service_match.group(1)].append(report)
                    break  # Only assign to first matching service

    for service, group in openapi_groups.items():
        # Filter out already-used reports
        unique_group = [r for r in group if r.filename not in used_reports]
        if len(unique_group) > 1:
            cluster_id = f"openapi-{service}"
            clusters.append(
                Cluster(
                    cluster_id=cluster_id,
                    name=f"{service} OpenAPI Changes",
                    description=f"Multiple commits modifying {service} OpenAPI spec",
                    reports=unique_group,
                    merge_rationale=f"These {len(unique_group)} commits all modify the {service} service OpenAPI specification",
                    suggested_action=f"Regenerate API client once after all {service} changes are reviewed",
                    priority=2,
                )
            )
            for r in unique_group:
                used_reports.add(r.filename)

    # Strategy 3: Group by PRIMARY service + PRIMARY change type
    # Each report is only assigned to ONE service:change_type group
    service_type_groups: dict[str, list[ReportMetadata]] = defaultdict(list)
    for report in reports:
        if report.filename in used_reports:
            continue
        # Use primary service (first) and primary change type (first/most important)
        if report.services and report.change_categories:
            primary_service = report.services[0]
            # Prioritize: openapi_specs > controllers > models > others
            change_priority = ["openapi_specs", "controllers", "models", "proto_files"]
            primary_change = report.change_categories[0]
            for cp in change_priority:
                if cp in report.change_categories:
                    primary_change = cp
                    break
            key = f"{primary_service}:{primary_change}"
            service_type_groups[key].append(report)

    for key, group in service_type_groups.items():
        # Filter out already-used reports
        unique_group = [r for r in group if r.filename not in used_reports]
        if len(unique_group) > 1:
            service, change_type = key.split(":")
            cluster_id = f"service-{service}-{change_type}"
            clusters.append(
                Cluster(
                    cluster_id=cluster_id,
                    name=f"{service} {change_type.replace('_', ' ').title()}",
                    description=f"Multiple commits with {change_type} changes in {service}",
                    reports=unique_group,
                    merge_rationale=f"These {len(unique_group)} commits all affect {change_type} in the {service} service",
                    suggested_action=f"Review {change_type} changes in {service} together for consistency",
                    priority=3,
                )
            )
            for r in unique_group:
                used_reports.add(r.filename)

    # Strategy 4: Group proto file changes
    proto_groups: list[ReportMetadata] = []
    for report in reports:
        if report.filename in used_reports:
            continue
        if report.proto_changes:
            proto_groups.append(report)

    if len(proto_groups) > 1:
        clusters.append(
            Cluster(
                cluster_id="proto-changes",
                name="Proto File Changes",
                description="Commits modifying gRPC protocol buffers",
                reports=proto_groups,
                merge_rationale=f"These {len(proto_groups)} commits all modify proto files",
                suggested_action="Regenerate proto stubs and review gRPC client changes together",
                priority=4,
            )
        )
        for r in proto_groups:
            used_reports.add(r.filename)

    # Remaining unclustered reports become singletons
    for report in reports:
        if report.filename not in used_reports:
            clusters.append(
                Cluster(
                    cluster_id=f"single-{report.commit_sha}",
                    name=f"Commit {report.commit_sha}",
                    description=report.message[:100],
                    reports=[report],
                    merge_rationale="Standalone commit with unique changes",
                    suggested_action="Review individually",
                    priority=5,
                )
            )

    return clusters


def claude_review_clusters(
    clusters: list[Cluster],
    reports_dir: Path,
    api_key: str,
) -> tuple[list[Cluster], str]:
    """
    Use Claude to critically review the proposed clustering.

    Claude acts as a devil's advocate:
    1. Reads FULL report content (not just metadata)
    2. Questions whether groupings make semantic sense
    3. Identifies false positives (unrelated commits grouped together)
    4. Identifies false negatives (related commits in separate clusters)
    5. Provides reasoning for each recommendation

    Returns:
        tuple: (revised_clusters, review_report_markdown)
    """
    try:
        import anthropic
    except ImportError:
        print("Warning: anthropic package not installed, skipping Claude review")
        return clusters, ""

    client = anthropic.Anthropic(api_key=api_key)

    # Read full report content for each report
    report_contents = {}
    for cluster in clusters:
        for report in cluster.reports:
            report_path = reports_dir / report.filename
            if report_path.exists():
                content = report_path.read_text()
                # Truncate very long reports to avoid token limits
                if len(content) > 8000:
                    content = content[:8000] + "\n\n[... truncated for length ...]"
                report_contents[report.filename] = content

    # Build the clustering proposal for Claude to review
    clustering_proposal = []
    for c in clusters:
        cluster_info = {
            "cluster_id": c.cluster_id,
            "name": c.name,
            "heuristic_rationale": c.merge_rationale,
            "reports": [],
        }
        for r in c.reports:
            cluster_info["reports"].append(
                {
                    "filename": r.filename,
                    "commit_sha": r.commit_sha,
                    "message": r.message,
                    "jira_tickets": r.jira_tickets,
                    "services": r.services,
                    "change_categories": r.change_categories,
                    "impact_level": r.impact_level,
                }
            )
        clustering_proposal.append(cluster_info)

    # Build the full reports section
    reports_section = ""
    for filename, content in report_contents.items():
        reports_section += f"\n\n{'=' * 60}\nREPORT: {filename}\n{'=' * 60}\n{content}"

    prompt = f"""You are a critical code reviewer analyzing SDK change report clustering.

## Your Role
Act as a DEVIL'S ADVOCATE. Your job is to find problems with the proposed clustering:
- Are commits grouped together that shouldn't be?
- Are commits separated that should be together?
- Does the clustering actually help, or does it obscure important differences?

## Context
These reports describe changes in gdc-nas (backend) that may require updates to gooddata-python-sdk.
The goal is to group related changes so an agent can process them in a single run instead of separately.

## Proposed Clustering (by heuristics)
{json.dumps(clustering_proposal, indent=2)}

## Full Report Contents
{reports_section}

## Your Task

1. **Review each cluster critically:**
   - Read the ACTUAL report content, not just metadata
   - Ask: "Do these commits REALLY belong together?"
   - Look for semantic differences that heuristics missed
   - Consider: Would processing these together help or hurt?

2. **Identify problems:**
   - FALSE POSITIVES: Commits grouped together but actually unrelated
     (e.g., same service but completely different features)
   - FALSE NEGATIVES: Commits in different clusters but actually related
     (e.g., different services but same feature/JIRA epic)
   - OVER-CLUSTERING: Too many commits in one cluster, losing important nuance
   - UNDER-CLUSTERING: Singletons that could be merged

3. **Make recommendations:**
   - APPROVE: Cluster is good as-is
   - SPLIT: Break cluster into smaller groups (explain why)
   - MERGE: Combine clusters (explain the connection)
   - REASSIGN: Move specific report(s) to different cluster

Respond in JSON format:
{{
  "overall_assessment": "Brief summary of clustering quality (good/needs-work/poor)",
  "concerns": ["List of main concerns about the current clustering"],
  "cluster_reviews": [
    {{
      "cluster_id": "id",
      "verdict": "APPROVE|SPLIT|MERGE|REASSIGN",
      "confidence": "high|medium|low",
      "reasoning": "Detailed explanation of your assessment",
      "issues_found": ["Specific problems identified"],
      "recommendation": {{
        "action": "keep|split|merge|reassign",
        "details": "What exactly should change",
        "new_groups": [  // Only for split/reassign
          {{
            "name": "New cluster name",
            "reports": ["filename1.md", "filename2.md"],
            "rationale": "Why these belong together"
          }}
        ],
        "merge_with": "other_cluster_id",  // Only for merge
        "priority": 1
      }}
    }}
  ],
  "missed_connections": [  // Reports that should be grouped but aren't
    {{
      "reports": ["file1.md", "file2.md"],
      "connection": "Why these are related",
      "suggested_cluster_name": "Name for new cluster"
    }}
  ],
  "final_recommendations": [
    "Actionable recommendation 1",
    "Actionable recommendation 2"
  ]
}}"""

    try:
        print("  Sending reports to Claude for critical review...")
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = response.content[0].text

        # Extract JSON from response
        json_match = re.search(r"\{[\s\S]+\}", response_text)
        if not json_match:
            print("  Warning: Could not parse Claude response")
            return clusters, f"## Claude Review\n\nFailed to parse response:\n```\n{response_text[:1000]}\n```"

        review = json.loads(json_match.group())

        # Generate review report markdown
        review_md = generate_review_report(review)

        print(f"  Assessment: {review.get('overall_assessment', 'N/A')}")
        if review.get("concerns"):
            print(f"  Concerns: {len(review['concerns'])} identified")

        # Apply recommendations
        revised_clusters = apply_claude_recommendations(clusters, review, reports_dir)

        return revised_clusters, review_md

    except Exception as e:
        print(f"  Warning: Claude API error: {e}")
        return clusters, f"## Claude Review\n\nAPI Error: {e}"


def generate_review_report(review: dict) -> str:
    """Generate a markdown report from Claude's review."""
    lines = [
        "# Claude Clustering Review",
        "",
        f"**Overall Assessment:** {review.get('overall_assessment', 'N/A')}",
        "",
    ]

    # Concerns
    concerns = review.get("concerns", [])
    if concerns:
        lines.append("## Concerns Identified")
        lines.append("")
        for concern in concerns:
            lines.append(f"- ⚠️ {concern}")
        lines.append("")

    # Cluster reviews
    cluster_reviews = review.get("cluster_reviews", [])
    if cluster_reviews:
        lines.append("## Cluster-by-Cluster Review")
        lines.append("")
        for cr in cluster_reviews:
            verdict = cr.get("verdict", "UNKNOWN")
            verdict_icon = {"APPROVE": "✅", "SPLIT": "✂️", "MERGE": "🔗", "REASSIGN": "↔️"}.get(verdict, "❓")
            confidence = cr.get("confidence", "unknown")

            lines.append(f"### {verdict_icon} `{cr.get('cluster_id', 'unknown')}`")
            lines.append("")
            lines.append(f"**Verdict:** {verdict} (confidence: {confidence})")
            lines.append("")
            lines.append(f"**Reasoning:** {cr.get('reasoning', 'N/A')}")
            lines.append("")

            issues = cr.get("issues_found", [])
            if issues:
                lines.append("**Issues:**")
                for issue in issues:
                    lines.append(f"- {issue}")
                lines.append("")

            rec = cr.get("recommendation", {})
            if rec.get("details"):
                lines.append(f"**Recommendation:** {rec['details']}")
                lines.append("")

    # Missed connections
    missed = review.get("missed_connections", [])
    if missed:
        lines.append("## Missed Connections")
        lines.append("")
        lines.append("Reports that should potentially be grouped together:")
        lines.append("")
        for m in missed:
            lines.append(f"- **{m.get('suggested_cluster_name', 'Unknown')}**")
            lines.append(f"  - Reports: {', '.join(m.get('reports', []))}")
            lines.append(f"  - Connection: {m.get('connection', 'N/A')}")
        lines.append("")

    # Final recommendations
    final_recs = review.get("final_recommendations", [])
    if final_recs:
        lines.append("## Final Recommendations")
        lines.append("")
        for i, rec in enumerate(final_recs, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    lines.append("---")
    lines.append("*Review generated by Claude*")

    return "\n".join(lines)


def apply_claude_recommendations(
    clusters: list[Cluster],
    review: dict,
    reports_dir: Path,
) -> list[Cluster]:
    """Apply Claude's recommendations to revise the clustering."""
    cluster_map = {c.cluster_id: c for c in clusters}
    report_map = {}
    for c in clusters:
        for r in c.reports:
            report_map[r.filename] = r

    revised_clusters = []
    processed_cluster_ids = set()
    processed_report_files = set()

    # Process cluster reviews
    for cr in review.get("cluster_reviews", []):
        cluster_id = cr.get("cluster_id")
        if cluster_id not in cluster_map:
            continue

        verdict = cr.get("verdict", "APPROVE")
        rec = cr.get("recommendation", {})
        original_cluster = cluster_map[cluster_id]

        if verdict == "APPROVE" or rec.get("action") == "keep":
            # Keep cluster as-is, maybe update priority
            if rec.get("priority"):
                original_cluster.priority = rec["priority"]
            revised_clusters.append(original_cluster)
            processed_cluster_ids.add(cluster_id)
            for r in original_cluster.reports:
                processed_report_files.add(r.filename)

        elif verdict == "SPLIT" and rec.get("new_groups"):
            # Split into new groups
            processed_cluster_ids.add(cluster_id)
            for i, new_group in enumerate(rec["new_groups"]):
                group_reports = []
                for fname in new_group.get("reports", []):
                    if fname in report_map:
                        group_reports.append(report_map[fname])
                        processed_report_files.add(fname)

                if group_reports:
                    revised_clusters.append(
                        Cluster(
                            cluster_id=f"claude-split-{cluster_id}-{i}",
                            name=new_group.get("name", f"Split from {cluster_id}"),
                            description=new_group.get("rationale", ""),
                            reports=group_reports,
                            merge_rationale=f"Claude split from {cluster_id}: {new_group.get('rationale', '')}",
                            suggested_action=original_cluster.suggested_action,
                            priority=rec.get("priority", original_cluster.priority),
                        )
                    )

        elif verdict == "MERGE" and rec.get("merge_with"):
            # Will be handled when processing the target cluster
            pass

    # Handle merges
    for cr in review.get("cluster_reviews", []):
        if cr.get("verdict") == "MERGE":
            cluster_id = cr.get("cluster_id")
            merge_with = cr.get("recommendation", {}).get("merge_with")

            if cluster_id in processed_cluster_ids or merge_with in processed_cluster_ids:
                continue

            if cluster_id in cluster_map and merge_with in cluster_map:
                c1 = cluster_map[cluster_id]
                c2 = cluster_map[merge_with]
                merged_reports = c1.reports + c2.reports

                revised_clusters.append(
                    Cluster(
                        cluster_id=f"claude-merged-{cluster_id}",
                        name=cr.get("recommendation", {}).get("details", f"Merged: {c1.name} + {c2.name}")[:50],
                        description=cr.get("reasoning", ""),
                        reports=merged_reports,
                        merge_rationale=f"Claude merged {cluster_id} with {merge_with}: {cr.get('reasoning', '')}",
                        suggested_action=c1.suggested_action,
                        priority=cr.get("recommendation", {}).get("priority", min(c1.priority, c2.priority)),
                    )
                )
                processed_cluster_ids.add(cluster_id)
                processed_cluster_ids.add(merge_with)
                for r in merged_reports:
                    processed_report_files.add(r.filename)

    # Handle missed connections (create new clusters)
    for missed in review.get("missed_connections", []):
        reports_to_group = []
        for fname in missed.get("reports", []):
            if fname in report_map and fname not in processed_report_files:
                reports_to_group.append(report_map[fname])
                processed_report_files.add(fname)

        if len(reports_to_group) > 1:
            revised_clusters.append(
                Cluster(
                    cluster_id=f"claude-new-{len(revised_clusters)}",
                    name=missed.get("suggested_cluster_name", "Claude-identified group"),
                    description=missed.get("connection", ""),
                    reports=reports_to_group,
                    merge_rationale=f"Claude identified connection: {missed.get('connection', '')}",
                    suggested_action="Review these related changes together",
                    priority=2,
                )
            )

    # Add any unprocessed clusters
    for c in clusters:
        if c.cluster_id not in processed_cluster_ids:
            # Check if any of its reports are already processed
            remaining_reports = [r for r in c.reports if r.filename not in processed_report_files]
            if remaining_reports:
                c.reports = remaining_reports
                revised_clusters.append(c)
                for r in remaining_reports:
                    processed_report_files.add(r.filename)

    # Add any completely unprocessed reports as singletons
    for fname, report in report_map.items():
        if fname not in processed_report_files:
            revised_clusters.append(
                Cluster(
                    cluster_id=f"single-{report.commit_sha}",
                    name=f"Commit {report.commit_sha}",
                    description=report.message[:100],
                    reports=[report],
                    merge_rationale="Standalone commit",
                    suggested_action="Review individually",
                    priority=5,
                )
            )

    return revised_clusters


def generate_merged_report(cluster: Cluster, original_reports_dir: Path) -> str:
    """Generate a merged report for a cluster."""
    lines = [
        f"# Merged Report: {cluster.name}",
        "",
        f"**Cluster ID:** `{cluster.cluster_id}`",
        f"**Priority:** {'🔴 Critical' if cluster.priority == 1 else '🟡 High' if cluster.priority == 2 else '🟢 Normal'}",
        f"**Reports Merged:** {len(cluster.reports)}",
        "",
        "## Merge Rationale",
        "",
        cluster.merge_rationale,
        "",
        "## Suggested Action",
        "",
        cluster.suggested_action,
        "",
        "## Commits Included",
        "",
        "| Commit | JIRA | Message |",
        "|--------|------|---------|",
    ]

    # Add commit table
    for report in cluster.reports:
        jira_str = ", ".join(f"[{t}](https://gooddata.atlassian.net/browse/{t})" for t in report.jira_tickets) or "-"
        msg = report.message[:60] + "..." if len(report.message) > 60 else report.message
        lines.append(f"| `{report.commit_sha}` | {jira_str} | {msg} |")

    lines.extend(["", "## Combined Changes", ""])

    # Aggregate services
    all_services = sorted(set(s for r in cluster.reports for s in r.services))
    if all_services:
        lines.append("### Services Affected")
        lines.append("")
        for s in all_services:
            lines.append(f"- **{s}**")
        lines.append("")

    # Aggregate change categories
    all_categories = sorted(set(c for r in cluster.reports for c in r.change_categories))
    if all_categories:
        lines.append("### Change Categories")
        lines.append("")
        for cat in all_categories:
            icon = "🔴" if cat == "openapi_specs" else "🟡" if cat in ("controllers", "models") else "⚪"
            lines.append(f"- {icon} {cat.replace('_', ' ').title()}")
        lines.append("")

    # Aggregate OpenAPI changes
    all_endpoints_added = []
    all_endpoints_removed = []
    all_schemas_added = []
    all_schemas_removed = []

    for r in cluster.reports:
        all_endpoints_added.extend(r.openapi_changes.get("endpoints_added", []))
        all_endpoints_removed.extend(r.openapi_changes.get("endpoints_removed", []))
        all_schemas_added.extend(r.openapi_changes.get("schemas_added", []))
        all_schemas_removed.extend(r.openapi_changes.get("schemas_removed", []))

    if any([all_endpoints_added, all_endpoints_removed, all_schemas_added, all_schemas_removed]):
        lines.append("### OpenAPI Changes Summary")
        lines.append("")

        if all_endpoints_added:
            lines.append("**Endpoints Added:**")
            for ep in sorted(set(all_endpoints_added)):
                lines.append(f"- ➕ `{ep}`")
            lines.append("")

        if all_endpoints_removed:
            lines.append("**Endpoints Removed:**")
            for ep in sorted(set(all_endpoints_removed)):
                lines.append(f"- ➖ `{ep}`")
            lines.append("")

        if all_schemas_added:
            lines.append("**Schemas Added:**")
            for s in sorted(set(all_schemas_added)):
                lines.append(f"- ➕ `{s}`")
            lines.append("")

        if all_schemas_removed:
            lines.append("**Schemas Removed:**")
            for s in sorted(set(all_schemas_removed)):
                lines.append(f"- ➖ `{s}`")
            lines.append("")

    # Aggregate proto changes
    all_proto = sorted(set(p for r in cluster.reports for p in r.proto_changes))
    if all_proto:
        lines.append("### Proto Changes")
        lines.append("")
        for p in all_proto:
            lines.append(f"- {p}")
        lines.append("")

    # Add links to original reports
    lines.append("## Original Reports")
    lines.append("")
    for r in cluster.reports:
        lines.append(f"- [{r.filename}](./{r.filename})")
    lines.append("")

    lines.append("---")
    lines.append("*Generated by cluster_sdk_reports.py*")

    return "\n".join(lines)


def generate_cluster_summary(clusters: list[Cluster]) -> str:
    """Generate a summary of all clusters."""
    lines = [
        "# SDK Change Clusters",
        "",
        f"**Total Clusters:** {len(clusters)}",
        f"**Total Reports:** {sum(len(c.reports) for c in clusters)}",
        "",
        "## Cluster Overview",
        "",
        "| Priority | Cluster | Reports | Action |",
        "|----------|---------|---------|--------|",
    ]

    # Sort by priority
    sorted_clusters = sorted(clusters, key=lambda c: (c.priority, c.cluster_id))

    for c in sorted_clusters:
        priority_icon = "🔴" if c.priority == 1 else "🟡" if c.priority == 2 else "🟢"
        action_short = c.suggested_action.split("\n")[0][:50] if c.suggested_action else "-"
        lines.append(
            f"| {priority_icon} {c.priority} | [{c.name}](./cluster-{c.cluster_id}.md) | {len(c.reports)} | {action_short} |"
        )

    lines.extend(
        [
            "",
            "## Processing Recommendations",
            "",
            "Process clusters in priority order:",
            "",
        ]
    )

    for i, c in enumerate(sorted_clusters, 1):
        lines.append(f"{i}. **{c.name}** ({len(c.reports)} commits)")
        if c.suggested_action:
            for action in c.suggested_action.split("\n")[:3]:
                if action.strip():
                    lines.append(f"   - {action.strip()}")

    lines.extend(
        [
            "",
            "---",
            "*Generated by cluster_sdk_reports.py*",
        ]
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Cluster SDK diff reports for batch processing")
    parser.add_argument("--input-dir", required=True, help="Directory containing individual reports")
    parser.add_argument("--output-dir", required=True, help="Directory for clustered output")
    parser.add_argument(
        "--use-claude", action="store_true", help="Use Claude API for enhanced clustering (requires ANTHROPIC_API_KEY)"
    )
    parser.add_argument(
        "--min-cluster-size", type=int, default=2, help="Minimum reports to form a cluster (default: 2)"
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        sys.exit(1)

    # Parse all reports
    print(f"Reading reports from {input_dir}...")
    reports = []
    for report_file in input_dir.glob("*.md"):
        if report_file.name == "00-summary.md":
            continue
        metadata = parse_report(report_file)
        if metadata:
            reports.append(metadata)
            print(f"  Parsed: {report_file.name} ({metadata.impact_level})")

    if not reports:
        print("No reports found to cluster")
        sys.exit(0)

    print(f"\nFound {len(reports)} reports to cluster")

    # Perform heuristic clustering
    print("\nPerforming heuristic clustering...")
    clusters = heuristic_cluster(reports)
    print(f"  Created {len(clusters)} initial clusters")

    # Optionally have Claude review the clustering
    claude_review_md = ""
    if args.use_claude:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            print("\nHaving Claude critically review the clustering...")
            clusters, claude_review_md = claude_review_clusters(clusters, input_dir, api_key)
            print(f"  Revised cluster count: {len(clusters)}")
        else:
            print("\nWarning: --use-claude specified but ANTHROPIC_API_KEY not set, skipping review")

    # Filter out small clusters (make them singletons)
    final_clusters = []
    for c in clusters:
        if len(c.reports) >= args.min_cluster_size or c.cluster_id.startswith("single-"):
            final_clusters.append(c)
        else:
            # Convert to singleton
            for r in c.reports:
                final_clusters.append(
                    Cluster(
                        cluster_id=f"single-{r.commit_sha}",
                        name=f"Commit {r.commit_sha}",
                        description=r.message[:100],
                        reports=[r],
                        merge_rationale="Standalone commit",
                        suggested_action="Review individually",
                        priority=5,
                    )
                )

    # Generate output
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy original reports
    print(f"\nWriting output to {output_dir}...")

    # Generate cluster reports
    multi_report_clusters = [c for c in final_clusters if len(c.reports) > 1]
    singleton_clusters = [c for c in final_clusters if len(c.reports) == 1]

    print(f"  Multi-report clusters: {len(multi_report_clusters)}")
    print(f"  Singleton reports: {len(singleton_clusters)}")

    for cluster in multi_report_clusters:
        report_content = generate_merged_report(cluster, input_dir)
        output_file = output_dir / f"cluster-{cluster.cluster_id}.md"
        output_file.write_text(report_content)
        print(f"  Generated: {output_file.name}")

    # Generate summary
    summary_content = generate_cluster_summary(final_clusters)
    summary_file = output_dir / "00-clusters.md"
    summary_file.write_text(summary_content)
    print(f"  Generated: {summary_file.name}")

    # Generate JSON manifest for programmatic access
    manifest = {
        "total_reports": len(reports),
        "total_clusters": len(final_clusters),
        "multi_report_clusters": len(multi_report_clusters),
        "claude_reviewed": bool(claude_review_md),
        "clusters": [c.to_dict() for c in sorted(final_clusters, key=lambda x: (x.priority, x.cluster_id))],
    }
    manifest_file = output_dir / "clusters.json"
    manifest_file.write_text(json.dumps(manifest, indent=2))
    print(f"  Generated: {manifest_file.name}")

    # Write Claude review report if available
    if claude_review_md:
        review_file = output_dir / "01-claude-review.md"
        review_file.write_text(claude_review_md)
        print(f"  Generated: {review_file.name}")

    # Print summary
    print("\n" + "=" * 60)
    print("CLUSTERING SUMMARY")
    print("=" * 60)
    print(f"Input reports:        {len(reports)}")
    print(f"Multi-report clusters: {len(multi_report_clusters)}")
    print(f"Singleton reports:     {len(singleton_clusters)}")
    print(f"Potential agent runs saved: {len(reports) - len(final_clusters)}")
    print()

    if multi_report_clusters:
        print("Clusters formed:")
        for c in sorted(multi_report_clusters, key=lambda x: x.priority):
            print(f"  [{c.priority}] {c.name}: {len(c.reports)} reports")


if __name__ == "__main__":
    main()
