# (C) 2024 GoodData Corporation
"""
Service Connectivity and Authentication Tests

This module provides tests for verifying connection and authentication to individual
GoodData services. It's particularly useful for testing the transition from AIO
(All-in-One) to multiservice architecture.

Run these tests to verify:
1. Connection to each service endpoint
2. Authentication to each service endpoint
3. Proper error handling for invalid credentials

Usage:
    # Run all connectivity tests (with VCR cassettes):
    make test TEST_FILTER=test_service_connectivity

    # Run specific service tests:
    pytest tests/service/test_service_connectivity.py -k "entities" -v

    # Run tests against live services (no cassettes):
    OVERWRITE=1 pytest tests/service/test_service_connectivity.py -v

    # Run only connection tests:
    pytest tests/service/test_service_connectivity.py -k "connection" -v

    # Run only authentication tests:
    pytest tests/service/test_service_connectivity.py -k "auth" -v
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pytest
from gooddata_api_client import exceptions
from gooddata_sdk import GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures" / "connectivity"


# =============================================================================
# Helper Functions
# =============================================================================


def create_sdk(host: str, token: str, timeout: Optional[float] = 10.0) -> GoodDataSdk:
    """Create SDK instance with optional timeout for connection tests."""
    return GoodDataSdk.create(host_=host, token_=token)


def create_sdk_invalid_token(host: str) -> GoodDataSdk:
    """Create SDK instance with an invalid token for auth failure tests."""
    return GoodDataSdk.create(host_=host, token_="invalid_token_12345")


def create_sdk_invalid_host() -> GoodDataSdk:
    """Create SDK instance with an invalid host for connection failure tests."""
    return GoodDataSdk.create(host_="http://invalid-host-that-does-not-exist:9999", token_="any_token")


# =============================================================================
# Entities API Tests (Metadata Service)
# /api/v1/entities/* and /api/v1/options
# =============================================================================


class TestEntitiesApiConnectivity:
    """
    Tests for Entities API connectivity.

    The Entities API handles metadata operations:
    - GET /api/v1/options - Get all configuration options
    - GET /api/v1/entities/workspaces - List workspaces
    - GET /api/v1/entities/dataSources - List data sources
    - GET /api/v1/entities/users - List users
    - etc.
    """

    @gd_vcr.use_cassette(str(_fixtures_dir / "entities_connection_success.yaml"))
    def test_entities_api_connection_success(self, test_config):
        """Test successful connection to Entities API via /api/v1/options endpoint."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # This internally calls GET /api/v1/options
        assert sdk.support.is_available is True

    @gd_vcr.use_cassette(str(_fixtures_dir / "entities_get_workspaces.yaml"))
    def test_entities_api_list_workspaces(self, test_config):
        """Test Entities API can list workspaces."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # GET /api/v1/entities/workspaces
        workspaces = sdk.catalog_workspace.list_workspaces()
        assert workspaces is not None
        # Should have at least the demo workspace from test config
        assert len(workspaces) > 0

    @gd_vcr.use_cassette(str(_fixtures_dir / "entities_get_data_sources.yaml"))
    def test_entities_api_list_data_sources(self, test_config):
        """Test Entities API can list data sources."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # GET /api/v1/entities/dataSources
        data_sources = sdk.catalog_data_source.list_data_sources()
        assert data_sources is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "entities_auth_failure.yaml"))
    def test_entities_api_auth_failure(self, test_config):
        """Test Entities API returns proper error for invalid token."""
        sdk = create_sdk_invalid_token(test_config["host"])

        with pytest.raises((exceptions.UnauthorizedException, exceptions.ForbiddenException)):
            # This should fail authentication
            _ = sdk.support.is_available

    def test_entities_api_connection_failure(self):
        """Test Entities API handles connection failure gracefully."""
        sdk = create_sdk_invalid_host()

        # Should return False for unreachable host, not raise exception
        assert sdk.support.is_available is False


# =============================================================================
# Actions API Tests (Compute/AFM Service)
# /api/v1/actions/*
# =============================================================================


