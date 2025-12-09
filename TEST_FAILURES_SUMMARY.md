# Test Failures Summary - Multi-Service Migration

This document summarizes the remaining test failures after migrating from AIO to multi-service architecture.

## Status: 7 Failing Tests (out of 345+)

---

## 1. `test_generate_logical_model` & `test_scan_pdm_and_generate_logical_model`

**File:** `tests/catalog/test_catalog_data_source.py`

**Error:** `AssertionError: assert declarative_model.ldm.datasets == generated_declarative_model.ldm.datasets`

**Root Cause:**
The test compares the current workspace LDM with a freshly generated LDM from the database schema. The comparison fails because:

- **Current LDM** (from workspace): includes manual customizations like `locale='en-US'` and `translations=[CatalogDeclarativeLabelTranslation(locale='cs-CZ', ...)]`
- **Generated LDM** (from PDM): `locale=None`, `translations=None` - because translations are manual configurations, not derived from database schema

**Why it passed in AIO:** The old AIO demo data likely didn't include translation configurations.

**Fix Options:**
1. Modify test to compare only structural fields (ignore locale/translations)
2. Remove translations from demo workspace LDM loaded by data-loader
3. Mark as expected difference in multi-service

---

## 2. `test_catalog_create_data_source_snowflake_spec`

**File:** `tests/catalog/test_catalog_data_source.py`

**Error:** `ApiException: Status Code: 400 - "Key pair authentication is not supported."`

**Root Cause:**
The test creates a Snowflake data source using `KeyPairCredentials`. This authentication method is not supported in the multi-service environment.

**Why it passed in AIO:** AIO may have had Snowflake key pair authentication support enabled, or this feature was added later and not backported.

**Fix Options:**
1. Skip the key pair portion of the test on multi-service
2. Mark entire test as expected failure on multi-service
3. Add feature flag to enable key pair auth in multi-service (requires backend changes)

---

## 3. `test_catalog_list_aggregated_facts`

**File:** `tests/catalog/test_catalog_workspace_content.py`

**Error:** `assert 0 == 1` (expected 1 aggregated fact, got 0)

**Root Cause:**
The demo workspace in multi-service doesn't have any aggregated facts configured. The data-loader doesn't create them.

**Why it passed in AIO:** The AIO demo workspace included an aggregated fact in its LDM.

**Fix Options:**
1. Update data-loader to include aggregated facts in demo workspace
2. Update test expected value to 0
3. Skip test on multi-service

---

## 4. `test_load_ldm_and_modify_tables_columns_case`

**File:** `tests/catalog/test_catalog_workspace_content.py`

**Error:** `IndexError: list index out of range`

**Root Cause:**
The test expects certain tables/columns in the LDM that don't exist in multi-service. When it tries to access an index, the list is shorter than expected.

**Why it passed in AIO:** AIO had additional tables/columns in the demo LDM.

**Fix Options:**
1. Ensure data-loader creates the same LDM structure as AIO
2. Update test to work with available data
3. Skip test on multi-service

---

## 5. `test_get_declarative_ldm`

**File:** `tests/catalog/test_catalog_workspace_content.py`

**Error:** `AssertionError: assert False`

**Root Cause:**
The test verifies the declarative LDM matches an expected structure. The multi-service LDM differs from the expected fixture.

**Why it passed in AIO:** LDM structure matched expected fixture.

**Fix Options:**
1. Update expected fixture for multi-service LDM
2. Make comparison more lenient
3. Skip test on multi-service

---

## 6. `test_catalog_load`

**File:** `tests/catalog/test_catalog_workspace_content.py`

**Error:** `assert 6 == 7` (expected 7 catalog items, got 6)

**Root Cause:**
The demo workspace has 6 catalog items instead of the expected 7. One item is missing - likely the aggregated fact or a metric that depends on data not present in multi-service.

**Why it passed in AIO:** AIO had all 7 catalog items.

**Fix Options:**
1. Add missing catalog item to data-loader
2. Update expected count to 6
3. Skip test on multi-service

---

## Summary of Root Causes

| Category | Tests Affected | Cause |
|----------|---------------|-------|
| **LDM Translation Configs** | 2 | Demo workspace includes locale/translations that generate_ldm can't produce |
| **Feature Not Supported** | 1 | Snowflake key pair auth not available in multi-service |
| **Missing Demo Data** | 4 | Data-loader doesn't create identical demo data as AIO (aggregated facts, extra tables) |

---

## Recommended Actions

### Short-term (Get Tests Passing)
1. **For LDM tests:** Modify tests to ignore locale/translation fields when comparing
2. **For Snowflake test:** Add `pytest.mark.skip` for key pair auth portion
3. **For workspace content tests:** Update expected values or skip on multi-service

### Long-term (Full Parity)
1. Update data-loader to create identical demo workspace content as AIO
2. Enable Snowflake key pair auth in multi-service (if needed)
3. Review all test fixtures for AIO-specific assumptions

---

## Tests That Now Pass (Previously Failing)

After our fixes, the following test categories now pass:
- ✅ All user permission tests (`test_get_user_permissions`, `test_manage_user_permissions`, etc.)
- ✅ All export tests
- ✅ All table/dataframe tests
- ✅ All organization tests
- ✅ All workspace tests (except the 4 noted above)

**Total:** ~338 passing, 7 failing
