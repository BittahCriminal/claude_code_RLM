# Available API Deployments

## Overview

This endpoint retrieves a list of available API deployments from the Azure API Management service. It can be filtered by URL apiPath or API ID. The endpoint queries the Azure Management API to retrieve deployment information and returns it in a structured format.

## Endpoint

`GET /tmds/deployments`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim.

## Request Parameters

### Headers

- `apiPath` (optional): Filter deployments by URL apiPath
- `apiId` (optional): Filter deployments by API ID

## Response

### Success Response

**Status Code:** 200 OK

```json
[
  {
    "name": "GCR Members - Shared AOAI (OAuth)",
    "apiPath": "gcr/shared/openai",
    "apiId": "670528256820ca7d1ddc6857"
  },
  {
    "name": "GCR_Members - gcr-llama-32-90b-vision-1",
    "apiPath": "gcr/shared/microsoft/deployments/gcr-llama-32-90b-vision-1",
    "apiId": "gcr-members-gcr-llama-32-90b-vision-1"
  },
  {
    "name": "GCR_Members - gcr-llama-3-3-70b-instruct-4",
    "apiPath": "gcr/shared/microsoft/deployments/gcr-llama-3-3-70b-instruct-4",
    "apiId": "67acf9ddbf5b936b11c513de"
  },
  ....
]
```

### Error Responses

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

**Status Code:** 500 Internal Server Error

```json
{
  "error": "Failed to retrieve API list",
  "statusCode": 500
}
```

## Example

Bash

```bash
# Get all deployments
curl -X GET \
  https://trapi.research.microsoft.com/tmds/deployments \
  -H 'Authorization: Bearer eyJ0eXAi...'

# Filter by API ID
curl -X GET \
  https://trapi.research.microsoft.com/tmds/deployments \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'apiId: gpt4-api'

# Filter by URL apiPath
curl -X GET \
  https://trapi.research.microsoft.com/tmds/deployments \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'apiPath: /openai/gpt4'
```

Powershell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$url = "https://trapi.research.microsoft.com/tmds/deployments"
$headers = @{
    apiPath = "gcr/shared/openai"
}
Invoke-RestMethod -Method GET -Uri $url -Authentication OAuth -Token $token.Token -Headers $headers
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/deployments
    APIM->>Azure Management API: GET /subscriptions/{subId}/resourceGroups/trapi-{env}/providers/Microsoft.ApiManagement/service/{service}/apis
    Note over APIM,Azure Management API: Uses APIM System Assigned Identity
    Azure Management API->>APIM: Return APIs list
    
    alt URL apiPath or API ID Provided
        APIM->>APIM: Filter results by apiPath or apiId header
    end
    
    APIM->>Client: Return filtered API list
:::

## Implementation Details

The deployments endpoint internally:

Authenticates the request using Azure AD

1. Queries the Azure Management API for all APIs in the APIM instance
2. Formats the response to include name, URL apiPath, and API ID for each deployment
3. Optionally filters results based on provided headers
4. Returns the final list as a JSON array
5. This endpoint is useful for discovery of available APIs and their identifiers, which can be used in other API calls like `/tmds/model/{ApiId}/{Model}`.