# (C) 2022 GoodData Corporation
import pytest

from gooddata_sdk.catalog.user.entity_model.user_setting import CatalogUserSetting


class TestCatalogUserSetting:
    def test_user_setting_creation(self):
        """Test creating a valid user setting."""
        setting = CatalogUserSetting(
            id="locale",
            setting_type="LOCALE",
            content={"value": "en-US"}
        )
        
        assert setting.id == "locale"
        assert setting.setting_type == "LOCALE"
        assert setting.content == {"value": "en-US"}

    def test_restricted_setting_null_joins_by_id(self):
        """Test that null joins setting is restricted when specified by id."""
        with pytest.raises(ValueError, match="Setting 'nullJoins' is restricted to workspace/organization level only"):
            CatalogUserSetting(
                id="nullJoins",
                setting_type="NULL_JOINS",
                content={"enabled": True}
            )

    def test_restricted_setting_null_joins_by_type(self):
        """Test that null joins setting is restricted when specified by type."""
        with pytest.raises(ValueError, match="Setting 'nullJoins' is restricted to workspace/organization level only"):
            CatalogUserSetting(
                id="custom_id",
                setting_type="nullJoins",
                content={"enabled": True}
            )

    def test_restricted_setting_null_joins_uppercase(self):
        """Test that NULL_JOINS setting is also restricted."""
        with pytest.raises(ValueError, match="Setting 'NULL_JOINS' is restricted to workspace/organization level only"):
            CatalogUserSetting(
                id="null_joins_setting",
                setting_type="NULL_JOINS",
                content={"enabled": True}
            )

    def test_restricted_setting_join_strategy(self):
        """Test that join strategy settings are also restricted."""
        with pytest.raises(ValueError, match="Setting 'JOIN_STRATEGY' is restricted to workspace/organization level only"):
            CatalogUserSetting(
                id="join_setting",
                setting_type="JOIN_STRATEGY",
                content={"strategy": "inner"}
            )

    def test_allowed_setting_passes(self):
        """Test that non-restricted settings work normally."""
        setting = CatalogUserSetting(
            id="timezone",
            setting_type="TIMEZONE",
            content={"value": "America/New_York"}
        )
        
        assert setting.id == "timezone"
        assert setting.setting_type == "TIMEZONE"

    def test_from_api_method(self):
        """Test the from_api class method."""
        api_entity = {
            "id": "locale",
            "attributes": {
                "type": "LOCALE",
                "content": {"value": "en-US"}
            }
        }
        
        setting = CatalogUserSetting.from_api(api_entity)
        
        assert setting.id == "locale"
        assert setting.setting_type == "LOCALE"
        assert setting.content == {"value": "en-US"}

    def test_from_api_restricted_setting(self):
        """Test that restricted settings are caught even when created from API."""
        api_entity = {
            "id": "nullJoins",
            "attributes": {
                "type": "NULL_JOINS",
                "content": {"enabled": True}
            }
        }
        
        with pytest.raises(ValueError, match="Setting 'nullJoins' is restricted to workspace/organization level only"):
            CatalogUserSetting.from_api(api_entity)