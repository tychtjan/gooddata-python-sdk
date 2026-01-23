# User Settings API

The GoodData SDK now supports user-specific settings management with access restrictions for certain settings.

## Features

- CRUD operations for user settings (Create, Read, Update, Delete)
- Access restrictions for workspace/organization-level settings
- Type-safe API with proper validation

## Usage Examples

### Creating User Settings

```python
from gooddata_sdk import GoodDataSdk, CatalogUserSetting

# Initialize SDK
sdk = GoodDataSdk.create(host="http://localhost:3000", token="your_token")

# Create a locale setting for a user
locale_setting = CatalogUserSetting.init(
    setting_id="locale",
    setting_type="LOCALE",
    content={"value": "en-US"}
)

# Apply the setting to a user
sdk.catalog_user.create_or_update_user_setting("user123", locale_setting)
```

### Retrieving User Settings

```python
# Get a specific user setting
setting = sdk.catalog_user.get_user_setting("user123", "locale")
print(f"Locale setting: {setting.attributes.content}")

# List all settings for a user
all_settings = sdk.catalog_user.list_user_settings("user123")
for setting in all_settings:
    print(f"Setting {setting.id}: {setting.attributes.content}")
```

### Updating User Settings

```python
# Update an existing setting
updated_setting = CatalogUserSetting.init(
    setting_id="locale",
    setting_type="LOCALE",
    content={"value": "de-DE"}
)
sdk.catalog_user.create_or_update_user_setting("user123", updated_setting)
```

### Deleting User Settings

```python
# Delete a user setting
sdk.catalog_user.delete_user_setting("user123", "locale")
```

## Access Restrictions

Some settings are restricted to workspace or organization level only and cannot be set at the user level:

- `nullJoins` - Controls null join behavior, restricted to workspace/organization level

```python
# This will raise a ValueError
try:
    restricted_setting = CatalogUserSetting.init(
        setting_id="nullJoins",
        setting_type="BOOLEAN", 
        content={"value": True}
    )
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Setting 'nullJoins' (type: 'BOOLEAN') is restricted to workspace/organization level only.
```

## API Reference

### CatalogUserSetting.init()

Creates a new user setting with validation.

**Parameters:**
- `setting_id` (str): The ID of the setting
- `setting_type` (str): The type of the setting
- `content` (dict): The setting content/value

**Raises:**
- `ValueError`: If the setting is restricted to workspace/organization level

### Service Methods

#### create_or_update_user_setting(user_id, user_setting)
Creates a new user setting or updates an existing one.

#### get_user_setting(user_id, user_setting_id)
Retrieves a specific user setting.

#### list_user_settings(user_id)
Lists all settings for a user.

#### delete_user_setting(user_id, user_setting_id)
Deletes a user setting.