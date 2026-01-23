# (C) 2022 GoodData Corporation
import pytest
from unittest.mock import Mock, MagicMock, patch

from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk.catalog.user.entity_model.user_setting import CatalogUserSetting
from gooddata_sdk.catalog.user.service import CatalogUserService
from gooddata_sdk.client import GoodDataApiClient


class TestCatalogUserSettingIntegration:
    @patch('gooddata_sdk.catalog.user.service.load_all_entities')
    def test_list_user_settings(self, mock_load_all_entities):
        """Test listing user settings."""
        # Mock the API client and entities API
        api_client = Mock(spec=GoodDataApiClient)
        entities_api = Mock()
        api_client.entities_api = entities_api
        
        # Mock the response data
        mock_load_all_entities.return_value.data = [
            {
                "id": "locale",
                "attributes": {
                    "type": "LOCALE", 
                    "content": {"value": "en-US"}
                }
            },
            {
                "id": "timezone",
                "attributes": {
                    "type": "TIMEZONE",
                    "content": {"value": "America/New_York"}
                }
            }
        ]
        
        # Create service instance
        service = CatalogUserService(api_client)
        service._entities_api = entities_api
        
        # Call the method
        settings = service.list_user_settings("user123")
        
        # Verify results
        assert len(settings) == 2
        assert settings[0].id == "locale"
        assert settings[0].setting_type == "LOCALE"
        assert settings[1].id == "timezone"
        assert settings[1].setting_type == "TIMEZONE"

    def test_create_or_update_user_setting_new(self):
        """Test creating a new user setting."""
        # Mock the API client and entities API
        api_client = Mock(spec=GoodDataApiClient)
        entities_api = Mock()
        api_client.entities_api = entities_api
        
        # Mock get_user_setting to raise NotFoundException (setting doesn't exist)
        entities_api.get_entity_user_settings.side_effect = NotFoundException()
        
        # Create service instance
        service = CatalogUserService(api_client)
        service._entities_api = entities_api
        service.get_user_setting = Mock(side_effect=NotFoundException())
        
        # Create a valid user setting
        setting = CatalogUserSetting(
            id="locale",
            setting_type="LOCALE",
            content={"value": "en-US"}
        )
        
        # Call the method
        service.create_or_update_user_setting("user123", setting)
        
        # Verify that create was called
        entities_api.create_entity_user_settings.assert_called_once()

    def test_create_or_update_user_setting_update(self):
        """Test updating an existing user setting."""
        # Mock the API client and entities API
        api_client = Mock(spec=GoodDataApiClient)
        entities_api = Mock()
        api_client.entities_api = entities_api
        
        # Create service instance
        service = CatalogUserService(api_client)
        service._entities_api = entities_api
        
        # Mock get_user_setting to return existing setting
        existing_setting = CatalogUserSetting(
            id="locale",
            setting_type="LOCALE",
            content={"value": "fr-FR"}
        )
        service.get_user_setting = Mock(return_value=existing_setting)
        
        # Create updated setting
        updated_setting = CatalogUserSetting(
            id="locale",
            setting_type="LOCALE",
            content={"value": "en-US"}
        )
        
        # Call the method
        service.create_or_update_user_setting("user123", updated_setting)
        
        # Verify that update was called
        entities_api.update_entity_user_settings.assert_called_once()

    def test_delete_user_setting(self):
        """Test deleting a user setting."""
        # Mock the API client and entities API
        api_client = Mock(spec=GoodDataApiClient)
        entities_api = Mock()
        api_client.entities_api = entities_api
        
        # Create service instance
        service = CatalogUserService(api_client)
        service._entities_api = entities_api
        
        # Call the method
        service.delete_user_setting("user123", "locale")
        
        # Verify that delete was called
        entities_api.delete_entity_user_settings.assert_called_once_with("user123", "locale")

    def test_get_user_setting(self):
        """Test getting a specific user setting."""
        # Mock the API client and entities API
        api_client = Mock(spec=GoodDataApiClient)
        entities_api = Mock()
        api_client.entities_api = entities_api
        
        # Mock the API response
        mock_response = Mock()
        mock_response.data = {
            "id": "locale",
            "attributes": {
                "type": "LOCALE",
                "content": {"value": "en-US"}
            }
        }
        entities_api.get_entity_user_settings.return_value = mock_response
        
        # Create service instance
        service = CatalogUserService(api_client)
        service._entities_api = entities_api
        
        # Call the method
        setting = service.get_user_setting("user123", "locale")
        
        # Verify results
        assert setting.id == "locale"
        assert setting.setting_type == "LOCALE"
        assert setting.content == {"value": "en-US"}
        entities_api.get_entity_user_settings.assert_called_once_with("user123", "locale")