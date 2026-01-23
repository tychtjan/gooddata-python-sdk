# (C) 2022 GoodData Corporation

import pytest
from gooddata_api_client.model.attribute_item import AttributeItem
from gooddata_api_client.model.change_analysis_request import ChangeAnalysisRequest
from gooddata_api_client.model.change_analysis_params import ChangeAnalysisParams
from gooddata_api_client.model.measure_item import MeasureItem
from gooddata_api_client.model.object_identifier import ObjectIdentifier


class TestChangeAnalysisTags:
    """Test tag filtering functionality for change analysis requests."""

    def test_change_analysis_request_with_tags(self):
        """Test that ChangeAnalysisRequest accepts include_tags and exclude_tags parameters."""
        # Create test objects
        date_attribute = AttributeItem(object_identifier=ObjectIdentifier(id="date_attr", type="attribute"))
        measure = MeasureItem(object_identifier=ObjectIdentifier(id="measure1", type="measure"))
        
        include_tags = ["important", "sales"]
        exclude_tags = ["deprecated", "test"]
        
        # Create ChangeAnalysisRequest with tag filters
        request = ChangeAnalysisRequest(
            analyzed_period="2025-02",
            date_attribute=date_attribute,
            measure=measure,
            reference_period="2025-01",
            include_tags=include_tags,
            exclude_tags=exclude_tags
        )
        
        # Verify tags are set correctly
        assert request.include_tags == include_tags
        assert request.exclude_tags == exclude_tags
        
        # Verify tag attributes are in the attribute map
        assert "include_tags" in request.attribute_map
        assert "exclude_tags" in request.attribute_map
        assert request.attribute_map["include_tags"] == "includeTags"
        assert request.attribute_map["exclude_tags"] == "excludeTags"

    def test_change_analysis_params_with_tags(self):
        """Test that ChangeAnalysisParams accepts include_tags and exclude_tags parameters."""
        # Create test objects
        date_attribute = AttributeItem(object_identifier=ObjectIdentifier(id="date_attr", type="attribute"))
        measure = MeasureItem(object_identifier=ObjectIdentifier(id="measure1", type="measure"))
        
        include_tags = ["financial", "quarterly"]
        exclude_tags = ["internal", "draft"]
        
        # Create ChangeAnalysisParams with tag filters
        params = ChangeAnalysisParams(
            analyzed_period="2025-02",
            attributes=[],
            date_attribute=date_attribute,
            filters=[],
            include_tags=include_tags,
            exclude_tags=exclude_tags,
            measure=measure,
            measure_title="Revenue",
            reference_period="2025-01",
            use_smart_attribute_selection=False
        )
        
        # Verify tags are set correctly
        assert params.include_tags == include_tags
        assert params.exclude_tags == exclude_tags
        
        # Verify tag attributes are in the attribute map
        assert "include_tags" in params.attribute_map
        assert "exclude_tags" in params.attribute_map
        assert params.attribute_map["include_tags"] == "includeTags"
        assert params.attribute_map["exclude_tags"] == "excludeTags"

    def test_change_analysis_request_optional_tags(self):
        """Test that tags are optional parameters in ChangeAnalysisRequest."""
        # Create test objects
        date_attribute = AttributeItem(object_identifier=ObjectIdentifier(id="date_attr", type="attribute"))
        measure = MeasureItem(object_identifier=ObjectIdentifier(id="measure1", type="measure"))
        
        # Create ChangeAnalysisRequest without tag filters (should work)
        request = ChangeAnalysisRequest(
            analyzed_period="2025-02",
            date_attribute=date_attribute,
            measure=measure,
            reference_period="2025-01"
        )
        
        # Verify request is created successfully without tags
        assert request.analyzed_period == "2025-02"
        assert request.date_attribute == date_attribute
        assert request.measure == measure
        assert request.reference_period == "2025-01"

    def test_change_analysis_request_empty_tags(self):
        """Test ChangeAnalysisRequest with empty tag lists."""
        # Create test objects
        date_attribute = AttributeItem(object_identifier=ObjectIdentifier(id="date_attr", type="attribute"))
        measure = MeasureItem(object_identifier=ObjectIdentifier(id="measure1", type="measure"))
        
        # Create ChangeAnalysisRequest with empty tag filters
        request = ChangeAnalysisRequest(
            analyzed_period="2025-02",
            date_attribute=date_attribute,
            measure=measure,
            reference_period="2025-01",
            include_tags=[],
            exclude_tags=[]
        )
        
        # Verify empty tags are set correctly
        assert request.include_tags == []
        assert request.exclude_tags == []

    def test_change_analysis_openapi_types_include_tags(self):
        """Test that include_tags and exclude_tags are defined in openapi_types."""
        # Check ChangeAnalysisRequest types
        request_types = ChangeAnalysisRequest.openapi_types()
        assert "include_tags" in request_types
        assert "exclude_tags" in request_types
        assert request_types["include_tags"] == ([str],)
        assert request_types["exclude_tags"] == ([str],)
        
        # Check ChangeAnalysisParams types
        params_types = ChangeAnalysisParams.openapi_types()
        assert "include_tags" in params_types
        assert "exclude_tags" in params_types
        assert params_types["include_tags"] == ([str],)
        assert params_types["exclude_tags"] == ([str],)