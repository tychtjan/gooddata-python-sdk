# (C) 2022 GoodData Corporation
"""
Upload demo layout for SDK tests against NAS (microservices) backend.

This script:
1. Creates the demo schema and tables in NAS postgres (tiger database)
2. Uploads metadata: user groups, users, data sources, workspaces, permissions

Environment variables:
  - HOST: GoodData API endpoint (default: http://localhost:3000)
  - TOKEN: API token (default: bootstrap admin token)
  - HEADER_HOST: Host header for org routing (default: None)
  - FIXTURES_DIR: Path to fixtures directory (default: ./fixtures)
  - POSTGRES_CONTAINER: Docker container name (default: gdc-nas-postgres-1)
"""

import json
import os
import subprocess
import time
from pathlib import Path

import requests

fixtures_dir = Path(os.environ.get("FIXTURES_DIR", Path(os.path.curdir) / "fixtures"))
host = os.environ.get("HOST", "http://localhost:3000")
token = os.environ.get("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
header_host = os.environ.get("HEADER_HOST", None)
postgres_container = os.environ.get("POSTGRES_CONTAINER", "gdc-nas-postgres-1")
content_type_jsonapi = "application/vnd.gooddata.api+json"
content_type_default = "application/json"
base_headers = {"Host": header_host} if header_host else {}
api_version = "v1"


def setup_postgres():
    """Create demo schema and tables in NAS postgres (tiger database)."""
    print("Setting up PostgreSQL demo schema...", flush=True)

    sql = """
    CREATE SCHEMA IF NOT EXISTS demo;
    CREATE TABLE IF NOT EXISTS demo.products (product_id int PRIMARY KEY, product_name varchar(128), category varchar(128));
    CREATE TABLE IF NOT EXISTS demo.campaigns (campaign_id int PRIMARY KEY, campaign_name varchar(128));
    CREATE TABLE IF NOT EXISTS demo.customers (customer_id int PRIMARY KEY, customer_name varchar(128), state varchar(64), region varchar(64));
    CREATE TABLE IF NOT EXISTS demo.campaign_channels (campaign_channel_id varchar(128) PRIMARY KEY, category varchar(128), type varchar(128), budget decimal(15,2), spend decimal(15,2), campaign_id int);
    CREATE TABLE IF NOT EXISTS demo.order_lines (order_line_id varchar(128) PRIMARY KEY, order_id varchar(128), order_status varchar(128), date date, campaign_id int, customer_id int, product_id int, price decimal(15,2), quantity decimal(15,2));
    INSERT INTO demo.campaigns VALUES (1,'Spring Sale'),(2,'Summer Promo'),(3,'Fall Campaign') ON CONFLICT DO NOTHING;
    INSERT INTO demo.products VALUES (1,'Widget A','Electronics'),(2,'Gadget B','Electronics'),(3,'Tool C','Hardware'),(4,'Device D','Electronics'),(5,'Item E','Hardware'),(6,'Thing F','Electronics'),(7,'Object G','Hardware'),(8,'Unit H','Electronics'),(9,'Part I','Hardware'),(10,'Piece J','Electronics') ON CONFLICT DO NOTHING;
    INSERT INTO demo.customers VALUES (1,'Acme Corp','CA','West'),(2,'Beta Inc','NY','East'),(3,'Gamma LLC','TX','South') ON CONFLICT DO NOTHING;
    INSERT INTO demo.campaign_channels VALUES ('cc1','Digital','Email',1000,800,1),('cc2','Digital','Social',2000,1500,1),('cc3','Traditional','Print',500,450,2) ON CONFLICT DO NOTHING;
    INSERT INTO demo.order_lines VALUES ('ol1','ord1','Completed','2024-01-15',NULL,1,1,100,2),('ol2','ord1','Completed','2024-01-15',1,1,2,150,1),('ol3','ord2','Pending','2024-02-20',2,2,3,75,3),('ol4','ord3','Completed','2024-03-10',1,3,4,200,1),('ol5','ord4','Pending','2024-04-05',NULL,1,5,50,4) ON CONFLICT DO NOTHING;
    """

    try:
        subprocess.run(
            ["docker", "exec", postgres_container, "psql", "-U", "postgres", "-d", "tiger", "-c", sql],
            capture_output=True,
            text=True,
            check=True,
        )
        print("  PostgreSQL demo schema created!", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"  Warning: PostgreSQL setup failed: {e.stderr}", flush=True)
    except FileNotFoundError:
        print("  Warning: docker command not found, skipping postgres setup", flush=True)


def rest_op(op, url_path, data=None, raise_ex=True, content_type="application/json"):
    all_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
        "Accept": content_type,
        **base_headers,
    }
    url = f"{host}/{url_path}"
    kwargs = {"url": url, "headers": all_headers}
    if data:
        kwargs["json"] = data

    op_fnc = getattr(requests, op)
    response = op_fnc(**kwargs)

    if response.status_code < 200 or response.status_code > 299:
        if raise_ex:
            raise Exception(f"Call to {url} failed - {str(response.text)}")
        return None

    return response.json() if response.status_code == 200 else None


