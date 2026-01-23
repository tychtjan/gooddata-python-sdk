# (C) 2024 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any, Optional

import attr
from gooddata_api_client.model.json_api_user_setting_in import JsonApiUserSettingIn
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from gooddata_api_client.model.json_api_user_setting_out import JsonApiUserSettingOut
from gooddata_api_client.model.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserSetting(Base):
    id: str
    attributes: Optional[CatalogUserSettingAttributes] = None

    @classmethod
    def init(cls, setting_id: str, setting_type: str, content: dict[str, Any]) -> CatalogUserSetting:
        """Initialize a CatalogUserSetting with restricted access for certain settings.
        
        Some settings are restricted to workspace/organization level only and cannot be set at user level.
        
        Args:
            setting_id: The ID of the setting
            setting_type: The type of the setting
            content: The setting content
            
        Returns:
            CatalogUserSetting instance
            
        Raises:
            ValueError: If trying to set a restricted setting at user level
        """
        # Define settings that are restricted to workspace/organization level only
        restricted_settings = {
            "nullJoins",  # Based on the JIRA description about null joins setting access restrictions
        }
        
        if setting_id in restricted_settings or setting_type in restricted_settings:
            raise ValueError(
                f"Setting '{setting_id}' (type: '{setting_type}') is restricted to workspace/organization level only. "
                "It cannot be set at user level."
            )
        
        return cls(id=setting_id, attributes=CatalogUserSettingAttributes(type=setting_type, content=content))

    @staticmethod
    def client_class() -> type[JsonApiUserSettingIn]:
        return JsonApiUserSettingIn

    def to_api(self, as_document: bool = False) -> JsonApiUserSettingIn | JsonApiUserSettingInDocument:
        """Convert to API representation."""
        api_setting = JsonApiUserSettingIn(
            id=self.id,
            type="userSetting",
            attributes=self.attributes.to_api() if self.attributes else None
        )
        
        if as_document:
            return JsonApiUserSettingInDocument(data=api_setting)
        return api_setting

    @classmethod
    def from_api(cls, api_setting: JsonApiUserSettingOut) -> CatalogUserSetting:
        """Create CatalogUserSetting from API representation."""
        attributes = None
        if hasattr(api_setting, 'attributes') and api_setting.attributes:
            attributes = CatalogUserSettingAttributes.from_api(api_setting.attributes)
        
        return cls(
            id=api_setting.id,
            attributes=attributes
        )


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserSettingAttributes(Base):
    type: Optional[str] = None
    content: dict[str, Any] = attr.field(factory=dict)

    @staticmethod
    def client_class() -> builtins.type[JsonApiOrganizationSettingInAttributes]:
        return JsonApiOrganizationSettingInAttributes

    def to_api(self) -> JsonApiOrganizationSettingInAttributes:
        """Convert to API representation."""
        return JsonApiOrganizationSettingInAttributes(
            type=self.type,
            content=self.content
        )

    @classmethod
    def from_api(cls, api_attributes) -> CatalogUserSettingAttributes:
        """Create CatalogUserSettingAttributes from API representation."""
        return cls(
            type=api_attributes.type if hasattr(api_attributes, 'type') else None,
            content=api_attributes.content if hasattr(api_attributes, 'content') else {}
        )


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserSettingDocument(Base):
    data: CatalogUserSetting

    def to_api(self) -> JsonApiUserSettingInDocument:
        return JsonApiUserSettingInDocument(data=self.data.to_api())

    @staticmethod
    def client_class() -> type[JsonApiUserSettingInDocument]:
        return JsonApiUserSettingInDocument