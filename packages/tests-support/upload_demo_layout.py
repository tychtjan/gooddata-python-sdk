# (C) 2022 GoodData Corporation
"""
Setup script for GoodData SDK tests against gdc-nas.

Usage:
    FIXTURES_DIR="packages/tests-support/fixtures" uv run python packages/tests-support/upload_demo_layout.py

Environment variables:
    HOST: GoodData server URL (default: http://localhost:3000)
    TOKEN: API token (default: YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz)
    HEADER_HOST: Host header value (default: localhost)
    FIXTURES_DIR: Path to fixtures directory (default: ./fixtures)
    POSTGRES_HOST: Postgres host for direct DB operations (default: localhost)
    POSTGRES_PORT: Postgres port (default: 5432)
    POSTGRES_USER: Postgres user (default: postgres)
    POSTGRES_PASSWORD: Postgres password (default: passw0rd)
    POSTGRES_DB: Postgres database (default: tiger)
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Optional

import psycopg2
import requests

# Configuration from environment
fixtures_dir = Path(os.environ.get("FIXTURES_DIR", Path(os.path.curdir) / "fixtures"))
host = os.environ.get("HOST", "http://localhost:3000")
token = os.environ.get("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
header_host = os.environ.get("HEADER_HOST", "localhost")

# Postgres configuration for direct DB operations
pg_host = os.environ.get("POSTGRES_HOST", "localhost")
pg_port = int(os.environ.get("POSTGRES_PORT", "5432"))
pg_user = os.environ.get("POSTGRES_USER", "postgres")
pg_password = os.environ.get("POSTGRES_PASSWORD", "passw0rd")
pg_db = os.environ.get("POSTGRES_DB", "tiger")

# Docker internal postgres hostname (used by gdc-nas services)
DOCKER_POSTGRES_HOST = "postgres"

content_type_jsonapi = "application/vnd.gooddata.api+json"
content_type_default = "application/json"
api_version = "v1"

# Expected test configuration
EXPECTED_DATA_SOURCE_ID = "demo-test-ds"
EXPECTED_SCHEMA = "demo"


def get_headers() -> dict[str, Any]:
    """Build request headers."""
    headers: dict[str, Any] = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if header_host:
        headers["Host"] = header_host
    return headers


def rest_op(
    op: str,
    url_path: str,
    data: Optional[dict[str, Any]] = None,
    raise_ex: bool = True,
) -> Optional[dict[str, Any]]:
    """Execute REST operation."""
    url = f"{host}/{url_path}"
    kwargs: dict[str, Any] = {
        "url": url,
        "headers": get_headers(),
    }
    if data:
        kwargs["json"] = data

    op_fnc = getattr(requests, op)
    response = op_fnc(**kwargs)

    if response.status_code < 200 or response.status_code > 299:
        if raise_ex:
            raise Exception(f"Call to {url} failed - {str(response.text)}")
        else:
            return None

    if response.status_code == 200:
        return response.json()
    else:
        return None


def read_data_from_file(data_json_path: Path) -> dict[str, Any]:
    """Load JSON data from file."""
    with open(data_json_path) as f:
        return json.load(f)


def rest_op_jsonapi(
    op: str,
    url_path: str,
    data: Optional[dict[str, Any]] = None,
    raise_ex: bool = True,
) -> Optional[dict[str, Any]]:
    """Execute REST operation with JSON:API content type."""
    headers = get_headers()
    headers["Content-Type"] = content_type_jsonapi

    url = f"{host}/{url_path}"
    kwargs: dict[str, Any] = {
        "url": url,
        "headers": headers,
    }
    if data:
        kwargs["json"] = data

    op_fnc = getattr(requests, op)
    response = op_fnc(**kwargs)

    if response.status_code < 200 or response.status_code > 299:
        if raise_ex:
            raise Exception(f"Call to {url} failed - {str(response.text)}")
        else:
            return None

    if response.status_code == 200:
        return response.json()
    else:
        return None


def rest_op_default(
    op: str,
    url_path: str,
    data: Optional[dict[str, Any]] = None,
    raise_ex: bool = True,
) -> Optional[dict[str, Any]]:
    """Execute REST operation with default content type."""
    return rest_op(op, url_path, data, raise_ex)


def wait_platform_up() -> None:
    """Wait until GoodData platform is up and ready."""
    print("Waiting till GoodData platform is up", flush=True)
    while True:
        try:
            result = rest_op_jsonapi("get", f"api/{api_version}/entities/admin/organizations/default", raise_ex=False)
            if result is not None:
                print("GoodData platform is up", flush=True)
                break
            print("GoodData platform metadata not responding", flush=True)
        except requests.exceptions.ConnectionError:
            print("GoodData platform is not available", flush=True)
        time.sleep(4)


def create_entity(
    entity_id: str,
    entity_data: dict[str, Any],
    entity_type: str,
    api_path: str,
    action: Any,
) -> Optional[dict[str, Any]]:
    """Create entity if it doesn't exist."""
    print(f"Creating {entity_type} id={entity_id}", flush=True)
    result = action("get", f"{api_path}/{entity_id}", raise_ex=False)
    if not result:
        return action("post", f"{api_path}", entity_data)
    else:
        print(f"Entity {entity_type} already exists id={entity_id}")
        return result


