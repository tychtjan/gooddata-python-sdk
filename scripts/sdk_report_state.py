#!/usr/bin/env python3
# (C) 2024 GoodData Corporation
"""
SDK Report State Management

Tracks the status of SDK diff reports and clusters through their lifecycle:
- new: Just generated, needs attention
- reviewed: Human/agent has looked at it
- in_progress: Agent is actively working on implementation
- implemented: SDK changes have been made
- skipped: No action needed (not SDK-relevant, duplicate, etc.)

State is stored in .github/sdk-report-state.json and committed to the repo.

Usage:
    # Mark a report as reviewed
    python sdk_report_state.py mark --report f4d1ceb1aab5.md --status reviewed --by "user:john"

    # Mark a cluster as in_progress
    python sdk_report_state.py mark --cluster openapi-result-cache --status in_progress --by "agent:sdk-analyze"

    # List all reports needing attention
    python sdk_report_state.py list --status new

    # Show summary of all states
    python sdk_report_state.py summary

    # Sync state with current reports (add new, keep existing)
    python sdk_report_state.py sync --reports-dir ./reports --clusters-dir ./clustered
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Valid statuses in lifecycle order
VALID_STATUSES = ["new", "reviewed", "in_progress", "implemented", "skipped"]

# Default state file location
DEFAULT_STATE_FILE = ".github/sdk-report-state.json"


def load_state(state_file: Path) -> dict:
    """Load existing state or return empty state."""
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {state_file}, starting fresh")

    return {
        "version": 1,
        "last_updated": None,
        "reports": {},
        "clusters": {},
    }


def save_state(state: dict, state_file: Path) -> None:
    """Save state to file."""
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2, sort_keys=False))


def mark_item(
    state: dict,
    item_type: str,  # "reports" or "clusters"
    item_id: str,
    status: str,
    marked_by: str | None = None,
    notes: str | None = None,
    pr_number: int | None = None,
    jira_tickets: list[str] | None = None,
) -> None:
    """Mark a report or cluster with a new status."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of: {VALID_STATUSES}")

    now = datetime.now(timezone.utc).isoformat()

    if item_id not in state[item_type]:
        state[item_type][item_id] = {
            "status": "new",
            "created_at": now,
            "history": [],
        }

    item = state[item_type][item_id]
    old_status = item.get("status", "new")

    # Record history
    if "history" not in item:
        item["history"] = []

    item["history"].append(
        {
            "from_status": old_status,
            "to_status": status,
            "changed_at": now,
            "changed_by": marked_by,
        }
    )

    # Update current status
    item["status"] = status
    item["updated_at"] = now

    if marked_by:
        item["last_updated_by"] = marked_by

    if notes:
        item["notes"] = notes

    if pr_number:
        item["pr_number"] = pr_number

    if jira_tickets:
        item["jira_tickets"] = jira_tickets

    # Set specific timestamps based on status
    if status == "reviewed":
        item["reviewed_at"] = now
        if marked_by:
            item["reviewed_by"] = marked_by
    elif status == "in_progress":
        item["started_at"] = now
        if marked_by:
            item["assigned_to"] = marked_by
    elif status == "implemented":
        item["implemented_at"] = now
        if marked_by:
            item["implemented_by"] = marked_by


def sync_with_reports(
    state: dict,
    reports_dir: Path | None = None,
    clusters_dir: Path | None = None,
) -> dict:
    """
    Sync state with current report files.
    - Add new reports/clusters as 'new'
    - Keep existing states
    - Optionally mark missing reports as 'archived'
    """
    now = datetime.now(timezone.utc).isoformat()
    stats = {"new_reports": 0, "new_clusters": 0, "existing": 0}

    # Sync individual reports
    if reports_dir and reports_dir.exists():
        for report_file in reports_dir.glob("*.md"):
            if report_file.name.startswith("00-"):
                continue  # Skip summary files

            report_id = report_file.name
            if report_id not in state["reports"]:
                state["reports"][report_id] = {
                    "status": "new",
                    "created_at": now,
                    "source_file": str(report_file),
                    "history": [],
                }
                stats["new_reports"] += 1
            else:
                stats["existing"] += 1

    # Sync clusters
    if clusters_dir and clusters_dir.exists():
        # Read cluster manifest if available
        manifest_file = clusters_dir / "clusters.json"
        if manifest_file.exists():
            manifest = json.loads(manifest_file.read_text())
            for cluster in manifest.get("clusters", []):
                cluster_id = cluster.get("cluster_id")
                if cluster_id and cluster_id not in state["clusters"]:
                    state["clusters"][cluster_id] = {
                        "status": "new",
                        "created_at": now,
                        "name": cluster.get("name"),
                        "report_count": len(cluster.get("reports", [])),
                        "reports": [r.get("filename") for r in cluster.get("reports", [])],
                        "history": [],
                    }
                    stats["new_clusters"] += 1
                else:
                    stats["existing"] += 1

    return stats


