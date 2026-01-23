# AuthUser

Entity representing user in authentication system.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | User description, which will be visible in application. | 
**email** | **str** | Email - used as lookup (must be unique). For PUT method, it must be same as in URL | 
**authentication_id** | **str** | Field, which should be stored in metadata in authenticationId field. In PUT and POST method it must be not present, or equal to value calculated by backend (e.g. returned from previous GET). | [optional] 
**password** | **str** | User password. It is not returned by GET method. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


