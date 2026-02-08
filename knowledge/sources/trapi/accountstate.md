# Account Suspension Status

## Overview

This endpoint retrieves the suspension status of all accounts and deployments. It checks if any account/deployment pairs are currently suspended.

## Endpoint

`GET /tmds/accountstate`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim. Access is restricted to the TRAPI Managed Identity.

## Access Restrictions

⚠️ **INTERNAL USE ONLY**: This API endpoint is restricted to the TRAPI service's Managed Identity.

External access is denied by an Azure AD token validation that requires a specific Object ID (OID) claim matching the TRAPI service's Managed Identity.

### For Developers

If you need to test or debug this endpoint:

1. **Update APIM Policy**: The APIM administrator will need to add your OID to the policy:

   ```xml
   <validate-azure-ad-token>
     <required-claims>
       <claim name="oid" match="any">
         <value>{{trapi-ManagedIdentityId}}</value>
         <value>YOUR-AZURE-AD-OID-HERE</value>
       </claim>
     </required-claims>
   </validate-azure-ad-token>
   ```

2. Conduct your tests / dev work against the API / Endpoint
3. Remove your OID when testing is complete.

## Response

### Success Response

**Status Code:** 200 OK

```json
[
  {
    "account": "gcraoai2sw2",
    "deploymentName": "o1_2024-12-17",
    "Suspended": false
  },
  {
    "account": "gcrgpt4aoai2",
    "deploymentName": "gpt-4o_2024-08-06",
    "Suspended": true
  },
  {
    "account": "gcrgpt4aoai2",
    "deploymentName": "gpt-4o-mini_2024-07-18",
    "Suspended": false
  },
  ...
]
```

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

**Status Code:** 503 Service Unavailable

```json
{
  "error": "Account model limits configuration unavailable"
}
```

### Example

Bash

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/accountstate \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

Powershell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$url = "https://trapi.research.microsoft.com/tmds/accountstate"
Invoke-RestMethod -Method GET -Uri $url -Authentication OAuth -Token $token.Token
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/accountstate
    
    alt Cache Miss
        APIM->>Azure Storage: GET /configs/{environment}/trapi-accountModelLimits.json
        Azure Storage->>APIM: Return model limits JSON
        APIM->>APIM Cache: Store accountModelLimits for 60 minutes
    end
    
    loop For each account/deployment
        APIM->>APIM Cache: Lookup Suspend-{account}-{deployment}
    end
    
    APIM->>Client: Return suspension status for all accounts
:::
