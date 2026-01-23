# Change Analysis Tag Filtering Implementation

## Overview
This implementation adds include/exclude tag filtering to change analysis requests, allowing users to filter which attributes and measures are considered during change analysis based on their assigned tags.

## Changes Made

### API Client Models Updated

#### ChangeAnalysisRequest (`gooddata-api-client/gooddata_api_client/model/change_analysis_request.py`)
- Added `include_tags` field: `([str],)` - Tags to include in the analysis
- Added `exclude_tags` field: `([str],)` - Tags to exclude from the analysis
- Updated `attribute_map` with proper JSON field mapping:
  - `include_tags` → `includeTags`
  - `exclude_tags` → `excludeTags`
- Updated both `_from_openapi_data` and `__init__` method documentation

#### ChangeAnalysisParams (`gooddata-api-client/gooddata_api_client/model/change_analysis_params.py`)
- Added `include_tags` field: `([str],)` - Tags to include in the analysis
- Added `exclude_tags` field: `([str],)` - Tags to exclude from the analysis
- Updated `attribute_map` with proper JSON field mapping
- Updated method signatures to include the new parameters
- Updated both `_from_openapi_data` and `__init__` method documentation

### Testing
- Created comprehensive unit tests in `packages/gooddata-sdk/tests/compute/test_change_analysis_tags.py`
- Tests cover both required and optional usage patterns
- Validates proper type definitions and attribute mapping

### Documentation
- Created usage example in `docs/examples/change_analysis_with_tags.py`
- Shows practical examples of tag filtering patterns:
  - Basic include/exclude filtering
  - Business-area focused analysis
  - Quality-focused analysis excluding unreliable data

## Usage Examples

### Basic Usage
```python
from gooddata_api_client.model.change_analysis_request import ChangeAnalysisRequest

request = ChangeAnalysisRequest(
    analyzed_period="2025-02",
    reference_period="2025-01",
    date_attribute=date_attribute,
    measure=measure,
    include_tags=["financial", "important"],
    exclude_tags=["deprecated", "test"]
)
```

### Include/Exclude Logic
- `include_tags`: Only attributes and measures with at least one of these tags will be considered
- `exclude_tags`: Attributes and measures with any of these tags will be filtered out
- If both are specified, include filtering is applied first, then exclude filtering
- Both parameters are optional arrays of strings

## Backward Compatibility
- All changes are backward compatible
- The new tag filtering parameters are optional
- Existing code will continue to work without modification

## API Compatibility
- Field names in JSON match the backend API specification:
  - `includeTags` (camelCase in JSON)
  - `excludeTags` (camelCase in JSON)
- Python field names follow SDK conventions:
  - `include_tags` (snake_case in Python)
  - `exclude_tags` (snake_case in Python)