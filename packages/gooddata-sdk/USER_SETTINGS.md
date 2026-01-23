# User Settings SDK Implementation

## Overview

The GoodData SDK now supports user settings management through the `CatalogUserSetting` entity model and related service methods in `CatalogUserService`.

## Features

### User Setting Entity Model

- **CatalogUserSetting**: Represents a user-level configuration setting
- Supports all standard setting types available in the GoodData platform
- Includes validation to restrict certain settings to workspace/organization level only

### Restricted Settings

The following settings are **restricted** from being set at the user level and can only be configured at workspace or organization level:

- `nullJoins` / `NULL_JOINS` - Null joins handling strategy
- `joinStrategy` / `JOIN_STRATEGY` - Join strategy configuration

### Service Methods

The `CatalogUserService` includes the following methods for user settings management:

- `create_or_update_user_setting(user_id, user_setting)` - Create or update a user setting
- `get_user_setting(user_id, setting_id)` - Retrieve a specific user setting
- `delete_user_setting(user_id, setting_id)` - Delete a user setting
- `list_user_settings(user_id)` - List all settings for a user

## Usage Examples

```python
from gooddata_sdk import GoodDataSdk, CatalogUserSetting

# Initialize SDK
sdk = GoodDataSdk(host="https://example.gooddata.com", token="your-token")

# Create a user setting
user_setting = CatalogUserSetting(
    id="locale",
    setting_type="LOCALE", 
    content={"value": "en-US"}
)

# Create or update the setting for a user
sdk.catalog_user.create_or_update_user_setting("user123", user_setting)

# List all user settings
settings = sdk.catalog_user.list_user_settings("user123")

# Get a specific setting
locale_setting = sdk.catalog_user.get_user_setting("user123", "locale")

# Delete a setting
sdk.catalog_user.delete_user_setting("user123", "locale")
```

## Validation

The SDK automatically validates that restricted settings cannot be created at the user level:

```python
# This will raise a ValueError
try:
    restricted_setting = CatalogUserSetting(
        id="nullJoins",
        setting_type="NULL_JOINS",
        content={"enabled": True}
    )
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Setting 'nullJoins' is restricted to workspace/organization level only
```

## Implementation Notes

- User settings follow the same pattern as workspace settings but with user-level scope
- The implementation includes comprehensive validation to enforce setting-level restrictions
- All methods handle API exceptions gracefully (e.g., NotFoundException for missing settings)
- The entity model supports both creation from API responses and manual instantiation