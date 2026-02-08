# Track Token Usage

## Overview

This endpoint tracks token usage for a specific account and deployment combination. It updates the token count in the APIM cache and can trigger suspension if limits are exceeded. This is a core component of the token tracking and quota enforcement system.

## Endpoint

`POST /tmds/tracktokens/{account}/{deployment}`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim. Access is restricted to the TRAPI Managed Identity through OID validation.

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

- `account` (required): The account name to track tokens for (e.g., "resrch-api-aiservices")
- `deployment` (required): The deployment name to track tokens for (e.g., "gpt-4", "gpt-4o")

### Request Body

```json
{
  "prompt_tokens": 1797,
  "completion_tokens": 63,
  "total_tokens": 1860
}
```

Body Parameters

- `total_tokens` (optional): The total number of tokens used in this request
- `prompt_tokens` and `completion_tokens` (optional): Used to calculate total tokens if total_tokens is not provided

Either `total_tokens` OR **both** `prompt_tokens` and `completion_tokens` must be provided.

In typical usage we are simply passing the entire `usage` object from the `Response` Object body.

### Response

Success Response

**Status Code:** 204 No Content

Error Responses

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

## Example

```json
curl -X POST \
  https://trapi.research.microsoft.com/tmds/tracktokens/resrch-api-aiservices/gpt-4 \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt_tokens": 1797,
    "completion_tokens": 63,
    "total_tokens": 1860
  }'
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: POST /tmds/tracktokens/{account}/{deployment}
    APIM->>APIM: Validate Azure AD token (OID check)

    alt No maxTokens in cache
        APIM->>APIM: GET /tmds/tokenlimits/{account}/{deployment}
        APIM->>APIM Cache: Store maxTokens for 1 hour
    end
    
    APIM->>APIM Cache: Lookup Epoch-{account}-{deployment}
    APIM->>APIM Cache: Lookup Total-{account}-{deployment}
    
    alt New minute
        APIM->>EventHub: Log token usage for previous minute
        APIM->>APIM Cache: Reset token count with new tokens
    else Same minute
        APIM->>APIM Cache: Add new tokens to existing count
    end
    
    alt Token limit exceeded
        APIM->>APIM: POST /tmds/suspend/{account}/{deployment}
        Note over APIM: Reason: "exhausted"
    else 120% pre-emptive protection triggered
        APIM->>APIM: POST /tmds/suspend/{account}/{deployment}
        Note over APIM: Reason: "prempt-protection"
    end
    
    APIM->>CosmosDB: Store token usage data
    APIM->>Client: Return 204 No Content
:::

## Updates in Token Tracking Policy

### Token Calculation

- The policy now calculates `totalTokens` from `prompt_tokens` and `completion_tokens` if `total_tokens` is not provided.
- If no token information is found, `totalTokens` defaults to `-1`.

### Cache Management

- The policy fetches and stores `maxTokens` from the token limits API if not found in the cache.
- Caches `Epoch`, `Total`, and `Max` values for 300 seconds.

### Suspension Logic

- Introduced pre-emptive protection logic to suspend accounts when token usage exceeds 120% of the maximum limit.
- Sends a suspension request with detailed information when limits are exceeded.

### CosmosDB Integration

- Token usage data is now sent to CosmosDB for tracking and analysis.

### Logging

- Logs token usage and suspension events for monitoring and debugging purposes.

This endpoint is a critical component of the token usage monitoring and quota enforcement system.