def read_data_from_file(data_json_path):
    with open(data_json_path) as f:
        return json.load(f)


def wait_platform_up():
    """Wait for GoodData platform to be up and ready."""
    print("Waiting for GoodData platform...", flush=True)
    for attempt in range(60):
        try:
            result = rest_op(
                "get",
                f"api/{api_version}/entities/admin/organizations/default",
                raise_ex=False,
                content_type=content_type_jsonapi,
            )
            if result is not None:
                print("  Platform is up!", flush=True)
                return
        except requests.exceptions.ConnectionError:
            pass
        print(f"  Waiting... ({attempt + 1}/60)", flush=True)
        time.sleep(2)
    raise Exception("Platform not available")


def create_entity(entity_id, entity_data, entity_type, api_path, use_jsonapi=False):
    print(f"  Creating {entity_type}: {entity_id}", flush=True)
    ct = content_type_jsonapi if use_jsonapi else content_type_default
    result = rest_op("get", f"{api_path}/{entity_id}", raise_ex=False, content_type=ct)
    if not result:
        return rest_op("post", api_path, entity_data, content_type=ct)
    print("    Already exists", flush=True)
    return result


def update_layout():
    user_groups = read_data_from_file(fixtures_dir / "user_groups.json")
    user_auth = read_data_from_file(fixtures_dir / "user_auth.json")
    user = read_data_from_file(fixtures_dir / "user.json")
    data_sources = read_data_from_file(fixtures_dir / "demo_data_sources.json")
    hierarchy = read_data_from_file(fixtures_dir / "demo_declarative_hierarchy.json")
    permissions = read_data_from_file(fixtures_dir / "workspace_permissions.json")
    ds_permissions = read_data_from_file(fixtures_dir / "data_source_permissions.json")

    # Setup postgres first
    setup_postgres()

    # Wait for platform
    wait_platform_up()

    print(f"\nUploading to: {host}\n", flush=True)

    print("Uploading user groups...", flush=True)
    rest_op("put", f"api/{api_version}/layout/userGroups", user_groups)

    print("Creating test user...", flush=True)
    response = create_entity(user_auth["email"], user_auth, "user auth", f"api/{api_version}/auth/users")
    if response and "authenticationId" in response:
        user["data"]["attributes"]["authenticationId"] = response["authenticationId"]
        create_entity(user["data"]["id"], user, "user", f"api/{api_version}/entities/users", use_jsonapi=True)

    print("Uploading data sources...", flush=True)
    # Use entity API for data sources (layout API doesn't properly handle passwords)
    for ds in data_sources.get("dataSources", []):
        ds_id = ds["id"]
        # Delete existing first
        rest_op("delete", f"api/{api_version}/entities/dataSources/{ds_id}", raise_ex=False)
        print(f"  Deleted existing: {ds_id}", flush=True)

        # Create via entity API with password
        entity_data = {
            "data": {
                "id": ds_id,
                "type": "dataSource",
                "attributes": {
                    "name": ds.get("name", ds_id),
                    "type": ds["type"],
                    "url": ds["url"],
                    "schema": ds.get("schema", "public"),
                    "username": ds["username"],
                    "password": ds["password"],
                },
            }
        }
        rest_op(
            "put", f"api/{api_version}/entities/dataSources/{ds_id}", entity_data, content_type=content_type_jsonapi
        )
        print(f"  Created: {ds_id}", flush=True)

    print("Uploading workspaces...", flush=True)
    rest_op("put", f"api/{api_version}/layout/workspaces", hierarchy)

    print("Uploading workspace permissions...", flush=True)
    rest_op("put", f"api/{api_version}/layout/workspaces/demo/permissions", permissions)

    print("Uploading data source permissions...", flush=True)
    rest_op("put", f"api/{api_version}/layout/dataSources/demo-test-ds/permissions", ds_permissions)

    print("\n✓ Done!", flush=True)


if __name__ == "__main__":
    update_layout()
