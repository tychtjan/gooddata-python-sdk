#!/usr/bin/env python3

import sys
import os

# Add the package to path for testing
sys.path.insert(0, 'packages/gooddata-sdk/src')

try:
    # Test basic imports
    print("Testing imports...")
    
    from gooddata_sdk.catalog.user.entity_model.user_setting import CatalogUserSetting
    print("✓ CatalogUserSetting import successful")
    
    from gooddata_sdk.catalog.user.service import CatalogUserService
    print("✓ CatalogUserService import successful")
    
    from gooddata_sdk.catalog.user import CatalogUserSetting as UserSettingAlias
    print("✓ CatalogUserSetting import from user package successful")
    
    # Test basic functionality
    print("\nTesting basic functionality...")
    
    # Test valid setting creation
    valid_setting = CatalogUserSetting(
        id="locale",
        setting_type="LOCALE",
        content={"value": "en-US"}
    )
    print("✓ Valid setting creation successful")
    
    # Test restriction validation
    try:
        restricted_setting = CatalogUserSetting(
            id="nullJoins",
            setting_type="NULL_JOINS", 
            content={"enabled": True}
        )
        print("✗ Restriction validation failed - should have raised ValueError")
        sys.exit(1)
    except ValueError as e:
        if "restricted to workspace/organization level only" in str(e):
            print("✓ Restriction validation working correctly")
        else:
            print(f"✗ Unexpected validation error: {e}")
            sys.exit(1)
    
    # Test to_api method
    api_doc = valid_setting.to_api()
    print("✓ to_api method successful")
    
    # Test from_api method 
    api_entity = {
        "id": "timezone",
        "attributes": {
            "type": "TIMEZONE",
            "content": {"value": "America/New_York"}
        }
    }
    
    setting_from_api = CatalogUserSetting.from_api(api_entity)
    assert setting_from_api.id == "timezone"
    assert setting_from_api.setting_type == "TIMEZONE"
    assert setting_from_api.content == {"value": "America/New_York"}
    print("✓ from_api method successful")
    
    print("\n🎉 All tests passed! Implementation looks good.")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)