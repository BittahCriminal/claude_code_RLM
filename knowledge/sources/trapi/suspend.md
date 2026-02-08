# Suspend an Account/Deployment

## Overview

This endpoint suspends an account/deployment pair by creating a temporary suspension record in the APIM cache. This prevents further requests to the specified account/deployment until the suspension period ends (typically until the next minute). The suspension mechanism is used by various TRAPI components to implement rate limiting and quota enforcement.

## Endpoint

`POST /tmds/suspend/{account}/{deployment}`

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

- `account` (required): The account name to suspend (e.g., "resrch-api-aiservices")
- `deployment` (required): The deployment name to suspend (e.g., "gpt-4", "gpt-4o")

### Request Body

```json
{
  "reason": "429|highwater|exhausted|prempt-protection",
  "tokencount": 123456,
  "maxtokens": 100000
}
```

### Body Parameters

- `reason` (required): The reason for suspension
  - `429`: Rate limit exceeded (HTTP 429 response from backend)
  - `highwater`: High traffic threshold reached
  - `exhausted`: Token quota exhausted for the current period
- `prempt-protection`: Pre-emptive protection triggered (usage approaching limit)
- `tokencount` (optional): Current token usage count that triggered the suspension
- `maxtokens` (optional): Maximum token limit for the account/deployment pair

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

```bash
curl -X POST \
  https://trapi.research.microsoft.com/tmds/suspend/gcraoai9eus2spot/gpt-4o_2024-05-13 \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'Content-Type: application/json' \
  -d '{
    "reason": "exhausted",
    "tokencount": 123456,
    "maxtokens": 100000
  }'
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: POST /tmds/suspend/{account}/{deployment}
    APIM->>APIM: Validate Azure AD token
    
    alt Token validation fails
        APIM->>Client: Return 401 Unauthorized
    end
    
    APIM->>APIM: Calculate seconds until next minute
    
    APIM->>APIM Cache: Store suspension record (Suspend-{account}-{deployment})
    Note over APIM Cache: Sets expiration to next minute
    
    APIM->>EventHub: Log suspension event with details
    Note over EventHub: Includes suspension reason and timing
    
    alt Reason is 429
        APIM->>APIM: Call tracktokens endpoint
        APIM->>CosmosDB: Log token usage and suspension details
    end
    
    APIM->>Client: Return 204 No Content
:::

## Implementation Details

When an account/deployment pair is suspended:

1. A cache entry with key Suspend-{account}-{deployment} is created in the APIM cache
2. The cache entry typically expires at the next full minute boundary
3. The load balancer and token tracking components check for this cache entry
4. When the entry exists, requests are rejected with a 429 status code
5. The suspension event is logged to EventHub for monitoring and analysis

This mechanism helps prevent quota overages and provides protection against excessive API usage.

## Updates in Suspension Policy

### Cache Suspension

- Suspension reason is now stored in the cache with a duration calculated as the seconds until the next full UTC minute.

### Token Tracking Integration

- Explicitly calls the `tracktokens` endpoint to suspend the endpoint when the reason is `429`.

### Logging

- Logs suspension events with details such as token count, maximum tokens, and suspension duration.

### Fast Termination

- Returns a `204 No Content` response immediately after processing the suspension.
