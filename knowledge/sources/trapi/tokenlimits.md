# Get Token Limits for an Account/Deployment

## Overview

This endpoint retrieves the maximum token capacity limit for a specific account and deployment combination. It provides information about token quotas that determine how many tokens can be consumed before rate limiting occurs.

## Endpoint

`GET /tmds/tokenlimits/{account}/{deployment}`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim. Access is restricted to the TRAPI Managed Identity through claims validation.

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

## Request Parameters

### Path Parameters

- `account` (required): The account name to check (e.g., "resrch-api-aiservices")
- `deployment` (required): The deployment name to check (e.g., "gpt-4", "gpt-4o")

### Headers

- `Authorization` (required): Bearer token for authentication

## Response

### Success Response

**Status Code:** 200 OK

```json
{
  "capacity": 2000000
}
```

The capacity value represents the maximum number of tokens allowed for the account/deployment pair per time period.

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
  "error": "No capacity configuration found for specified account and deployment"
}
```

**Status Code:** 503 Service Unavailable

```json
{
  "error": "Account model limits configuration unavailable"
}
```

## Example

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/tokenlimits/resrch-api-aiservices/gpt-4 \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/tokenlimits/{account}/{deployment}
    
    APIM->>APIM: Validate Azure AD token
    
    alt Cache Miss
        APIM->>Azure Storage: GET /configs/{environment}/trapi-accountModelLimits.json
        Azure Storage->>APIM: Return model limits JSON
        APIM->>APIM Cache: Store accountModelLimits for 60 minutes
    end
    
    APIM->>APIM: Find matching account/deployment
    
    alt Account/Deployment Found
        APIM->>Client: Return capacity configuration (200 OK)
    else Account/Deployment Not Found
        APIM->>Client: Return 404 Not Found
    end
:::

## Implementation Details

The endpoint follows these steps:

1. Validates the Azure AD token to ensure authorized access
2. Checks if account model limits exist in the APIM cache
3. If not found in cache, retrieves the configuration from Azure Blob Storage
4. Searches the configuration for a match on both account and deployment name
5. If found, returns the capacity value as an integer
6. If not found, returns a 404 error response

This endpoint is primarily used by the token tracking system to determine when to apply rate limiting based on token consumption.