def find_demo_schema() -> Optional[str]:
    """Find the demo schema in gdc-nas (has dynamic prefix like demo_6d9051d9069a8468)."""
    try:
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_password,
            database=pg_db,
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT schema_name FROM information_schema.schemata
            WHERE schema_name ~ '^demo_[a-f0-9]{16}$'
            LIMIT 1
        """)
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return row[0]
    except Exception as e:
        print(f"Warning: Could not search for demo schema: {e}", flush=True)

    return None


def setup_demo_schema_postgres() -> bool:
    """
    Set up the 'demo' schema in postgres by copying from the gdc-nas dynamic schema.
    Returns True if setup was successful.
    """
    source_schema = find_demo_schema()
    if not source_schema:
        print("Could not find source demo schema (demo_<hash>) in postgres", flush=True)
        return False

    print(f"Setting up '{EXPECTED_SCHEMA}' schema from '{source_schema}'...", flush=True)

    try:
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_password,
            database=pg_db,
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if demo schema already exists with tables
        cur.execute(
            """
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = %s AND table_type = 'BASE TABLE'
            """,
            (EXPECTED_SCHEMA,),
        )
        existing_tables = cur.fetchone()[0]
        if existing_tables > 0:
            print(f"Schema '{EXPECTED_SCHEMA}' already exists with {existing_tables} tables, skipping", flush=True)
            cur.close()
            conn.close()
            return True

        # Create demo schema
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {EXPECTED_SCHEMA}")

        # Get tables from source schema
        cur.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = %s AND table_type = 'BASE TABLE'
            """,
            (source_schema,),
        )
        tables = [row[0] for row in cur.fetchall()]

        # Copy each table structure and data
        for table in tables:
            print(f"  Copying table {table}...", flush=True)
            # Drop if exists (in case of partial previous run)
            cur.execute(f"DROP TABLE IF EXISTS {EXPECTED_SCHEMA}.{table} CASCADE")
            cur.execute(f"CREATE TABLE {EXPECTED_SCHEMA}.{table} (LIKE {source_schema}.{table} INCLUDING ALL)")
            cur.execute(f"INSERT INTO {EXPECTED_SCHEMA}.{table} SELECT * FROM {source_schema}.{table}")

        cur.close()
        conn.close()
        print(f"Schema '{EXPECTED_SCHEMA}' created successfully with {len(tables)} tables", flush=True)
        return True

    except Exception as e:
        print(f"Failed to set up demo schema: {e}", flush=True)
        return False


def delete_data_source_if_exists() -> None:
    """Delete the test data source if it exists (to ensure clean state)."""
    try:
        result = rest_op("get", f"api/{api_version}/entities/dataSources/{EXPECTED_DATA_SOURCE_ID}", raise_ex=False)
        if result:
            print(f"Deleting existing data source '{EXPECTED_DATA_SOURCE_ID}'...", flush=True)
            rest_op("delete", f"api/{api_version}/entities/dataSources/{EXPECTED_DATA_SOURCE_ID}", raise_ex=False)
            time.sleep(2)  # Give time for deletion to propagate
    except Exception as e:
        print(f"Warning: Could not delete existing data source: {e}", flush=True)