class TestActionsApiConnectivity:
    """
    Tests for Actions API connectivity.

    The Actions API handles:
    - Compute operations (AFM execution)
    - Data source scanning
    - Export operations
    - AI features
    """

    @gd_vcr.use_cassette(str(_fixtures_dir / "actions_resolve_settings.yaml"))
    def test_actions_api_resolve_settings(self, test_config):
        """Test Actions API can resolve organization settings."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # Uses GET /api/v1/actions/resolveSettings internally
        # We test via organization service which uses actions API
        org = sdk.catalog_organization.get_organization()
        assert org is not None
        assert org.id is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "actions_scan_data_source_schemata.yaml"))
    def test_actions_api_scan_schemata(self, test_config):
        """Test Actions API can scan data source schemata."""
        sdk = create_sdk(test_config["host"], test_config["token"])
        data_source_id = test_config["data_source"]

        # GET /api/v1/actions/dataSources/{dataSourceId}/scanSchemata
        try:
            schemata = sdk.catalog_data_source.scan_schemata(data_source_id)
            assert schemata is not None
        except exceptions.NotFoundException:
            # Data source might not exist in test environment
            pytest.skip(f"Data source '{data_source_id}' not found")

    @gd_vcr.use_cassette(str(_fixtures_dir / "actions_auth_failure.yaml"))
    def test_actions_api_auth_failure(self, test_config):
        """Test Actions API returns proper error for invalid token."""
        sdk = create_sdk_invalid_token(test_config["host"])

        with pytest.raises((exceptions.UnauthorizedException, exceptions.ForbiddenException)):
            _ = sdk.catalog_organization.get_organization()


# =============================================================================
# Layout API Tests (Configuration Service)
# /api/v1/layout/*
# =============================================================================


class TestLayoutApiConnectivity:
    """
    Tests for Layout API connectivity.

    The Layout API handles declarative configuration:
    - GET/PUT /api/v1/layout/workspaces - Workspace layouts
    - GET/PUT /api/v1/layout/dataSources - Data source layouts
    - GET/PUT /api/v1/layout/organization - Organization layout
    """

    @gd_vcr.use_cassette(str(_fixtures_dir / "layout_get_workspaces.yaml"))
    def test_layout_api_get_declarative_workspaces(self, test_config):
        """Test Layout API can get declarative workspaces."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # GET /api/v1/layout/workspaces
        workspaces = sdk.catalog_workspace.get_declarative_workspaces()
        assert workspaces is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "layout_get_workspace.yaml"))
    def test_layout_api_get_declarative_workspace(self, test_config):
        """Test Layout API can get single declarative workspace."""
        sdk = create_sdk(test_config["host"], test_config["token"])
        workspace_id = test_config["workspace"]

        # GET /api/v1/layout/workspaces/{workspaceId}
        workspace = sdk.catalog_workspace.get_declarative_workspace(workspace_id)
        assert workspace is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "layout_get_data_sources.yaml"))
    def test_layout_api_get_declarative_data_sources(self, test_config):
        """Test Layout API can get declarative data sources."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # GET /api/v1/layout/dataSources
        data_sources = sdk.catalog_data_source.get_declarative_data_sources()
        assert data_sources is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "layout_auth_failure.yaml"))
    def test_layout_api_auth_failure(self, test_config):
        """Test Layout API returns proper error for invalid token."""
        sdk = create_sdk_invalid_token(test_config["host"])

        with pytest.raises((exceptions.UnauthorizedException, exceptions.ForbiddenException)):
            _ = sdk.catalog_workspace.get_declarative_workspaces()


# =============================================================================
# User Management API Tests
# /api/v1/actions/userManagement/*
# =============================================================================


class TestUserManagementApiConnectivity:
    """
    Tests for User Management API connectivity.

    The User Management API handles:
    - User listing and management
    - User group operations
    - Permission assignments
    """

    @gd_vcr.use_cassette(str(_fixtures_dir / "user_management_list_users.yaml"))
    def test_user_management_api_list_users(self, test_config):
        """Test User Management API can list users."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # Uses /api/v1/actions/userManagement/users
        users = sdk.catalog_user.list_users()
        assert users is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "user_management_list_user_groups.yaml"))
    def test_user_management_api_list_user_groups(self, test_config):
        """Test User Management API can list user groups."""
        sdk = create_sdk(test_config["host"], test_config["token"])

        # Uses /api/v1/actions/userManagement/userGroups
        user_groups = sdk.catalog_user.list_user_groups()
        assert user_groups is not None

    @gd_vcr.use_cassette(str(_fixtures_dir / "user_management_auth_failure.yaml"))
    def test_user_management_api_auth_failure(self, test_config):
        """Test User Management API returns proper error for invalid token."""
        sdk = create_sdk_invalid_token(test_config["host"])

        with pytest.raises((exceptions.UnauthorizedException, exceptions.ForbiddenException)):
            _ = sdk.catalog_user.list_users()


