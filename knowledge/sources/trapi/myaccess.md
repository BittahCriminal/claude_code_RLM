# Get My Accessible APIs

## Overview

The operation allows users to check their access permissions. It checks all available APIs and returns a list of all the APIs the user has got permissions to access.

## Endpoint

`GET /tmds/myaccess`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim.

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
  https://trapi.research.microsoft.com/tmds/myaccess \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

Powershell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$url = "https://trapi.research.microsoft.com/tmds/myaccess"
Invoke-RestMethod -Method GET -Uri $url -Authentication OAuth -Token $token.Token
```

## Service Flow

:::mermaid
sequenceDiagram
    participant User
    participant API Management
    participant /access Endpoint
    User->>API Management: GET /tmds/myaccess (with Azure AD Token)
    API Management->>API Management: Validate Azure AD Token
    API Management->>API Management: Extract User OID
    API Management->>/access Endpoint: GET /access/{OID}
    /access Endpoint-->>API Management: Access Details
    API Management-->>User: Forward Access Details
:::