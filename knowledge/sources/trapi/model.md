# Check if a Specific Model Exists

## Overview

This endpoint checks if a specific model exists for a given API ID. It first retrieves the apiPath associated with the API ID, then queries that API's models endpoint to determine if the specified model is available.

## Endpoint

`GET /tmds/model/{ApiId}/{Model}`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim.

## Request Parameters

### Path Parameters

- `ApiId` (required): The ID of the API to check (e.g., "gpt4-api")
- `Model` (required): The model name to check (e.g., "gpt-4", "gpt-4o")

### Headers

- `Authorization` (required): Bearer token for authentication

## Response

### Success Response

**Status Code:** 200 OK

```json
{
  "exists": true || false
}
```

### Error Responses

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

**Status Code:** 404 Not Found

```json
{
  "exists": false,
  "error": "API ID not found"
}
```

## Example

Bash

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/model/66b113a3ec1bc4460812c2d2/o3-mini_2025-01-31 \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

Powershell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$url = "https://trapi.research.microsoft.com/tmds/model/66b113a3ec1bc4460812c2d2/o3-mini_2025-01-31"
Invoke-RestMethod -Method GET -Uri $url -Authentication OAuth -Token $token.Token
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/model/{ApiId}/{Model}
    APIM->>APIM: Validate Azure AD token
    
    APIM->>APIM: Internal GET /tmds/deployments with ApiId header
    Note over APIM: Find apiPath matching ApiId
    
    alt API ID not found
        APIM->>Client: Return 404 Not Found with exists:false
    else API ID found
        APIM->>Backend API: GET /{apiPath}/models
        Backend API->>APIM: Return models list
        
        APIM->>APIM: Check if Model exists in models list
        APIM->>Client: Return exists:true/false
    end
:::

## Implementation Details

The endpoint performs the following operations:

1. Extracts the ApiId and Model parameters from the URL
2. Calls the internal `/tmds/deployments` endpoint to get the UapiPath for the specified ApiId
3. If no apiPath is found, returns a 404 error
4. Otherwise, calls the models endpoint for the specific API using the apiPath
5. Checks if the specified model exists in the response
6. Returns a JSON object with an "exists" boolean property

This endpoint is useful for checking model availability before attempting to use a specific model with an API.