def list_items(state: dict, item_type: str, status_filter: str | None = None) -> list[dict]:
    """List items optionally filtered by status."""
    items = []
    for item_id, item_data in state.get(item_type, {}).items():
        if status_filter is None or item_data.get("status") == status_filter:
            items.append({"id": item_id, **item_data})

    # Sort by created_at (newest first)
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


def get_summary(state: dict) -> dict:
    """Get summary statistics."""
    summary = {
        "last_updated": state.get("last_updated"),
        "reports": {status: 0 for status in VALID_STATUSES},
        "clusters": {status: 0 for status in VALID_STATUSES},
        "total_reports": len(state.get("reports", {})),
        "total_clusters": len(state.get("clusters", {})),
    }

    for item_data in state.get("reports", {}).values():
        status = item_data.get("status", "new")
        if status in summary["reports"]:
            summary["reports"][status] += 1

    for item_data in state.get("clusters", {}).values():
        status = item_data.get("status", "new")
        if status in summary["clusters"]:
            summary["clusters"][status] += 1

    return summary


def print_summary(state: dict) -> None:
    """Print a formatted summary."""
    summary = get_summary(state)

    print("=" * 50)
    print("SDK REPORT STATE SUMMARY")
    print("=" * 50)
    print(f"Last updated: {summary['last_updated'] or 'Never'}")
    print()

    print("REPORTS:")
    print("-" * 30)
    for status in VALID_STATUSES:
        count = summary["reports"][status]
        icon = {"new": "🆕", "reviewed": "👁️", "in_progress": "🔄", "implemented": "✅", "skipped": "⏭️"}.get(status, "")
        print(f"  {icon} {status:15} {count:3}")
    print(f"  {'─' * 20}")
    print(f"  {'Total':15} {summary['total_reports']:3}")
    print()

    print("CLUSTERS:")
    print("-" * 30)
    for status in VALID_STATUSES:
        count = summary["clusters"][status]
        icon = {"new": "🆕", "reviewed": "👁️", "in_progress": "🔄", "implemented": "✅", "skipped": "⏭️"}.get(status, "")
        print(f"  {icon} {status:15} {count:3}")
    print(f"  {'─' * 20}")
    print(f"  {'Total':15} {summary['total_clusters']:3}")


def print_items(items: list[dict], item_type: str) -> None:
    """Print a formatted list of items."""
    if not items:
        print(f"No {item_type} found")
        return

    print(f"\n{item_type.upper()} ({len(items)} items):")
    print("-" * 60)

    for item in items:
        status = item.get("status", "unknown")
        icon = {"new": "🆕", "reviewed": "👁️", "in_progress": "🔄", "implemented": "✅", "skipped": "⏭️"}.get(
            status, "❓"
        )

        item_id = item.get("id", "unknown")
        created = item.get("created_at", "")[:10] if item.get("created_at") else ""

        extra_info = ""
        if item.get("assigned_to"):
            extra_info = f" (assigned: {item['assigned_to']})"
        elif item.get("pr_number"):
            extra_info = f" (PR #{item['pr_number']})"
        elif item.get("notes"):
            extra_info = f" ({item['notes'][:30]}...)" if len(item.get("notes", "")) > 30 else f" ({item['notes']})"

        print(f"  {icon} [{status:12}] {item_id:40} {created}{extra_info}")


