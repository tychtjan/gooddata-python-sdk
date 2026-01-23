# (C) 2024 GoodData Corporation
"""Tests for ENABLE_NULL_JOINS setting support."""

import pytest
from gooddata_sdk.catalog.setting import CatalogDeclarativeSetting


def test_enable_null_joins_setting():
    """Test that ENABLE_NULL_JOINS setting can be created."""
    setting = CatalogDeclarativeSetting(
        id="enable_null_joins_test",
        type="ENABLE_NULL_JOINS",
        content={"enabled": True}
    )
    
    assert setting.id == "enable_null_joins_test"
    assert setting.type == "ENABLE_NULL_JOINS"
    assert setting.content == {"enabled": True}
    
    # Test conversion to API object
    api_obj = setting.to_api()
    assert api_obj is not None
    
    # Test that the API object has the correct class
    assert setting.client_class().__name__ == "DeclarativeSetting"


def test_enable_null_joins_setting_validation():
    """Test that the ENABLE_NULL_JOINS setting type is valid."""
    # This should not raise a validation error
    setting = CatalogDeclarativeSetting(
        id="enable_null_joins_validation_test", 
        type="ENABLE_NULL_JOINS"
    )
    
    assert setting.type == "ENABLE_NULL_JOINS"