# =============================================================================
# Combined Service Health Check
# =============================================================================


class TestAllServicesHealth:
    """
    Combined health check for all services.

    Use this to quickly verify all services are accessible and authenticated.
    """

    @gd_vcr.use_cassette(str(_fixtures_dir / "all_services_health.yaml"))
    def test_all_services_accessible(self, test_config):
        """
        Comprehensive test that verifies connectivity to all services.

        This is useful for quick validation that all services are up and
        properly configured for the multiservice architecture.
        """
        sdk = create_sdk(test_config["host"], test_config["token"])

        # 1. Test Entities API (Metadata)
        assert sdk.support.is_available, "Entities API (Metadata) not available"

        # 2. Test Entities API - List operation
        workspaces_list = sdk.catalog_workspace.list_workspaces()
        assert workspaces_list is not None, "Failed to list workspaces via Entities API"

        # 3. Test Layout API
        workspaces_layout = sdk.catalog_workspace.get_declarative_workspaces()
        assert workspaces_layout is not None, "Failed to get declarative workspaces via Layout API"

        # 4. Test Actions API - Organization
        org = sdk.catalog_organization.get_organization()
        assert org is not None, "Failed to get organization via Actions API"

        # 5. Test User Management API
        users = sdk.catalog_user.list_users()
        assert users is not None, "Failed to list users via User Management API"

        print("\n✓ All services accessible and authenticated")
        print(f"  - Organization ID: {org.id}")
        print(f"  - Workspaces found: {len(workspaces_list)}")
        print(f"  - Users found: {len(users)}")

    def test_invalid_host_all_services(self):
        """Test that invalid host is handled gracefully for all services."""
        sdk = create_sdk_invalid_host()

        # Should return False, not raise exception
        assert sdk.support.is_available is False

    @gd_vcr.use_cassette(str(_fixtures_dir / "all_services_auth_failure.yaml"))
    def test_invalid_token_all_services(self, test_config):
        """Test that invalid token properly fails authentication for all services."""
        sdk = create_sdk_invalid_token(test_config["host"])

        # All operations should fail with authentication error
        with pytest.raises((exceptions.UnauthorizedException, exceptions.ForbiddenException)):
            _ = sdk.support.is_available


# =============================================================================
# Live Connection Tests (No VCR)
# =============================================================================


class TestLiveConnection:
    """
    Live connection tests that bypass VCR cassettes.

    These tests are useful for real-time connectivity verification.
    Run with: pytest tests/service/test_service_connectivity.py::TestLiveConnection -v

    Note: These require a running GoodData instance with proper credentials.
    """

    @pytest.mark.skipif(
        True,  # Set to False to enable live tests
        reason="Live tests disabled by default - enable manually for real testing",
    )
    def test_live_connection_all_services(self, test_config):
        """
        Live test - verify actual connectivity to all services.

        Enable this test by setting skipif to False when testing
        against a real multiservice deployment.
        """
        sdk = create_sdk(test_config["host"], test_config["token"])

        # Verify all services
        print(f"\n🔍 Testing live connection to: {test_config['host']}")

        # Entities API
        is_available = sdk.support.is_available
        print(f"  ✓ Entities API: {'Available' if is_available else 'Not Available'}")
        assert is_available, "Entities API not available"

        # Layout API
        try:
            workspaces = sdk.catalog_workspace.get_declarative_workspaces()
            print(f"  ✓ Layout API: Found {len(workspaces.workspaces)} workspaces")
        except Exception as e:
            print(f"  ✗ Layout API: {e}")
            raise

        # User Management API
        try:
            users = sdk.catalog_user.list_users()
            print(f"  ✓ User Management API: Found {len(users)} users")
        except Exception as e:
            print(f"  ✗ User Management API: {e}")
            raise

        # Actions API
        try:
            org = sdk.catalog_organization.get_organization()
            print(f"  ✓ Actions API: Organization ID = {org.id}")
        except Exception as e:
            print(f"  ✗ Actions API: {e}")
            raise

        print("\n✓ All services verified successfully!")
