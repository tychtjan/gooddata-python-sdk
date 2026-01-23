# (C) 2022 GoodData Corporation
from __future__ import annotations

import functools
from typing import Any

import attr
from gooddata_api_client.model.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes
from gooddata_api_client.model.json_api_user_setting_in import JsonApiUserSettingIn
from gooddata_api_client.model.json_api_user_setting_in_document import JsonApiUserSettingInDocument
from gooddata_api_client.model.json_api_user_setting_out import JsonApiUserSettingOut

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.utils import safeget


# List of settings that are restricted from being set at user level
_RESTRICTED_USER_SETTINGS = {
    "nullJoins",  # Null joins setting should only be at workspace/organization level
    "NULL_JOINS",  # Alternative naming convention
    "joinStrategy",  # Alternative name for join strategies
    "JOIN_STRATEGY",  # Alternative naming convention
}


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserSetting(Base):
    id: str = attr.field(default=None)
    setting_type: str = attr.field(
        validator=functools.partial(value_in_allowed, client_class=JsonApiOrganizationSettingInAttributes)
    )
    content: dict = attr.field(
        repr=False,
        default=attr.Factory(lambda self: safeget(self.json_api_entity.attributes, ["content"]), takes_self=True),
    )

    @staticmethod
    def client_class() -> type[JsonApiUserSettingOut]:
        return JsonApiUserSettingOut

    def _attributes(self) -> JsonApiOrganizationSettingInAttributes:
        return JsonApiOrganizationSettingInAttributes(
            content=self.content,
            type=self.setting_type,
        )

    def __attrs_post_init__(self) -> None:
        """Validate that restricted settings are not set at user level."""
        if self.id in _RESTRICTED_USER_SETTINGS or self.setting_type in _RESTRICTED_USER_SETTINGS:
            raise ValueError(
                f"Setting '{self.id or self.setting_type}' is restricted to workspace/organization level only"
            )

    def to_api(self) -> JsonApiUserSettingInDocument:
        return JsonApiUserSettingInDocument(
            data=JsonApiUserSettingIn(id=self.id, attributes=self._attributes())
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogUserSetting:
        return cls(
            id=entity["id"],
            setting_type=entity["attributes"]["type"],
            content=entity["attributes"]["content"],
        )