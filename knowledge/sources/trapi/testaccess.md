# Test User Access to API

## Overview

This endpoint determines if a specific user has access to an API endpoint by checking their Azure AD Object ID (OID) against the permissions configuration. It allows applications to verify API access rights before attempting to make API calls.

## Endpoint

`GET /tmds/testaccess`

## Authentication

Requires a valid Azure AD OAuth2 token with the appropriate audience claim.

## Request Parameters

### Headers

- `OID` (required): The Azure AD Object ID of the user to check access for
- `apiPath` (optional): The URL apiPath to check access to (either this or ApiId must be provided)
- `ApiId` (optional): The API ID to check access to (either this or apiPath must be provided)

## Response

### Success Response

**Status Code:** 200 OK

```json
{
  "hasAccess": true||false
}
```

### Error Responses

**Status Code:** 400 Bad Request

```json
{
  "error": "OID header is required"
}
```

or

```json
{
  "error": "Either apiPath or ApiId header must be provided"
}
```

**Status Code:** 404 Not Found

```json
{
  "error": "No apiPath found for the provided ApiId",
  "hasAccess": false
}
```

**Status Code:** 500 Internal Server Error

```json
{
  "error": "Failed to retrieve apiPath for the provided ApiId",
  "status": 500
}
```

or

```json
{
  "error": "Failed to retrieve user access information",
  "status": 500
}
```

## Example

Bash

```bash
# Test access using apiPath
curl -X GET \
  https://trapi.research.microsoft.com/tmds/testaccess \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'apiPath: /openai/gpt4'

# Test access using ApiId
curl -X GET \
  https://trapi.research.microsoft.com/tmds/testaccess \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'OID: 00000000-0000-0000-0000-000000000000' \
```

Powershell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$url = "https://trapi.research.microsoft.com/tmds/testaccess"
$headers = @{
    apiPath = "gcr/shared/openai"
    OID = "00000000-0000-0000-0000-000000000000"
}
Invoke-RestMethod -Method GET -Uri $url -Authentication OAuth -Token $token.Token
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/testaccess
    
    APIM->>APIM: Validate headers (OID and apiPath/ApiId)
    
    alt ApiId provided but no apiPath
        APIM->>APIM: GET /tmds/deployments with ApiId header
        APIM->>APIM: Extract apiPath from response
    end
    
    APIM->>APIM: GET /tmds/access/{OID}
    Note over APIM: Uses same authentication token
    
    APIM->>APIM: Check if apiPath is in user's accessible APIs
    APIM->>Client: Return hasAccess: true/false
:::

## Implementation Details

The testaccess endpoint implements a two-step verification process:

1. First, it resolves the API identifier:
   - If a `apiPath` is provided, it uses that directly
   - If an `ApiId` is provided, it calls the `tmds/deployments` endpoint to find the corresponding `apiPath`
2. Then it verifies the user's access:
   - It calls the `/tmds/access/{OID}` endpoint to retrieve all APIs the user can access
   - It checks if the requested API's URL apiPath is in the user's accessible list
   - It returns a boolean result indicating whether access is allowed

This endpoint is particularly useful for frontend applications that need to conditionally show or hide API-dependent features based on the user's permissions.
