# TMDS Wiki Models Listing

## Overview

`GET /tmds/wikimodels` returns the deployed model metadata (as produced by the `spDeployedModels` stored procedure in Cosmos DB) for use in wiki / documentation scenarios. The response is a raw JSON payload containing model deployment records; the policy performs only authentication, a stored procedure invocation, and response mediation.

## Endpoint

`GET /tmds/wikimodels`

## Authentication

Standard TMDS OAuth2 (AAD) requirements via `trapi-sec-oauth-cosmos` fragment. Caller must belong to an allowed security group or allowed managed identity.

## Access Restrictions

- Groups/identities limited by `allowedGroups` / `allowedIdentities` variables set in the policy.
- Read‑only; no mutation side effects.
- Partition key fixed to `RUNTIMECI`.

### For Developers

Use when you need the canonical deployed model list for UI, wiki generation, or audit output.

1. Acquire an AAD token with required audience.
2. Call `GET /tmds/wikimodels` (no additional headers required).
3. Handle 404 if no deployment data is currently available.
4. For non‑200, inspect returned JSON for code/message details.

## Request Parameters

### Headers

- `Authorization` (required): Bearer token.
  (No custom headers required.)

## GET /tmds/wikimodels

Returns the JSON body from the `spDeployedModels` Cosmos stored procedure.

### Response Codes

- 200 OK: Deployment model data payload.
- 401 Unauthorized: Missing or invalid token.
- 403 Forbidden: Caller not in allowed group/identity.
- 404 Not Found: Stored procedure returned 404 (no deployment data).
- 5xx: Error interacting with Cosmos or internal execution failure.

### Response Body (200 Example)

```json
[
  {
    "modelName": "gpt-4o-mini",
    "version": "2025-08-15",
    "deployment": "gpt4o-mini-eastus",
    "sku": "Standard",
    "region": "eastus",
    "status": "Active"
  }
]
```

### Error Response (404 Example)

```json
{
  "error": {
    "code": "NotFound",
    "message": "Could not get any deployment data."
  }
}
```

### Error Response (Generic)

```json
{ "error": { "code": "500", "message": "Error interacting with backend service." } }
```

## Example

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/wikimodels \
  -H "Authorization: Bearer eyJ0eXAi..."
```

## Service Flow

::: mermaid
sequenceDiagram
    participant Client
    participant APIM
    participant Cosmos as CosmosDB (spDeployedModels)

    Client->>APIM: GET /tmds/wikimodels
    APIM->>APIM: Validate AAD token (security fragment)
    APIM->>Cosmos: POST spDeployedModels (partitionKey RUNTIMECI)
    alt 200
        Cosmos-->>APIM: JSON model list
        APIM-->>Client: 200 OK (passthrough body)
    else 404
        Cosmos-->>APIM: 404 Not Found
        APIM-->>Client: 404 error JSON
    else other status
        Cosmos-->>APIM: error status & body
        APIM-->>Client: propagated status with sanitized error JSON
    end
    note over APIM: On unhandled exception -> 500 structured error
:::

## Notes

- Uses APIM Managed Identity for AAD token to Cosmos (header format `type=aad&ver=1.0&sig=...`).
- No caching performed by this policy; consumers should cache if needed.
- Response body is not reshaped (except for error normalization on non‑200 cases when Cosmos body is absent or non‑JSON).

## Changelog

- Initial documentation added (2025-09).
