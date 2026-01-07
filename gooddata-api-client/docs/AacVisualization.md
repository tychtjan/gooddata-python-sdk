# AacVisualization

AAC visualization definition.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the visualization. | 
**type** | **str** | Visualization type. | 
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**attribute** | [**[AacBucketItem]**](AacBucketItem.md) | Attribute bucket (for repeater). | [optional] 
**color** | [**[AacBucketItem]**](AacBucketItem.md) | Color bucket. | [optional] 
**columns** | [**[AacBucketItem]**](AacBucketItem.md) | Columns bucket (for tables). | [optional] 
**config** | [**JsonNode**](JsonNode.md) |  | [optional] 
**description** | **str** | Visualization description. | [optional] 
**is_hidden** | **bool** | Deprecated. Use showInAiResults instead. | [optional] 
**location** | [**[AacBucketItem]**](AacBucketItem.md) | Location bucket (for geo charts). | [optional] 
**metrics** | [**[AacBucketItem]**](AacBucketItem.md) | Metrics bucket. | [optional] 
**primary_measures** | [**[AacBucketItem]**](AacBucketItem.md) | Primary measures bucket. | [optional] 
**query** | [**AacQuery**](AacQuery.md) |  | [optional] 
**rows** | [**[AacBucketItem]**](AacBucketItem.md) | Rows bucket (for tables). | [optional] 
**secondary_measures** | [**[AacBucketItem]**](AacBucketItem.md) | Secondary measures bucket. | [optional] 
**segment_by** | [**[AacBucketItem]**](AacBucketItem.md) | Segment by attributes bucket. | [optional] 
**show_in_ai_results** | **bool** | Whether to show in AI results. | [optional] 
**size** | [**[AacBucketItem]**](AacBucketItem.md) | Size bucket. | [optional] 
**stack** | [**[AacBucketItem]**](AacBucketItem.md) | Stack bucket. | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**trend** | [**[AacBucketItem]**](AacBucketItem.md) | Trend bucket. | [optional] 
**view_by** | [**[AacBucketItem]**](AacBucketItem.md) | View by attributes bucket. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