def setup_data_source_for_tests() -> None:
    """
    Create the expected test data source (demo-test-ds).
    Points to postgres:5432/tiger with schema 'demo'.
    """
    print(f"Setting up data source '{EXPECTED_DATA_SOURCE_ID}'...", flush=True)

    # Delete existing data source to ensure clean state
    delete_data_source_if_exists()

    # Create the data source with correct gdc-nas configuration
    # Use docker internal hostname 'postgres' (not localhost)
    data_source = {
        "data": {
            "id": EXPECTED_DATA_SOURCE_ID,
            "type": "dataSource",
            "attributes": {
                "name": EXPECTED_DATA_SOURCE_ID,
                "type": "POSTGRESQL",
                "url": f"jdbc:postgresql://{DOCKER_POSTGRES_HOST}:5432/{pg_db}?sslmode=prefer",
                "schema": EXPECTED_SCHEMA,
                "username": pg_user,
                "password": pg_password,
            },
        }
    }

    try:
        rest_op_jsonapi("post", f"api/{api_version}/entities/dataSources", data_source)
        print(f"Data source '{EXPECTED_DATA_SOURCE_ID}' created", flush=True)
    except Exception as e:
        if "already stored" in str(e) or "409" in str(e):
            print(f"Data source '{EXPECTED_DATA_SOURCE_ID}' already exists (conflict)", flush=True)
        else:
            raise


def setup_data_source_permissions() -> None:
    """Set up permissions on the data source."""
    print("Setting up data source permissions...", flush=True)
    permissions = {
        "permissions": [
            {"assignee": {"id": "demo2", "type": "user"}, "name": "MANAGE"},
            {"assignee": {"id": "demoGroup", "type": "userGroup"}, "name": "USE"},
        ]
    }
    try:
        rest_op_default(
            "put",
            f"api/{api_version}/layout/dataSources/{EXPECTED_DATA_SOURCE_ID}/permissions",
            permissions,
            raise_ex=True,
        )
        print("Data source permissions set successfully", flush=True)
    except Exception as e:
        print(f"Warning: Failed to set data source permissions: {e}", flush=True)


def scan_and_cache_pdm() -> None:
    """Scan data source and cache the physical data model."""
    print(f"Scanning data source '{EXPECTED_DATA_SOURCE_ID}'...", flush=True)
    try:
        rest_op_default(
            "post",
            f"api/{api_version}/actions/dataSources/{EXPECTED_DATA_SOURCE_ID}/scan",
            {"scanTables": True, "scanViews": True},
            raise_ex=False,
        )
        print("PDM scan completed", flush=True)
    except Exception as e:
        print(f"Warning: PDM scan failed (may not be critical): {e}", flush=True)


def update_layout() -> None:
    """Main function to set up gdc-nas test environment."""
    user_groups = read_data_from_file(fixtures_dir / "user_groups.json")
    user_auth = read_data_from_file(fixtures_dir / "user_auth.json")
    user = read_data_from_file(fixtures_dir / "user.json")
    hierarchy = read_data_from_file(fixtures_dir / "demo_declarative_hierarchy.json")
    permissions = read_data_from_file(fixtures_dir / "workspace_permissions.json")

    wait_platform_up()

    print("Setting up gdc-nas test environment...", flush=True)

    # Step 1: Set up the demo schema (copy from dynamic schema)
    if not setup_demo_schema_postgres():
        print("Warning: Could not set up demo schema, some tests may fail", flush=True)

    # Step 2: Create the test data source
    setup_data_source_for_tests()

    # Step 3: Set up users and groups (needed for permissions)
    print("Uploading userGroups", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/userGroups", user_groups)

    response = create_entity(
        user_auth["email"], user_auth, "user auth", f"api/{api_version}/auth/users", rest_op_default
    )
    if response:
        user["data"]["attributes"]["authenticationId"] = response.get("authenticationId", "")
    create_entity(user["data"]["id"], user, "user", f"api/{api_version}/entities/users", rest_op_jsonapi)

    # Step 4: Set up data source permissions (after users/groups exist)
    setup_data_source_permissions()

    # Step 5: Set up workspaces
    print("Uploading demo workspaces", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/workspaces", hierarchy)

    # Step 6: Set up workspace permissions
    print("Uploading permissions for demo workspace", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/workspaces/demo/permissions", permissions)

    # Step 7: Scan data source to ensure PDM is cached
    scan_and_cache_pdm()

    print("Layout configuration done successfully!", flush=True)


if __name__ == "__main__":
    update_layout()
