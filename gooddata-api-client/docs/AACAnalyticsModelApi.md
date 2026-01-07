# gooddata_api_client.AACAnalyticsModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analytics_model_aac**](AACAnalyticsModelApi.md#get_analytics_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Get analytics model in AAC format
[**set_analytics_model_aac**](AACAnalyticsModelApi.md#set_analytics_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/analyticsModel | Set analytics model from AAC format


# **get_analytics_model_aac**
> AacAnalyticsModel get_analytics_model_aac(workspace_id)

Get analytics model in AAC format

             Retrieve the analytics model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This includes metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_analytics_model_api
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
    api_instance = aac_analytics_model_api.AACAnalyticsModelApi(api_client)
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
        print("Exception when calling AACAnalyticsModelApi->get_analytics_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get analytics model in AAC format
        api_response = api_instance.get_analytics_model_aac(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACAnalyticsModelApi->get_analytics_model_aac: %s\n" % e)
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

# **set_analytics_model_aac**
> set_analytics_model_aac(workspace_id, aac_analytics_model)

Set analytics model from AAC format

             Set the analytics model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              analytics model with the provided definition, including metrics,              dashboards, visualizations, plugins, and attribute hierarchies.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_analytics_model_api
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
    api_instance = aac_analytics_model_api.AACAnalyticsModelApi(api_client)
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
            AacDashboard(
                active_tab_id="active_tab_id_example",
                cross_filtering=True,
                description="description_example",
                enable_section_headers=True,
                filter_views=True,
                filters={
                    "key": AacDashboardFilter(
                        date="date_example",
                        display_as="display_as_example",
                        _from=JsonNode(),
                        granularity="granularity_example",
                        metric_filters=[
                            "metric_filters_example",
                        ],
                        mode="active",
                        multiselect=True,
                        parents=[
                            JsonNode(),
                        ],
                        state=AacFilterState(
                            exclude=[
                                "exclude_example",
                            ],
                            include=[
                                "include_example",
                            ],
                        ),
                        title="title_example",
                        to=JsonNode(),
                        type="attribute_filter",
                        using="using_example",
                    ),
                },
                id="sales-overview",
                permissions=AacDashboardPermissions(
                    edit=AacPermission(
                        all=True,
                        user_groups=[
                            "user_groups_example",
                        ],
                        users=[
                            "users_example",
                        ],
                    ),
                    share=AacPermission(
                        all=True,
                        user_groups=[
                            "user_groups_example",
                        ],
                        users=[
                            "users_example",
                        ],
                    ),
                    view=AacPermission(
                        all=True,
                        user_groups=[
                            "user_groups_example",
                        ],
                        users=[
                            "users_example",
                        ],
                    ),
                ),
                plugins=[
                    AacDashboardPluginLink(
                        id="id_example",
                        parameters=JsonNode(),
                    ),
                ],
                sections=[
                    AacSection(
                        description="description_example",
                        header=True,
                        title="title_example",
                        widgets=[
                            AacWidget(
                                additional_properties={
                                    "key": JsonNode(),
                                },
                                content="content_example",
                                date="date_example",
                                description="description_example",
                                drill_down=JsonNode(),
                                ignore_dashboard_filters=[
                                    "ignore_dashboard_filters_example",
                                ],
                                metric="metric_example",
                                sections=[
                                    AacSection(),
                                ],
                                size=AacWidgetSize(
                                    height=1,
                                    height_as_ratio=True,
                                    width=1,
                                ),
                                title="title_example",
                                type="visualization",
                                visualization="visualization_example",
                            ),
                        ],
                    ),
                ],
                tabs=[
                    AacTab(
                        filters={
                            "key": AacDashboardFilter(
                                date="date_example",
                                display_as="display_as_example",
                                _from=JsonNode(),
                                granularity="granularity_example",
                                metric_filters=[
                                    "metric_filters_example",
                                ],
                                mode="active",
                                multiselect=True,
                                parents=[
                                    JsonNode(),
                                ],
                                state=AacFilterState(
                                    exclude=[
                                        "exclude_example",
                                    ],
                                    include=[
                                        "include_example",
                                    ],
                                ),
                                title="title_example",
                                to=JsonNode(),
                                type="attribute_filter",
                                using="using_example",
                            ),
                        },
                        id="id_example",
                        sections=[
                            AacSection(
                                description="description_example",
                                header=True,
                                title="title_example",
                                widgets=[
                                    AacWidget(
                                        additional_properties={
                                            "key": JsonNode(),
                                        },
                                        content="content_example",
                                        date="date_example",
                                        description="description_example",
                                        drill_down=JsonNode(),
                                        ignore_dashboard_filters=[
                                            "ignore_dashboard_filters_example",
                                        ],
                                        metric="metric_example",
                                        sections=[
                                            AacSection(),
                                        ],
                                        size=AacWidgetSize(
                                            height=1,
                                            height_as_ratio=True,
                                            width=1,
                                        ),
                                        title="title_example",
                                        type="visualization",
                                        visualization="visualization_example",
                                    ),
                                ],
                            ),
                        ],
                        title="title_example",
                    ),
                ],
                tags=[
                    "tags_example",
                ],
                title="Sales Overview",
                type="dashboard",
                user_filters_reset=True,
                user_filters_save=True,
            ),
        ],
        metrics=[
            AacMetric(
                description="description_example",
                format="#,##0.00",
                id="total-sales",
                is_hidden=True,
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
            AacVisualization(
                additional_properties={
                    "key": JsonNode(),
                },
                attribute=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                color=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                columns=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                config=JsonNode(),
                description="description_example",
                id="sales-by-region",
                is_hidden=True,
                location=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                metrics=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                primary_measures=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                query=AacQuery(
                    attributes=[
                        AacQueryAttribute(
                            additional_properties={
                                "key": JsonNode(),
                            },
                            display_as="display_as_example",
                            local_id="local_id_example",
                            show_all_values=True,
                            using="using_example",
                        ),
                    ],
                    filters={
                        "key": AacQueryFilter(
                            additional_properties={
                                "key": JsonNode(),
                            },
                            condition="condition_example",
                            _from=JsonNode(),
                            granularity="granularity_example",
                            state=AacFilterState(
                                exclude=[
                                    "exclude_example",
                                ],
                                include=[
                                    "include_example",
                                ],
                            ),
                            to=JsonNode(),
                            type="type_example",
                            using="using_example",
                            value=3.14,
                        ),
                    },
                    metrics=[
                        AacQueryMetric(
                            additional_properties={
                                "key": JsonNode(),
                            },
                            compute_ratio=True,
                            format="format_example",
                            local_id="local_id_example",
                            maql="maql_example",
                            title="title_example",
                            using="using_example",
                        ),
                    ],
                ),
                rows=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                secondary_measures=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                segment_by=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                show_in_ai_results=True,
                size=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                stack=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                tags=[
                    "tags_example",
                ],
                title="Sales by Region",
                trend=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
                type="bar_chart",
                view_by=[
                    AacBucketItem(
                        additional_properties={
                            "key": JsonNode(),
                        },
                        alias="alias_example",
                        compute_ratio=True,
                        display_as="display_as_example",
                        format="format_example",
                        local_id="local_id_example",
                        maql="maql_example",
                        show_all_values=True,
                        title="title_example",
                        using="using_example",
                    ),
                ],
            ),
        ],
    ) # AacAnalyticsModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set analytics model from AAC format
        api_instance.set_analytics_model_aac(workspace_id, aac_analytics_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACAnalyticsModelApi->set_analytics_model_aac: %s\n" % e)
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

