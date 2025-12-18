# AuthApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**authTokenCreate**](AuthApi.md#authtokencreate) | **POST** /api/v1/external/auth/token/ |  |
| [**authTokenRefreshCreate**](AuthApi.md#authtokenrefreshcreate) | **POST** /api/v1/external/auth/token/refresh/ |  |



## authTokenCreate

> TokenObtainPair authTokenCreate(tokenObtainPair)



Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { AuthTokenCreateRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // TokenObtainPair
    tokenObtainPair: ...,
  } satisfies AuthTokenCreateRequest;

  try {
    const data = await api.authTokenCreate(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **tokenObtainPair** | [TokenObtainPair](TokenObtainPair.md) |  | |

### Return type

[**TokenObtainPair**](TokenObtainPair.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`, `application/x-www-form-urlencoded`, `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## authTokenRefreshCreate

> TokenRefresh authTokenRefreshCreate(tokenRefresh)



Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { AuthTokenRefreshCreateRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // TokenRefresh
    tokenRefresh: ...,
  } satisfies AuthTokenRefreshCreateRequest;

  try {
    const data = await api.authTokenRefreshCreate(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **tokenRefresh** | [TokenRefresh](TokenRefresh.md) |  | |

### Return type

[**TokenRefresh**](TokenRefresh.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`, `application/x-www-form-urlencoded`, `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

