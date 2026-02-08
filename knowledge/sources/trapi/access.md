# User API Access Information

## Overview
This endpoint retrieves a list of APIs that a specific user has access to, based on their Azure AD Object ID (OID). It retrieves access information by checking security groups and managed identities in the configuration.

## Endpoint
`GET /tmds/access/{OID}`

## Authentication
Requires an Azure AD OAuth2 token with the appropriate audience claim.

## Request Parameters

### Path Parameters
- `OID` (required): The Azure AD Object ID of the user to check access for.

### Headers
- `Authorization` (required): Bearer token for authentication.

## Response

### Success Response
**Status Code:** 200 OK

```json
[
  {
    "apiPath": "msrc/shared/openai"
  },
  {
    "apiPath": "msrai4s/shared/openai"
  },
  {
    "apiPath": "msrhf/shared/openai"
  }
]
```

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

**Status Code:**  500 Internal Server Error

```json
{
  "error": "Failed to retrieve user access information"
}
```

## Examples

Bash

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/access/00000000-0000-0000-0000-000000000000 \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

Powershell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$url = "https://trapi.research.microsoft.com/tmds/access/00000000-0000-0000-0000-000000000000"
Invoke-RestMethod -Method GET -Uri $url -Authentication OAuth -Token $token.Token
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/access/{OID}
    APIM->>Azure Storage: GET /configs/{environment}/trapi-config.json
    Azure Storage->>APIM: Return config JSON
    APIM->>Microsoft Graph: GET /v1.0/users/{OID}/memberOf
    Microsoft Graph->>APIM: Return user groups
    APIM->>APIM: Process access permissions
    APIM->>Client: Return accessible APIs
:::
