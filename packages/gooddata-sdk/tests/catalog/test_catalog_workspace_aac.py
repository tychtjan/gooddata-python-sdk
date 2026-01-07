# (C) 2026 GoodData Corporation
"""Unit tests for AAC (Analytics as Code) layout API methods."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from gooddata_sdk.catalog.workspace.content_service import CatalogWorkspaceContentService


class TestCatalogWorkspaceAac:
    """Tests for AAC layout API methods in CatalogWorkspaceContentService."""

    @pytest.fixture
    def mock_api_client(self):
        """Create a mock GoodDataApiClient."""
        mock_client = MagicMock()
        mock_client.entities_api = MagicMock()
        mock_client.layout_api = MagicMock()
        mock_client.actions_api = MagicMock()
        mock_client.user_management_api = MagicMock()
        mock_client.aac_api = MagicMock()
        return mock_client

    @pytest.fixture
    def content_service(self, mock_api_client):
        """Create a CatalogWorkspaceContentService with mocked client."""
        return CatalogWorkspaceContentService(mock_api_client)

    @pytest.fixture
    def sample_aac_logical_model(self):
        """Sample AAC logical model for testing."""
        mock_model = MagicMock()
        mock_model.datasets = []
        mock_model.date_datasets = []
        return mock_model

    @pytest.fixture
    def sample_aac_analytics_model(self):
        """Sample AAC analytics model for testing."""
        mock_model = MagicMock()
        mock_model.metrics = []
        mock_model.visualizations = []
        mock_model.dashboards = []
        mock_model.attribute_hierarchies = []
        mock_model.plugins = []
        return mock_model

    # GET logical model tests

    def test_get_aac_logical_model_returns_model(self, content_service, sample_aac_logical_model):
        """Test that get_aac_logical_model returns an AacLogicalModel."""
        content_service._aac_api.get_logical_model_aac.return_value = sample_aac_logical_model

        result = content_service.get_aac_logical_model("test_workspace")

        assert result is not None
        assert result == sample_aac_logical_model
        content_service._aac_api.get_logical_model_aac.assert_called_once_with(
            workspace_id="test_workspace",
            include_parents=False,
        )

    def test_get_aac_logical_model_with_include_parents(self, content_service, sample_aac_logical_model):
        """Test that include_parents parameter is passed correctly."""
        content_service._aac_api.get_logical_model_aac.return_value = sample_aac_logical_model

        content_service.get_aac_logical_model("ws", include_parents=True)

        content_service._aac_api.get_logical_model_aac.assert_called_once_with(
            workspace_id="ws",
            include_parents=True,
        )

    # PUT logical model tests

    def test_put_aac_logical_model_calls_api(self, content_service, sample_aac_logical_model):
        """Test that put_aac_logical_model calls the API correctly."""
        content_service.put_aac_logical_model("test_workspace", sample_aac_logical_model)

        content_service._aac_api.set_logical_model_aac.assert_called_once_with(
            workspace_id="test_workspace",
            aac_logical_model=sample_aac_logical_model,
        )

    # GET analytics model tests

    def test_get_aac_analytics_model_returns_model(self, content_service, sample_aac_analytics_model):
        """Test that get_aac_analytics_model returns an AacAnalyticsModel."""
        content_service._aac_api.get_analytics_model_aac.return_value = sample_aac_analytics_model

        result = content_service.get_aac_analytics_model("test_workspace")

        assert result is not None
        assert result == sample_aac_analytics_model
        content_service._aac_api.get_analytics_model_aac.assert_called_once_with(
            workspace_id="test_workspace",
        )

    def test_get_aac_analytics_model_with_exclude(self, content_service, sample_aac_analytics_model):
        """Test that exclude parameter is passed correctly."""
        content_service._aac_api.get_analytics_model_aac.return_value = sample_aac_analytics_model

        content_service.get_aac_analytics_model("ws", exclude=["ACTIVITY_INFO"])

        content_service._aac_api.get_analytics_model_aac.assert_called_once_with(
            workspace_id="ws",
            exclude=["ACTIVITY_INFO"],
        )

    # PUT analytics model tests

    def test_put_aac_analytics_model_calls_api(self, content_service, sample_aac_analytics_model):
        """Test that put_aac_analytics_model calls the API correctly."""
        content_service.put_aac_analytics_model("test_workspace", sample_aac_analytics_model)

        content_service._aac_api.set_analytics_model_aac.assert_called_once_with(
            workspace_id="test_workspace",
            aac_analytics_model=sample_aac_analytics_model,
        )


class TestCatalogDataSourceAac:
    """Tests for AAC methods in CatalogDataSourceService."""

    @pytest.fixture
    def mock_api_client(self):
        """Create a mock GoodDataApiClient."""
        mock_client = MagicMock()
        mock_client.entities_api = MagicMock()
        mock_client.layout_api = MagicMock()
        mock_client.actions_api = MagicMock()
        mock_client.user_management_api = MagicMock()
        mock_client.aac_api = MagicMock()
        return mock_client

    @pytest.fixture
    def data_source_service(self, mock_api_client):
        """Create a CatalogDataSourceService with mocked client."""
        from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService

        return CatalogDataSourceService(mock_api_client)

    @pytest.fixture
    def sample_aac_logical_model(self):
        """Sample AAC logical model for testing."""
        mock_model = MagicMock()
        mock_model.datasets = []
        mock_model.date_datasets = []
        return mock_model

    def test_generate_logical_model_aac_returns_model(self, data_source_service, sample_aac_logical_model):
        """Test that generate_logical_model_aac returns AacLogicalModel."""
        data_source_service._actions_api.generate_logical_model_aac.return_value = sample_aac_logical_model

        result = data_source_service.generate_logical_model_aac("test_datasource")

        assert result is not None
        assert result == sample_aac_logical_model
        data_source_service._actions_api.generate_logical_model_aac.assert_called_once()

    def test_generate_logical_model_aac_with_custom_request(self, data_source_service, sample_aac_logical_model):
        """Test generate_logical_model_aac with custom LDM request."""
        from gooddata_sdk.catalog.data_source.action_model.requests.ldm_request import CatalogGenerateLdmRequest

        data_source_service._actions_api.generate_logical_model_aac.return_value = sample_aac_logical_model
        custom_request = CatalogGenerateLdmRequest(separator="_", wdf_prefix="custom")

        data_source_service.generate_logical_model_aac("test_datasource", custom_request)

        data_source_service._actions_api.generate_logical_model_aac.assert_called_once()
        call_args = data_source_service._actions_api.generate_logical_model_aac.call_args
        assert call_args[0][0] == "test_datasource"
