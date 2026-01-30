# gooddata_api_client.OtherApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_geo_file**](OtherApi.md#convert_geo_file) | **POST** /api/v1/actions/customGeoCollection/convert | Convert a geo file to GeoParquet format
[**create_entity_custom_geo_collections**](OtherApi.md#create_entity_custom_geo_collections) | **POST** /api/v1/entities/customGeoCollections | 
[**create_entity_knowledge_recommendations**](OtherApi.md#create_entity_knowledge_recommendations) | **POST** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations | 
[**create_entity_memory_items**](OtherApi.md#create_entity_memory_items) | **POST** /api/v1/entities/workspaces/{workspaceId}/memoryItems | 
[**custom_geo_collection_staging_upload**](OtherApi.md#custom_geo_collection_staging_upload) | **POST** /api/v1/actions/customGeoCollection/staging/upload | Upload a geo collection file to the staging area
[**delete_entity_custom_geo_collections**](OtherApi.md#delete_entity_custom_geo_collections) | **DELETE** /api/v1/entities/customGeoCollections/{id} | 
[**delete_entity_knowledge_recommendations**](OtherApi.md#delete_entity_knowledge_recommendations) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**delete_entity_memory_items**](OtherApi.md#delete_entity_memory_items) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 
[**deprovision_ai_lake_database_instance**](OtherApi.md#deprovision_ai_lake_database_instance) | **DELETE** /api/v1/ailake/database/instance/{instanceId} | (BETA) Delete an existing AILake Database instance
[**get_ai_lake_database_instance**](OtherApi.md#get_ai_lake_database_instance) | **GET** /api/v1/ailake/database/instance/{instanceId} | (BETA) Get the specified AILake Database instance
[**get_ai_lake_operation**](OtherApi.md#get_ai_lake_operation) | **GET** /api/v1/ailake/operation/{operationId} | (BETA) Get Long Running Operation details
[**get_all_entities_custom_geo_collections**](OtherApi.md#get_all_entities_custom_geo_collections) | **GET** /api/v1/entities/customGeoCollections | 
[**get_all_entities_knowledge_recommendations**](OtherApi.md#get_all_entities_knowledge_recommendations) | **GET** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations | 
[**get_all_entities_memory_items**](OtherApi.md#get_all_entities_memory_items) | **GET** /api/v1/entities/workspaces/{workspaceId}/memoryItems | 
[**get_analytics_model_aac**](OtherApi.md#get_analytics_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Get analytics model in AAC format
[**get_collection_items**](OtherApi.md#get_collection_items) | **GET** /api/v1/location/collections/{collectionId}/items | Get collection features
[**get_custom_collection_items**](OtherApi.md#get_custom_collection_items) | **GET** /api/v1/location/custom/collections/{collectionId}/items | Get custom collection features
[**get_entity_custom_geo_collections**](OtherApi.md#get_entity_custom_geo_collections) | **GET** /api/v1/entities/customGeoCollections/{id} | 
[**get_entity_knowledge_recommendations**](OtherApi.md#get_entity_knowledge_recommendations) | **GET** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**get_entity_memory_items**](OtherApi.md#get_entity_memory_items) | **GET** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 
[**get_logical_model_aac**](OtherApi.md#get_logical_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Get logical model in AAC format
[**get_user_data_filters**](OtherApi.md#get_user_data_filters) | **GET** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Get user data filters
[**import_custom_geo_collection**](OtherApi.md#import_custom_geo_collection) | **POST** /api/v1/actions/customGeoCollection/{collectionId}/import | Import custom geo collection
[**metadata_check_organization**](OtherApi.md#metadata_check_organization) | **POST** /api/v1/actions/organization/metadataCheck | (BETA) Check Organization Metadata Inconsistencies
[**metadata_sync**](OtherApi.md#metadata_sync) | **POST** /api/v1/actions/workspaces/{workspaceId}/metadataSync | (BETA) Sync Metadata to other services
[**metadata_sync_organization**](OtherApi.md#metadata_sync_organization) | **POST** /api/v1/actions/organization/metadataSync | (BETA) Sync organization scope Metadata to other services
[**patch_entity_custom_geo_collections**](OtherApi.md#patch_entity_custom_geo_collections) | **PATCH** /api/v1/entities/customGeoCollections/{id} | 
[**patch_entity_knowledge_recommendations**](OtherApi.md#patch_entity_knowledge_recommendations) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**patch_entity_memory_items**](OtherApi.md#patch_entity_memory_items) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 
[**provision_ai_lake_database_instance**](OtherApi.md#provision_ai_lake_database_instance) | **POST** /api/v1/ailake/database/instance | (BETA) Create a new AILake Database instance
[**search_entities_knowledge_recommendations**](OtherApi.md#search_entities_knowledge_recommendations) | **POST** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/search | 
[**search_entities_memory_items**](OtherApi.md#search_entities_memory_items) | **POST** /api/v1/entities/workspaces/{workspaceId}/memoryItems/search | Search request for MemoryItem
[**set_analytics_model_aac**](OtherApi.md#set_analytics_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Set analytics model from AAC format
[**set_logical_model_aac**](OtherApi.md#set_logical_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Set logical model from AAC format
[**set_user_data_filters**](OtherApi.md#set_user_data_filters) | **PUT** /api/v1/layout/workspaces/{workspaceId}/userDataFilters | Set user data filters
[**switch_active_identity_provider**](OtherApi.md#switch_active_identity_provider) | **POST** /api/v1/actions/organization/switchActiveIdentityProvider | Switch Active Identity Provider
[**update_entity_custom_geo_collections**](OtherApi.md#update_entity_custom_geo_collections) | **PUT** /api/v1/entities/customGeoCollections/{id} | 
[**update_entity_knowledge_recommendations**](OtherApi.md#update_entity_knowledge_recommendations) | **PUT** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | 
[**update_entity_memory_items**](OtherApi.md#update_entity_memory_items) | **PUT** /api/v1/entities/workspaces/{workspaceId}/memoryItems/{objectId} | 


# **convert_geo_file**
> ConvertGeoFileResponse convert_geo_file(convert_geo_file_request)

Convert a geo file to GeoParquet format

Converts a geo file from the staging area to GeoParquet format. Supported source formats: GeoJSON (.geojson, .json). If the source file is already in GeoParquet format, the same location is returned without conversion.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.convert_geo_file_response import ConvertGeoFileResponse
from gooddata_api_client.model.convert_geo_file_request import ConvertGeoFileRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    convert_geo_file_request = ConvertGeoFileRequest(
        location="location_example",
    ) # ConvertGeoFileRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Convert a geo file to GeoParquet format
        api_response = api_instance.convert_geo_file(convert_geo_file_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->convert_geo_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **convert_geo_file_request** | [**ConvertGeoFileRequest**](ConvertGeoFileRequest.md)|  |

### Return type

[**ConvertGeoFileResponse**](ConvertGeoFileResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Conversion was successful. |  -  |
**400** | Invalid request or unsupported file format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument create_entity_custom_geo_collections(json_api_custom_geo_collection_in_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    json_api_custom_geo_collection_in_document = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            id="id1",
            type="customGeoCollection",
        ),
    ) # JsonApiCustomGeoCollectionInDocument | 

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_custom_geo_collections(json_api_custom_geo_collection_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->create_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_custom_geo_collection_in_document** | [**JsonApiCustomGeoCollectionInDocument**](JsonApiCustomGeoCollectionInDocument.md)|  |

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument create_entity_knowledge_recommendations(workspace_id, json_api_knowledge_recommendation_post_optional_id_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_post_optional_id_document import JsonApiKnowledgeRecommendationPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_knowledge_recommendation_post_optional_id_document = JsonApiKnowledgeRecommendationPostOptionalIdDocument(
        data=JsonApiKnowledgeRecommendationPostOptionalId(
            attributes=JsonApiKnowledgeRecommendationInAttributes(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations={},
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example",
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=JsonApiKnowledgeRecommendationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=JsonApiKnowledgeRecommendationInRelationshipsMetric(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    ) # JsonApiKnowledgeRecommendationPostOptionalIdDocument | 
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_knowledge_recommendations(workspace_id, json_api_knowledge_recommendation_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->create_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_knowledge_recommendations(workspace_id, json_api_knowledge_recommendation_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->create_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_knowledge_recommendation_post_optional_id_document** | [**JsonApiKnowledgeRecommendationPostOptionalIdDocument**](JsonApiKnowledgeRecommendationPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_entity_memory_items**
> JsonApiMemoryItemOutDocument create_entity_memory_items(workspace_id, json_api_memory_item_post_optional_id_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_memory_item_post_optional_id_document import JsonApiMemoryItemPostOptionalIdDocument
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_memory_item_post_optional_id_document = JsonApiMemoryItemPostOptionalIdDocument(
        data=JsonApiMemoryItemPostOptionalId(
            attributes=JsonApiMemoryItemInAttributes(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example",
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    ) # JsonApiMemoryItemPostOptionalIdDocument | 
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_memory_items(workspace_id, json_api_memory_item_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->create_entity_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_memory_items(workspace_id, json_api_memory_item_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->create_entity_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_memory_item_post_optional_id_document** | [**JsonApiMemoryItemPostOptionalIdDocument**](JsonApiMemoryItemPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiMemoryItemOutDocument**](JsonApiMemoryItemOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **custom_geo_collection_staging_upload**
> UploadGeoCollectionFileResponse custom_geo_collection_staging_upload(file)

Upload a geo collection file to the staging area

Provides a location for uploading staging files for custom geo collections. Supported file types: GeoParquet (.parquet), GeoJSON (.geojson, .json).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.upload_geo_collection_file_response import UploadGeoCollectionFileResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    file = open('/path/to/file', 'rb') # file_type | The geo collection file to upload. Supported formats: GeoParquet (.parquet), GeoJSON (.geojson, .json).

    # example passing only required values which don't have defaults set
    try:
        # Upload a geo collection file to the staging area
        api_response = api_instance.custom_geo_collection_staging_upload(file)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->custom_geo_collection_staging_upload: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file_type**| The geo collection file to upload. Supported formats: GeoParquet (.parquet), GeoJSON (.geojson, .json). |

### Return type

[**UploadGeoCollectionFileResponse**](UploadGeoCollectionFileResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Upload was successful. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_custom_geo_collections**
> delete_entity_custom_geo_collections(id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_custom_geo_collections(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->delete_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_custom_geo_collections(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->delete_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_knowledge_recommendations**
> delete_entity_knowledge_recommendations(workspace_id, object_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_knowledge_recommendations(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->delete_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_knowledge_recommendations(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->delete_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_memory_items**
> delete_entity_memory_items(workspace_id, object_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_memory_items(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->delete_entity_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_memory_items(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->delete_entity_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deprovision_ai_lake_database_instance**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} deprovision_ai_lake_database_instance(instance_id)

(BETA) Delete an existing AILake Database instance

(BETA) Deletes an existing database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    instance_id = "instanceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Delete an existing AILake Database instance
        api_response = api_instance.deprovision_ai_lake_database_instance(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->deprovision_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**|  |

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted |  * operation-id - Operation ID to use for polling. <br>  * operation-location - Operation location URL that can be used for polling. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ai_lake_database_instance**
> DatabaseInstance get_ai_lake_database_instance(instance_id)

(BETA) Get the specified AILake Database instance

(BETA) Retrieve details of the specified AI Lake database instance in the organization's AI Lake.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.database_instance import DatabaseInstance
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    instance_id = "instanceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get the specified AILake Database instance
        api_response = api_instance.get_ai_lake_database_instance(instance_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **instance_id** | **str**|  |

### Return type

[**DatabaseInstance**](DatabaseInstance.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake database instance successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ai_lake_operation**
> GetAiLakeOperation200Response get_ai_lake_operation(operation_id)

(BETA) Get Long Running Operation details

(BETA) Retrieves details of a Long Running Operation specified by the operation-id.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.get_ai_lake_operation200_response import GetAiLakeOperation200Response
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    operation_id = "e9fd5d74-8a1b-46bd-ac60-bd91e9206897" # str | Operation ID

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Get Long Running Operation details
        api_response = api_instance.get_ai_lake_operation(operation_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_ai_lake_operation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operation_id** | **str**| Operation ID |

### Return type

[**GetAiLakeOperation200Response**](GetAiLakeOperation200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AI Lake Long Running Operation details successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_custom_geo_collections**
> JsonApiCustomGeoCollectionOutList get_all_entities_custom_geo_collections()



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_list import JsonApiCustomGeoCollectionOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_custom_geo_collections(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_all_entities_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutList**](JsonApiCustomGeoCollectionOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutList get_all_entities_knowledge_recommendations(workspace_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_list import JsonApiKnowledgeRecommendationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_knowledge_recommendations(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_all_entities_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_knowledge_recommendations(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_all_entities_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutList**](JsonApiKnowledgeRecommendationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_memory_items**
> JsonApiMemoryItemOutList get_all_entities_memory_items(workspace_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_memory_item_out_list import JsonApiMemoryItemOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_memory_items(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_all_entities_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_memory_items(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_all_entities_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiMemoryItemOutList**](JsonApiMemoryItemOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_analytics_model_aac**
> AacAnalyticsModel get_analytics_model_aac(workspace_id)

Get analytics model in AAC format

             Retrieve the analytics model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This includes metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.aac_analytics_model import AacAnalyticsModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_analytics_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_analytics_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**AacAnalyticsModel**](AacAnalyticsModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current analytics model in AAC format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_collection_items**
> GeoJsonFeatureCollection get_collection_items(collection_id)

Get collection features

Retrieve features from a GeoCollections collection as GeoJSON

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.geo_json_feature_collection import GeoJsonFeatureCollection
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    collection_id = "countries" # str | Collection identifier
    limit = 100 # int | Maximum number of features to return (optional)
    bbox = "-180,-90,180,90" # str | Bounding box filter (minx,miny,maxx,maxy) (optional)
    values = [
        "US,CA,MX",
    ] # [str] | List of values to filter features by (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get collection features
        api_response = api_instance.get_collection_items(collection_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_collection_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get collection features
        api_response = api_instance.get_collection_items(collection_id, limit=limit, bbox=bbox, values=values)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_collection_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Collection identifier |
 **limit** | **int**| Maximum number of features to return | [optional]
 **bbox** | **str**| Bounding box filter (minx,miny,maxx,maxy) | [optional]
 **values** | **[str]**| List of values to filter features by | [optional]

### Return type

[**GeoJsonFeatureCollection**](GeoJsonFeatureCollection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Features retrieved successfully |  -  |
**404** | Collection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_collection_items**
> GeoJsonFeatureCollection get_custom_collection_items(collection_id)

Get custom collection features

Retrieve features from a custom (organization-scoped) GeoCollections collection as GeoJSON

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.geo_json_feature_collection import GeoJsonFeatureCollection
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    collection_id = "my-custom-collection" # str | Collection identifier
    limit = 100 # int | Maximum number of features to return (optional)
    bbox = "-180,-90,180,90" # str | Bounding box filter (minx,miny,maxx,maxy) (optional)
    values = [
        "US,CA,MX",
    ] # [str] | List of values to filter features by (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get custom collection features
        api_response = api_instance.get_custom_collection_items(collection_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_custom_collection_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get custom collection features
        api_response = api_instance.get_custom_collection_items(collection_id, limit=limit, bbox=bbox, values=values)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_custom_collection_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Collection identifier |
 **limit** | **int**| Maximum number of features to return | [optional]
 **bbox** | **str**| Bounding box filter (minx,miny,maxx,maxy) | [optional]
 **values** | **[str]**| List of values to filter features by | [optional]

### Return type

[**GeoJsonFeatureCollection**](GeoJsonFeatureCollection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Features retrieved successfully |  -  |
**404** | Collection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument get_entity_custom_geo_collections(id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_custom_geo_collections(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_custom_geo_collections(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument get_entity_knowledge_recommendations(workspace_id, object_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_knowledge_recommendations(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_knowledge_recommendations(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_memory_items**
> JsonApiMemoryItemOutDocument get_entity_memory_items(workspace_id, object_id)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_memory_items(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_entity_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_memory_items(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_entity_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiMemoryItemOutDocument**](JsonApiMemoryItemOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_logical_model_aac**
> AacLogicalModel get_logical_model_aac(workspace_id)

Get logical model in AAC format

             Retrieve the logical data model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. Use this for exporting models             that can be directly used as YAML configuration files.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    include_parents = True # bool |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_logical_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(workspace_id, include_parents=include_parents)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_logical_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **include_parents** | **bool**|  | [optional]

### Return type

[**AacLogicalModel**](AacLogicalModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current logical model in AAC format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_data_filters**
> DeclarativeUserDataFilters get_user_data_filters(workspace_id)

Get user data filters

Retrieve current user data filters assigned to the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get user data filters
        api_response = api_instance.get_user_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->get_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**DeclarativeUserDataFilters**](DeclarativeUserDataFilters.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current user data filters. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_custom_geo_collection**
> ImportGeoCollectionResponse import_custom_geo_collection(collection_id, import_geo_collection_request)

Import custom geo collection

Import a geo collection file from the staging area to be available for use.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.import_geo_collection_response import ImportGeoCollectionResponse
from gooddata_api_client.model.import_geo_collection_request import ImportGeoCollectionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    collection_id = "collectionId_example" # str | 
    import_geo_collection_request = ImportGeoCollectionRequest(
        location="location_example",
    ) # ImportGeoCollectionRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Import custom geo collection
        api_response = api_instance.import_custom_geo_collection(collection_id, import_geo_collection_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->import_custom_geo_collection: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**|  |
 **import_geo_collection_request** | [**ImportGeoCollectionRequest**](ImportGeoCollectionRequest.md)|  |

### Return type

[**ImportGeoCollectionResponse**](ImportGeoCollectionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful import. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_check_organization**
> metadata_check_organization()

(BETA) Check Organization Metadata Inconsistencies

(BETA) Temporary solution. Resyncs all organization objects and full workspaces within the organization with target GEN_AI_CHECK.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Check Organization Metadata Inconsistencies
        api_instance.metadata_check_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->metadata_check_organization: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_sync**
> metadata_sync(workspace_id)

(BETA) Sync Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger it in its scope only.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Sync Metadata to other services
        api_instance.metadata_sync(workspace_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->metadata_sync: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metadata_sync_organization**
> metadata_sync_organization()

(BETA) Sync organization scope Metadata to other services

(BETA) Temporary solution. Later relevant metadata actions will trigger sync in their scope only.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # (BETA) Sync organization scope Metadata to other services
        api_instance.metadata_sync_organization()
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->metadata_sync_organization: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument patch_entity_custom_geo_collections(id, json_api_custom_geo_collection_patch_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_custom_geo_collection_patch_document import JsonApiCustomGeoCollectionPatchDocument
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_custom_geo_collection_patch_document = JsonApiCustomGeoCollectionPatchDocument(
        data=JsonApiCustomGeoCollectionPatch(
            id="id1",
            type="customGeoCollection",
        ),
    ) # JsonApiCustomGeoCollectionPatchDocument | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.patch_entity_custom_geo_collections(id, json_api_custom_geo_collection_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->patch_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.patch_entity_custom_geo_collections(id, json_api_custom_geo_collection_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->patch_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_custom_geo_collection_patch_document** | [**JsonApiCustomGeoCollectionPatchDocument**](JsonApiCustomGeoCollectionPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument patch_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_patch_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_knowledge_recommendation_patch_document import JsonApiKnowledgeRecommendationPatchDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_knowledge_recommendation_patch_document = JsonApiKnowledgeRecommendationPatchDocument(
        data=JsonApiKnowledgeRecommendationPatch(
            attributes=JsonApiKnowledgeRecommendationPatchAttributes(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations={},
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example",
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=JsonApiKnowledgeRecommendationOutRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=JsonApiKnowledgeRecommendationInRelationshipsMetric(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    ) # JsonApiKnowledgeRecommendationPatchDocument | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.patch_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->patch_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.patch_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->patch_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_knowledge_recommendation_patch_document** | [**JsonApiKnowledgeRecommendationPatchDocument**](JsonApiKnowledgeRecommendationPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_memory_items**
> JsonApiMemoryItemOutDocument patch_entity_memory_items(workspace_id, object_id, json_api_memory_item_patch_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_memory_item_patch_document import JsonApiMemoryItemPatchDocument
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_memory_item_patch_document = JsonApiMemoryItemPatchDocument(
        data=JsonApiMemoryItemPatch(
            attributes=JsonApiMemoryItemPatchAttributes(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example",
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    ) # JsonApiMemoryItemPatchDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.patch_entity_memory_items(workspace_id, object_id, json_api_memory_item_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->patch_entity_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.patch_entity_memory_items(workspace_id, object_id, json_api_memory_item_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->patch_entity_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_memory_item_patch_document** | [**JsonApiMemoryItemPatchDocument**](JsonApiMemoryItemPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiMemoryItemOutDocument**](JsonApiMemoryItemOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **provision_ai_lake_database_instance**
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} provision_ai_lake_database_instance(provision_database_instance_request)

(BETA) Create a new AILake Database instance

(BETA) Creates a new database in the organization's AI Lake. Returns an operation-id in the operation-id header the client can use to poll for the progress.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.provision_database_instance_request import ProvisionDatabaseInstanceRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    provision_database_instance_request = ProvisionDatabaseInstanceRequest(
        name="name_example",
        storage_ids=[
            "storage_ids_example",
        ],
    ) # ProvisionDatabaseInstanceRequest | 

    # example passing only required values which don't have defaults set
    try:
        # (BETA) Create a new AILake Database instance
        api_response = api_instance.provision_ai_lake_database_instance(provision_database_instance_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->provision_ai_lake_database_instance: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **provision_database_instance_request** | [**ProvisionDatabaseInstanceRequest**](ProvisionDatabaseInstanceRequest.md)|  |

### Return type

**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted |  * operation-id - Operation ID to use for polling. <br>  * operation-location - Operation location URL that can be used for polling. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_entities_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutList search_entities_knowledge_recommendations(workspace_id, entity_search_body)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_list import JsonApiKnowledgeRecommendationOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    entity_search_body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example",
        ],
        meta_include=[
            "meta_include_example",
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            ),
        ],
    ) # EntitySearchBody | Search request body with filter, pagination, and sorting options
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.search_entities_knowledge_recommendations(workspace_id, entity_search_body)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->search_entities_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.search_entities_knowledge_recommendations(workspace_id, entity_search_body, origin=origin, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->search_entities_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **entity_search_body** | [**EntitySearchBody**](EntitySearchBody.md)| Search request body with filter, pagination, and sorting options |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiKnowledgeRecommendationOutList**](JsonApiKnowledgeRecommendationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_entities_memory_items**
> JsonApiMemoryItemOutList search_entities_memory_items(workspace_id, entity_search_body)

Search request for MemoryItem

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_memory_item_out_list import JsonApiMemoryItemOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    entity_search_body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example",
        ],
        meta_include=[
            "meta_include_example",
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            ),
        ],
    ) # EntitySearchBody | Search request body with filter, pagination, and sorting options
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Search request for MemoryItem
        api_response = api_instance.search_entities_memory_items(workspace_id, entity_search_body)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->search_entities_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Search request for MemoryItem
        api_response = api_instance.search_entities_memory_items(workspace_id, entity_search_body, origin=origin, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->search_entities_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **entity_search_body** | [**EntitySearchBody**](EntitySearchBody.md)| Search request body with filter, pagination, and sorting options |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiMemoryItemOutList**](JsonApiMemoryItemOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_analytics_model_aac**
> set_analytics_model_aac(workspace_id, aac_analytics_model)

Set analytics model from AAC format

             Set the analytics model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              analytics model with the provided definition, including metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.aac_analytics_model import AacAnalyticsModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    aac_analytics_model = AacAnalyticsModel(
        attribute_hierarchies=[
            AacAttributeHierarchy(
                attributes=["attribute/country","attribute/state","attribute/city"],
                description="description_example",
                id="geo-hierarchy",
                tags=[
                    "tags_example",
                ],
                title="Geographic Hierarchy",
                type="attribute_hierarchy",
            ),
        ],
        dashboards=[
            AacDashboard(None),
        ],
        metrics=[
            AacMetric(
                description="description_example",
                format="#,##0.00",
                id="total-sales",
                is_hidden=True,
                is_hidden_from_kda=True,
                maql="SELECT SUM({fact/amount})",
                show_in_ai_results=True,
                tags=[
                    "tags_example",
                ],
                title="Total Sales",
                type="metric",
            ),
        ],
        plugins=[
            AacPlugin(
                description="description_example",
                id="my-plugin",
                tags=[
                    "tags_example",
                ],
                title="My Plugin",
                type="plugin",
                url="https://example.com/plugin.js",
            ),
        ],
        visualizations=[
            AacVisualization(None),
        ],
    ) # AacAnalyticsModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set analytics model from AAC format
        api_instance.set_analytics_model_aac(workspace_id, aac_analytics_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->set_analytics_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **aac_analytics_model** | [**AacAnalyticsModel**](AacAnalyticsModel.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Analytics model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_logical_model_aac**
> set_logical_model_aac(workspace_id, aac_logical_model)

Set logical model from AAC format

             Set the logical data model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              logical model with the provided definition.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    aac_logical_model = AacLogicalModel(
        datasets=[
            AacDataset(
                data_source="my-postgres",
                description="description_example",
                fields={
                    "key": AacField(
                        aggregated_as="SUM",
                        assigned_to="assigned_to_example",
                        data_type="STRING",
                        default_view="default_view_example",
                        description="description_example",
                        is_hidden=True,
                        labels={
                            "key": AacLabel(
                                data_type="INT",
                                description="description_example",
                                geo_area_config=AacGeoAreaConfig(
                                    collection=AacGeoCollectionIdentifier(
                                        id="id_example",
                                        kind="STATIC",
                                    ),
                                ),
                                is_hidden=True,
                                locale="locale_example",
                                show_in_ai_results=True,
                                source_column="source_column_example",
                                tags=[
                                    "tags_example",
                                ],
                                title="title_example",
                                translations=[
                                    AacLabelTranslation(
                                        locale="locale_example",
                                        source_column="source_column_example",
                                    ),
                                ],
                                value_type="TEXT",
                            ),
                        },
                        locale="locale_example",
                        show_in_ai_results=True,
                        sort_column="sort_column_example",
                        sort_direction="ASC",
                        source_column="source_column_example",
                        tags=[
                            "tags_example",
                        ],
                        title="title_example",
                        type="attribute",
                    ),
                },
                id="customers",
                precedence=1,
                primary_key=AacDatasetPrimaryKey(None),
                references=[
                    AacReference(
                        dataset="orders",
                        multi_directional=True,
                        sources=[
                            AacReferenceSource(
                                data_type="INT",
                                source_column="source_column_example",
                                target="target_example",
                            ),
                        ],
                    ),
                ],
                sql="sql_example",
                table_path="public/customers",
                tags=[
                    "tags_example",
                ],
                title="Customers",
                type="dataset",
                workspace_data_filters=[
                    AacWorkspaceDataFilter(
                        data_type="INT",
                        filter_id="filter_id_example",
                        source_column="source_column_example",
                    ),
                ],
            ),
        ],
        date_datasets=[
            AacDateDataset(
                description="description_example",
                granularities=[
                    "granularities_example",
                ],
                id="date",
                tags=[
                    "tags_example",
                ],
                title="Date",
                title_base="title_base_example",
                title_pattern="title_pattern_example",
                type="date",
            ),
        ],
    ) # AacLogicalModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set logical model from AAC format
        api_instance.set_logical_model_aac(workspace_id, aac_logical_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->set_logical_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **aac_logical_model** | [**AacLogicalModel**](AacLogicalModel.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Logical model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_user_data_filters**
> set_user_data_filters(workspace_id, declarative_user_data_filters)

Set user data filters

Set user data filters assigned to the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.declarative_user_data_filters import DeclarativeUserDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_user_data_filters = DeclarativeUserDataFilters(
        user_data_filters=[
            DeclarativeUserDataFilter(
                description="ID of country setting",
                id="country_id_setting",
                maql="{label/country} = "USA" AND {label/date.year} = THIS(YEAR)",
                tags=["Revenues"],
                title="Country ID setting",
                user=DeclarativeUserIdentifier(
                    id="employee123",
                    type="user",
                ),
                user_group=DeclarativeUserGroupIdentifier(
                    id="group.admins",
                    type="userGroup",
                ),
            ),
        ],
    ) # DeclarativeUserDataFilters | 

    # example passing only required values which don't have defaults set
    try:
        # Set user data filters
        api_instance.set_user_data_filters(workspace_id, declarative_user_data_filters)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->set_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_user_data_filters** | [**DeclarativeUserDataFilters**](DeclarativeUserDataFilters.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | User data filters successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **switch_active_identity_provider**
> switch_active_identity_provider(switch_identity_provider_request)

Switch Active Identity Provider

Switch the active identity provider for the organization. Requires MANAGE permission on the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.switch_identity_provider_request import SwitchIdentityProviderRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    switch_identity_provider_request = SwitchIdentityProviderRequest(
        idp_id="my-idp-123",
    ) # SwitchIdentityProviderRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Switch Active Identity Provider
        api_instance.switch_active_identity_provider(switch_identity_provider_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->switch_active_identity_provider: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **switch_identity_provider_request** | [**SwitchIdentityProviderRequest**](SwitchIdentityProviderRequest.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_custom_geo_collections**
> JsonApiCustomGeoCollectionOutDocument update_entity_custom_geo_collections(id, json_api_custom_geo_collection_in_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_custom_geo_collection_out_document import JsonApiCustomGeoCollectionOutDocument
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_custom_geo_collection_in_document = JsonApiCustomGeoCollectionInDocument(
        data=JsonApiCustomGeoCollectionIn(
            id="id1",
            type="customGeoCollection",
        ),
    ) # JsonApiCustomGeoCollectionInDocument | 
    filter = "" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_custom_geo_collections(id, json_api_custom_geo_collection_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->update_entity_custom_geo_collections: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_custom_geo_collections(id, json_api_custom_geo_collection_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->update_entity_custom_geo_collections: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_custom_geo_collection_in_document** | [**JsonApiCustomGeoCollectionInDocument**](JsonApiCustomGeoCollectionInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomGeoCollectionOutDocument**](JsonApiCustomGeoCollectionOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument update_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_in_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_in_document import JsonApiKnowledgeRecommendationInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_knowledge_recommendation_in_document = JsonApiKnowledgeRecommendationInDocument(
        data=JsonApiKnowledgeRecommendationIn(
            attributes=JsonApiKnowledgeRecommendationInAttributes(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations={},
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example",
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=JsonApiKnowledgeRecommendationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=JsonApiKnowledgeRecommendationInRelationshipsMetric(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    ) # JsonApiKnowledgeRecommendationInDocument | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->update_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->update_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_knowledge_recommendation_in_document** | [**JsonApiKnowledgeRecommendationInDocument**](JsonApiKnowledgeRecommendationInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_memory_items**
> JsonApiMemoryItemOutDocument update_entity_memory_items(workspace_id, object_id, json_api_memory_item_in_document)



### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import other_api
from gooddata_api_client.model.json_api_memory_item_in_document import JsonApiMemoryItemInDocument
from gooddata_api_client.model.json_api_memory_item_out_document import JsonApiMemoryItemOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = other_api.OtherApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_memory_item_in_document = JsonApiMemoryItemInDocument(
        data=JsonApiMemoryItemIn(
            attributes=JsonApiMemoryItemInAttributes(
                are_relations_valid=True,
                description="description_example",
                instruction="instruction_example",
                is_disabled=True,
                keywords=[
                    "keywords_example",
                ],
                strategy="ALWAYS",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="memoryItem",
        ),
    ) # JsonApiMemoryItemInDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_memory_items(workspace_id, object_id, json_api_memory_item_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->update_entity_memory_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_memory_items(workspace_id, object_id, json_api_memory_item_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OtherApi->update_entity_memory_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_memory_item_in_document** | [**JsonApiMemoryItemInDocument**](JsonApiMemoryItemInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiMemoryItemOutDocument**](JsonApiMemoryItemOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

