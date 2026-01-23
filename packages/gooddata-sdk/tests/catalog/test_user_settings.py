# (C) 2024 GoodData Corporation
"""
Test module for user settings functionality.
"""

import pytest
from gooddata_sdk.catalog.user.entity_model.user_setting import CatalogUserSetting


class TestUserSettingAccessRestrictions:
    """Test user setting access restrictions functionality."""

    def test_restricted_setting_by_id(self):
        """Test that restricted settings cannot be set at user level by ID."""
        with pytest.raises(ValueError, match="Setting 'nullJoins'.*restricted to workspace/organization level"):
            CatalogUserSetting.init(
                setting_id="nullJoins",
                setting_type="BOOLEAN",
                content={"value": True}
            )

    def test_restricted_setting_by_type(self):
        """Test that restricted settings cannot be set at user level by type."""
        with pytest.raises(ValueError, match="Setting 'someId'.*restricted to workspace/organization level"):
            CatalogUserSetting.init(
                setting_id="someId", 
                setting_type="nullJoins",
                content={"value": True}
            )

    def test_allowed_setting(self):
        """Test that non-restricted settings can be set at user level."""
        user_setting = CatalogUserSetting.init(
            setting_id="locale",
            setting_type="LOCALE", 
            content={"value": "en-US"}
        )
        assert user_setting.id == "locale"
        assert user_setting.attributes.type == "LOCALE"
        assert user_setting.attributes.content == {"value": "en-US"}

    def test_allowed_setting_empty_content(self):
        """Test that settings can be created with empty content."""
        user_setting = CatalogUserSetting.init(
            setting_id="theme",
            setting_type="THEME", 
            content={}
        )
        assert user_setting.id == "theme"
        assert user_setting.attributes.type == "THEME"
        assert user_setting.attributes.content == {}

    def test_to_api_conversion(self):
        """Test conversion to API representation."""
        user_setting = CatalogUserSetting.init(
            setting_id="locale",
            setting_type="LOCALE",
            content={"value": "en-US"}
        )
        
        api_setting = user_setting.to_api()
        assert api_setting.id == "locale"
        assert api_setting.type == "userSetting"
        assert api_setting.attributes.type == "LOCALE"
        assert api_setting.attributes.content == {"value": "en-US"}

    def test_to_api_document_conversion(self):
        """Test conversion to API document representation."""
        user_setting = CatalogUserSetting.init(
            setting_id="locale",
            setting_type="LOCALE",
            content={"value": "en-US"}
        )
        
        api_document = user_setting.to_api(as_document=True)
        assert hasattr(api_document, 'data')
        assert api_document.data.id == "locale"
        assert api_document.data.type == "userSetting"

    def test_setting_without_attributes(self):
        """Test user setting creation without attributes."""
        user_setting = CatalogUserSetting(id="test_setting")
        assert user_setting.id == "test_setting"
        assert user_setting.attributes is None
        
        # Should handle None attributes gracefully in API conversion
        api_setting = user_setting.to_api()
        assert api_setting.id == "test_setting"
        assert api_setting.type == "userSetting"
        assert api_setting.attributes is None