def main():
    parser = argparse.ArgumentParser(description="Manage SDK report state")
    parser.add_argument(
        "--state-file",
        default=DEFAULT_STATE_FILE,
        help=f"State file path (default: {DEFAULT_STATE_FILE})",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # mark command
    mark_parser = subparsers.add_parser("mark", help="Mark a report or cluster with a status")
    mark_parser.add_argument("--report", help="Report filename to mark")
    mark_parser.add_argument("--cluster", help="Cluster ID to mark")
    mark_parser.add_argument("--status", required=True, choices=VALID_STATUSES, help="New status")
    mark_parser.add_argument("--by", help="Who is making the change (e.g., 'user:john', 'agent:sdk-analyze')")
    mark_parser.add_argument("--notes", help="Notes about the status change")
    mark_parser.add_argument("--pr", type=int, help="Associated PR number")
    mark_parser.add_argument("--jira", nargs="+", help="Associated JIRA tickets")

    # list command
    list_parser = subparsers.add_parser("list", help="List reports or clusters")
    list_parser.add_argument("--type", choices=["reports", "clusters", "all"], default="all", help="What to list")
    list_parser.add_argument("--status", choices=VALID_STATUSES, help="Filter by status")

    # summary command
    subparsers.add_parser("summary", help="Show summary statistics")

    # sync command
    sync_parser = subparsers.add_parser("sync", help="Sync state with report files")
    sync_parser.add_argument("--reports-dir", type=Path, help="Directory containing individual reports")
    sync_parser.add_argument("--clusters-dir", type=Path, help="Directory containing clustered reports")

    # get command (for programmatic use)
    get_parser = subparsers.add_parser("get", help="Get state for a specific item (JSON output)")
    get_parser.add_argument("--report", help="Report filename")
    get_parser.add_argument("--cluster", help="Cluster ID")

    # needs-attention command
    subparsers.add_parser("needs-attention", help="List items that need attention (new or in_progress)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    state_file = Path(args.state_file)
    state = load_state(state_file)

    if args.command == "mark":
        if not args.report and not args.cluster:
            print("Error: Must specify --report or --cluster")
            sys.exit(1)

        if args.report:
            mark_item(
                state,
                "reports",
                args.report,
                args.status,
                marked_by=args.by,
                notes=args.notes,
                pr_number=args.pr,
                jira_tickets=args.jira,
            )
            print(f"Marked report '{args.report}' as '{args.status}'")

        if args.cluster:
            mark_item(
                state,
                "clusters",
                args.cluster,
                args.status,
                marked_by=args.by,
                notes=args.notes,
                pr_number=args.pr,
                jira_tickets=args.jira,
            )
            print(f"Marked cluster '{args.cluster}' as '{args.status}'")

        save_state(state, state_file)

    elif args.command == "list":
        if args.type in ("reports", "all"):
            items = list_items(state, "reports", args.status)
            print_items(items, "reports")

        if args.type in ("clusters", "all"):
            items = list_items(state, "clusters", args.status)
            print_items(items, "clusters")

    elif args.command == "summary":
        print_summary(state)

    elif args.command == "sync":
        stats = sync_with_reports(state, args.reports_dir, args.clusters_dir)
        save_state(state, state_file)
        print(f"Synced state: {stats['new_reports']} new reports, {stats['new_clusters']} new clusters")
        print(f"  (kept {stats['existing']} existing items)")

    elif args.command == "get":
        if args.report:
            item = state.get("reports", {}).get(args.report)
            if item:
                print(json.dumps({"id": args.report, **item}, indent=2))
            else:
                print(json.dumps({"error": "not found"}))
                sys.exit(1)
        elif args.cluster:
            item = state.get("clusters", {}).get(args.cluster)
            if item:
                print(json.dumps({"id": args.cluster, **item}, indent=2))
            else:
                print(json.dumps({"error": "not found"}))
                sys.exit(1)
        else:
            print("Error: Must specify --report or --cluster")
            sys.exit(1)

    elif args.command == "needs-attention":
        print("\n🔔 ITEMS NEEDING ATTENTION")
        print("=" * 50)

        new_reports = list_items(state, "reports", "new")
        in_progress_reports = list_items(state, "reports", "in_progress")
        new_clusters = list_items(state, "clusters", "new")
        in_progress_clusters = list_items(state, "clusters", "in_progress")

        if new_clusters:
            print(f"\n🆕 New clusters ({len(new_clusters)}):")
            for item in new_clusters:
                print(f"  - {item['id']}: {item.get('name', 'N/A')} ({item.get('report_count', '?')} reports)")

        if in_progress_clusters:
            print(f"\n🔄 In-progress clusters ({len(in_progress_clusters)}):")
            for item in in_progress_clusters:
                assigned = item.get("assigned_to", "unassigned")
                print(f"  - {item['id']}: {item.get('name', 'N/A')} (by {assigned})")

        if new_reports:
            print(f"\n🆕 New reports ({len(new_reports)}):")
            for item in new_reports[:10]:  # Limit to first 10
                print(f"  - {item['id']}")
            if len(new_reports) > 10:
                print(f"  ... and {len(new_reports) - 10} more")

        if in_progress_reports:
            print(f"\n🔄 In-progress reports ({len(in_progress_reports)}):")
            for item in in_progress_reports:
                assigned = item.get("assigned_to", "unassigned")
                print(f"  - {item['id']} (by {assigned})")

        total = len(new_reports) + len(in_progress_reports) + len(new_clusters) + len(in_progress_clusters)
        if total == 0:
            print("\n✅ All caught up! Nothing needs attention.")
        else:
            print(f"\n📊 Total items needing attention: {total}")


if __name__ == "__main__":
    main()
