# (C) 2022 GoodData Corporation
import json
import os
import time
from pathlib import Path

import requests

fixtures_dir = Path(os.environ.get("FIXTURES_DIR", Path(os.path.curdir) / "fixtures"))
host = os.environ.get("HOST", "http://localhost:3000")
token = os.environ.get("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
header_host = os.environ.get("HEADER_HOST", None)
content_type_jsonapi = "application/vnd.gooddata.api+json"
content_type_default = "application/json"
headers = {"Host": header_host}
api_version = "v1"

# gdc-nas microservices configuration
GDC_NAS_DB_URL = "jdbc:postgresql://postgres:5432/tiger?sslmode=prefer"
GDC_NAS_DB_USER = "postgres"
GDC_NAS_DB_PASS = "passw0rd"


def rest_op(op, url_path, data=None, raise_ex=True):
    all_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        **headers,
    }
    url = f"{host}/{url_path}"
    kwargs = {
        "url": url,
        "headers": all_headers,
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


def read_data_from_file(data_json_path):
    with open(data_json_path) as f:
        return json.load(f)


def rest_op_jsonapi(op, url_path, data_json_path=None, raise_ex=True):
    headers["Content-Type"] = content_type_jsonapi
    return rest_op(op, url_path, data_json_path, raise_ex)


def rest_op_default(op, url_path, data_json_path=None, raise_ex=True):
    headers["Content-Type"] = content_type_default
    return rest_op(op, url_path, data_json_path, raise_ex)


def wait_platform_up():
    # wait till GD.CN is up and ready to receive requests
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


def discover_demo_schema(data_source_id: str) -> str | None:
    """
    Discover the demo schema from gdc-nas database.
    gdc-nas uses schema names with hash suffixes like 'demo_6d9051d9069a8468'.
    Uses SQL query to find all schemas starting with 'demo_'.
    Returns the schema name or None if not found.
    """
    print(f"Discovering demo schema from data source {data_source_id}...", flush=True)

    # Query postgres information_schema to find demo schemas
    # Exclude demo_denormalized and demo_no_timeshift variants
    sql_query = """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name LIKE 'demo_%'
        AND schema_name NOT LIKE 'demo_denormalized%'
        AND schema_name NOT LIKE 'demo_no_timeshift%'
        ORDER BY schema_name
        LIMIT 1
    """

    try:
        result = rest_op_default(
            "post",
            f"api/{api_version}/actions/dataSources/{data_source_id}/scanSql",
            {"sql": sql_query},
            raise_ex=False,
        )

        # The API returns dataPreview, not data
        if result and "dataPreview" in result:
            rows = result["dataPreview"]
            if rows and len(rows) > 0 and len(rows[0]) > 0:
                schema = rows[0][0]
                print(f"Discovered demo schema: {schema}", flush=True)
                return schema

        # Fallback: try to find any demo schema (including exact match 'demo')
        fallback_query = """
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name = 'demo' OR schema_name LIKE 'demo_%'
            ORDER BY length(schema_name), schema_name
            LIMIT 1
        """
        result = rest_op_default(
            "post",
            f"api/{api_version}/actions/dataSources/{data_source_id}/scanSql",
            {"sql": fallback_query},
            raise_ex=False,
        )

        if result and "dataPreview" in result:
            rows = result["dataPreview"]
            if rows and len(rows) > 0 and len(rows[0]) > 0:
                schema = rows[0][0]
                print(f"Discovered demo schema (fallback): {schema}", flush=True)
                return schema

        print("No demo schema found", flush=True)
    except Exception as e:
        print(f"Failed to discover schema: {e}", flush=True)

    return None


def configure_data_source_for_gdc_nas(data_sources: dict) -> dict:
    """
    Configure data sources to work with gdc-nas microservices.
    Updates connection URL and credentials.
    Initially sets schema to 'public' to allow schema discovery.
    """
    print("Configuring data sources for gdc-nas...", flush=True)

    for ds in data_sources.get("dataSources", []):
        if ds["id"] == "demo-test-ds":
            # Update to gdc-nas configuration
            ds["url"] = GDC_NAS_DB_URL
            ds["username"] = GDC_NAS_DB_USER
            ds["password"] = GDC_NAS_DB_PASS
            # Temporarily use 'public' schema to enable schema discovery
            ds["schema"] = "public"

    return data_sources


def update_data_source_schema(data_source_id: str, schema_name: str):
    """Update the schema for an existing data source."""
    print(f"Updating data source {data_source_id} to use schema {schema_name}", flush=True)

    # Get current data source
    result = rest_op_jsonapi("get", f"api/{api_version}/entities/dataSources/{data_source_id}", raise_ex=False)
    if result and "data" in result:
        # Update via PATCH
        patch_data = {"data": {"id": data_source_id, "type": "dataSource", "attributes": {"schema": schema_name}}}
        rest_op_jsonapi("patch", f"api/{api_version}/entities/dataSources/{data_source_id}", patch_data)


def update_ldm_schema_paths(hierarchy: dict, old_schema: str, new_schema: str) -> dict:
    """
    Update LDM table paths in the hierarchy to use the correct schema name.
    gdc-nas uses schema names like 'demo_6d9051d9069a8468' instead of 'demo'.
    Only updates 'path' arrays in dataSourceTableId objects.
    """

    def update_paths_recursive(obj):
        """Recursively find and update path arrays in dataSourceTableId objects."""
        if isinstance(obj, dict):
            # Check if this is a dataSourceTableId with a path
            if "path" in obj and "dataSourceId" in obj:
                path = obj["path"]
                if isinstance(path, list) and len(path) >= 1 and path[0] == old_schema:
                    obj["path"] = [new_schema] + path[1:]
            # Recurse into all dict values
            for value in obj.values():
                update_paths_recursive(value)
        elif isinstance(obj, list):
            for item in obj:
                update_paths_recursive(item)

    # Deep copy to avoid modifying original
    import copy

    updated_hierarchy = copy.deepcopy(hierarchy)
    update_paths_recursive(updated_hierarchy)

    print(f"Updated LDM paths: '{old_schema}' -> '{new_schema}'", flush=True)
    return updated_hierarchy


def update_test_fixtures(schema_name: str):
    """
    Update all SDK test fixture files with the discovered schema name.
    This ensures test fixtures match the gdc-nas schema naming.
    """

    import yaml

    sdk_tests_dir = fixtures_dir.parent.parent / "gooddata-sdk" / "tests"
    if not sdk_tests_dir.exists():
        print(f"SDK tests directory not found: {sdk_tests_dir}", flush=True)
        return

    print(f"Updating SDK test fixtures with schema: {schema_name}", flush=True)

    # Update data source YAML files
    ds_patterns = [
        sdk_tests_dir / "catalog/load/gooddata_layouts/default/data_sources/demo-test-ds/demo-test-ds.yaml",
    ]

    for ds_file in ds_patterns:
        if ds_file.exists():
            with open(ds_file) as f:
                content = yaml.safe_load(f)

            if content.get("schema") and content["schema"] != schema_name:
                content["schema"] = schema_name
                content["url"] = GDC_NAS_DB_URL
                content["username"] = GDC_NAS_DB_USER

                with open(ds_file, "w") as f:
                    # Preserve comment at top
                    f.write("# (C) 2022 GoodData Corporation\n")
                    yaml.dump(content, f, default_flow_style=False, sort_keys=False)
                print(f"  Updated: {ds_file.name}", flush=True)

    # Update LDM dataset YAML files (path arrays)
    ldm_dirs = [
        sdk_tests_dir / "catalog/load/gooddata_layouts/default/workspaces/demo/ldm/datasets",
        sdk_tests_dir / "catalog/load/gooddata_layouts/default/workspaces/demo_west/ldm/datasets",
    ]

    for ldm_dir in ldm_dirs:
        if ldm_dir.exists():
            for yaml_file in ldm_dir.glob("*.yaml"):
                with open(yaml_file) as f:
                    content = yaml.safe_load(f)

                updated = False
                if content and "dataSourceTableId" in content:
                    path = content["dataSourceTableId"].get("path", [])
                    if path and path[0] == "demo":
                        content["dataSourceTableId"]["path"][0] = schema_name
                        updated = True

                if updated:
                    with open(yaml_file, "w") as f:
                        f.write("# (C) 2025 GoodData Corporation\n")
                        yaml.dump(content, f, default_flow_style=False, sort_keys=False)
                    print(f"  Updated: {yaml_file.name}", flush=True)

    # Update expected JSON files
    expected_files = [
        sdk_tests_dir / "catalog/expected/declarative_data_sources.json",
    ]

    for expected_file in expected_files:
        if expected_file.exists():
            with open(expected_file) as f:
                content = json.load(f)

            updated = False
            for ds in content.get("dataSources", []):
                if ds.get("id") == "demo-test-ds" and ds.get("schema") != schema_name:
                    ds["schema"] = schema_name
                    ds["url"] = GDC_NAS_DB_URL
                    ds["username"] = GDC_NAS_DB_USER
                    updated = True

            if updated:
                with open(expected_file, "w") as f:
                    json.dump(content, f, indent=2)
                    f.write("\n")
                print(f"  Updated: {expected_file.name}", flush=True)

    print("Test fixtures updated!", flush=True)


def create_entity(entity_id, entity_data, entity_type, api_path, action):
    print(f"Creating {entity_type} id={entity_id}", flush=True)
    result = action("get", f"{api_path}/{entity_id}", raise_ex=False)
    if not result:
        return action("post", f"{api_path}", entity_data)
    else:
        print(f"Entity {entity_type} already exists id={entity_id} result={result}")
        return result


def update_layout():
    user_groups = read_data_from_file(fixtures_dir / "user_groups.json")
    user_auth = read_data_from_file(fixtures_dir / "user_auth.json")
    user = read_data_from_file(fixtures_dir / "user.json")
    data_sources = read_data_from_file(fixtures_dir / "demo_data_sources.json")
    hierarchy = read_data_from_file(fixtures_dir / "demo_declarative_hierarchy.json")
    permissions = read_data_from_file(fixtures_dir / "workspace_permissions.json")

    wait_platform_up()

    print("Uploading userGroups", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/userGroups", user_groups)

    response = create_entity(
        user_auth["email"], user_auth, "user auth", f"api/{api_version}/auth/users", rest_op_default
    )
    user["data"]["attributes"]["authenticationId"] = response["authenticationId"]
    create_entity(user["data"]["id"], user, "user", f"api/{api_version}/entities/users", rest_op_jsonapi)

    # Configure data sources for gdc-nas (updates URL, credentials)
    data_sources = configure_data_source_for_gdc_nas(data_sources)

    print("Uploading test DS with physical model for demo", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/dataSources", data_sources)

    # Discover the correct demo schema dynamically (gdc-nas uses hashed schema names)
    demo_schema = discover_demo_schema("demo-test-ds")
    if demo_schema:
        update_data_source_schema("demo-test-ds", demo_schema)
        # Update LDM paths in hierarchy to use the discovered schema
        if demo_schema != "demo":
            hierarchy = update_ldm_schema_paths(hierarchy, "demo", demo_schema)
            # Also update SDK test fixtures with the discovered schema
            update_test_fixtures(demo_schema)
    else:
        print("WARNING: Could not discover demo schema automatically!", flush=True)
        print("You may need to manually set the schema in the data source.", flush=True)

    print("Uploading demo workspaces", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/workspaces", hierarchy)

    print("Uploading permissions for demo workspace", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/workspaces/demo/permissions", permissions)

    print("Layout configuration done successfully!", flush=True)


if __name__ == "__main__":
    update_layout()
