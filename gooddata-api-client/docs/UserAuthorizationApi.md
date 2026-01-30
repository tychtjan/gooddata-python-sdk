# gooddata_api_client.UserAuthorizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](UserAuthorizationApi.md#create_user) | **POST** /api/v1/auth/users | Create a user
[**delete_user**](UserAuthorizationApi.md#delete_user) | **DELETE** /api/v1/auth/users/{userEmail} | Delete a user
[**get_profile**](UserAuthorizationApi.md#get_profile) | **GET** /api/v1/profile | Get Profile
[**get_user**](UserAuthorizationApi.md#get_user) | **GET** /api/v1/auth/users/{userEmail} | Get a user
[**get_users**](UserAuthorizationApi.md#get_users) | **GET** /api/v1/auth/users | Get all users
[**process_invitation**](UserAuthorizationApi.md#process_invitation) | **POST** /api/v1/actions/invite | Invite User
[**update_user**](UserAuthorizationApi.md#update_user) | **PUT** /api/v1/auth/users/{userEmail} | Update a user


# **create_user**
> AuthUser create_user(auth_user)

Create a user

Create a user - dedicated endpoint for user management in the internal OIDC provider. GoodData.CN specific

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.auth_user import AuthUser
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)
    auth_user = AuthUser(
        authentication_id="authentication_id_example",
        display_name="jeremy",
        email="zeus@example.com",
        password="password_example",
    ) # AuthUser | 

    # example passing only required values which don't have defaults set
    try:
        # Create a user
        api_response = api_instance.create_user(auth_user)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->create_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auth_user** | [**AuthUser**](AuthUser.md)|  |

### Return type

[**AuthUser**](AuthUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> delete_user(user_email)

Delete a user

Delete a user - dedicated endpoint for user management in the internal OIDC provider. GoodData.CN specific

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)
    user_email = "userEmail_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a user
        api_instance.delete_user(user_email)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->delete_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profile**
> Profile get_profile()

Get Profile

Returns a Profile including Organization and Current User Information.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.profile import Profile
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get Profile
        api_response = api_instance.get_profile()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->get_profile: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**Profile**](Profile.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> AuthUser get_user(user_email)

Get a user

Get a user - dedicated endpoint for user management in the internal OIDC provider. GoodData.CN specific

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.auth_user import AuthUser
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)
    user_email = "userEmail_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get a user
        api_response = api_instance.get_user(user_email)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->get_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**|  |

### Return type

[**AuthUser**](AuthUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users**
> [AuthUser] get_users()

Get all users

Get all users - dedicated endpoint for user management in the internal OIDC provider. GoodData.CN specific

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.auth_user import AuthUser
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all users
        api_response = api_instance.get_users()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->get_users: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[AuthUser]**](AuthUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **process_invitation**
> process_invitation(invitation)

Invite User

Puts a new invitation requirement into the invitation generator queue. This is a GoodData Cloud specific endpoint.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.invitation import Invitation
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)
    invitation = Invitation(
        email="email_example",
        first_name="first_name_example",
        force_send=True,
        last_name="last_name_example",
        user_id="user_id_example",
    ) # Invitation | 

    # example passing only required values which don't have defaults set
    try:
        # Invite User
        api_instance.process_invitation(invitation)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->process_invitation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **invitation** | [**Invitation**](Invitation.md)|  |

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

# **update_user**
> AuthUser update_user(user_email, auth_user)

Update a user

Update a user - dedicated endpoint for user management in the internal OIDC provider. GoodData.CN specific

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import user_authorization_api
from gooddata_api_client.model.auth_user import AuthUser
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_authorization_api.UserAuthorizationApi(api_client)
    user_email = "userEmail_example" # str | 
    auth_user = AuthUser(
        authentication_id="authentication_id_example",
        display_name="jeremy",
        email="zeus@example.com",
        password="password_example",
    ) # AuthUser | 

    # example passing only required values which don't have defaults set
    try:
        # Update a user
        api_response = api_instance.update_user(user_email, auth_user)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling UserAuthorizationApi->update_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**|  |
 **auth_user** | [**AuthUser**](AuthUser.md)|  |

### Return type

[**AuthUser**](AuthUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

