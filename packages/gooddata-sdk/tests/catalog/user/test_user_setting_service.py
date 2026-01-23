# (C) 2022 GoodData Corporation
import pytest
from unittest.mock import Mock, patch

from gooddata_sdk.catalog.user.entity_model.user_setting import CatalogUserSetting
from gooddata_sdk.catalog.user.service import CatalogUserService


class TestCatalogUserSettingService:
    def test_create_or_update_user_setting_restricted(self):
        """Test that creating a restricted user setting raises an error."""
        service = Mock(spec=CatalogUserService)
        
        with pytest.raises(ValueError, match="Setting 'nullJoins' is restricted to workspace/organization level only"):
            CatalogUserSetting(
                id="nullJoins",
                setting_type="NULL_JOINS",
                content={"enabled": True}
            )

    def test_user_setting_validation_message(self):
        """Test that the validation message is informative."""
        expected_msg = "Setting 'nullJoins' is restricted to workspace/organization level only"
        
        with pytest.raises(ValueError, match=expected_msg):
            CatalogUserSetting(
                id="nullJoins",
                setting_type="LOCALE",
                content={"value": "en-US"}
            )

    def test_allowed_user_setting_creation(self):
        """Test that allowed user settings can be created normally."""
        # This should not raise any exception
        setting = CatalogUserSetting(
            id="timezone",
            setting_type="TIMEZONE",
            content={"value": "America/New_York"}
        )
        
        assert setting.id == "timezone"
        assert setting.setting_type == "TIMEZONE"