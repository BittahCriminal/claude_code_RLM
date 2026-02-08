# Get API Path Mappings

## Overview

Retrieves the list of API path mapping objects stored in Cosmos DB via the `generatePathMappings` stored procedure. Each mapping describes an API (apiPath) together with its format, status, backend endpoints, and deployment metadata. An optional `apiPath` request header can be supplied to narrow the response to a single API.

This endpoint is useful for:

- Discovering all active TRAPI APIs and their backend endpoint definitions
- Inspecting deployment structures (endpoints, deployments arrays) for tooling or validation
- Feeding UI or automation that needs a catalogue of available API paths

## Endpoint

`GET /tmds/pathmappings`

## Authentication

Requires an Azure AD OAuth2 bearer token with the appropriate audience claim accepted by TRAPI.

## Request Parameters

### Headers
- `Authorization` (required): Bearer token.
- `apiPath` (optional): If provided, filters the result set to the specified API path (trim the leading slash if normally present; example: `gcr/shared/openai`). If omitted, all path mappings are returned.

## Response

### Success Response
**Status Code:** 200 OK

Returns a JSON array; each element is a path mapping object. Example:

```json
[
  {
    "apiPath": "gcr/shared/openai",
    "apiFormat": "openapi",
    "description": "Shared OpenAI gateway",
    "ci": "API",
    "isActive": true,
    "endpoints": [
      {
        "name": "primary-eastus",
        "url": "https://contoso-eastus.openai.azure.com/",
        "authType": "aad",
        "ci": "ENDPOINT",
        "backendType": "http",
        "resourcePoolName": "pool-eastus",
        "deployments": [ { "name": "gpt-4o" }, { "name": "gpt-4.1-mini" } ]
      }
    ]
  }
]
```

### Error Responses

**Status Code:** 500 Internal Server Error
```json
{
  "error": "Failed to retrieve path mappings from CosmosDB",
  "statusCode": 500
}
```

**Status Code:** 401 Unauthorized
```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

(401 is enforced by the common TMDS auth policies even though not explicitly set in the individual policy file.)

## Examples

Bash
```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/pathmappings \
  -H "Authorization: Bearer eyJ0eXAi..."
```

Filter by a single apiPath:
```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/pathmappings \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -H "apiPath: gcr/shared/openai"
```

PowerShell
```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$headers = @{ Authorization = "Bearer $($token.Token)" }
Invoke-RestMethod -Method GET -Uri "https://trapi.research.microsoft.com/tmds/pathmappings" -Headers $headers
```

PowerShell (filtered):
```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$headers = @{ 
  Authorization = "Bearer $($token.Token)" 
  apiPath       = "gcr/shared/openai" 
}
Invoke-RestMethod -Method GET -Uri "https://trapi.research.microsoft.com/tmds/pathmappings" -Headers $headers
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/pathmappings (optional apiPath header)
    APIM->>APIM: Validate Azure AD token
    APIM->>Managed Identity: Acquire token for Cosmos DB
    APIM->>Cosmos DB: POST /dbs/trapiDB/colls/configs/sprocs/generatePathMappings
    Note over APIM,Cosmos DB: Body is ["apiPath"] if provided else []
    Cosmos DB-->>APIM: 200 JSON array of path mappings OR error
    alt Success (200)
        APIM->>Client: 200 Array of mapping objects
    else Failure
        APIM->>Client: 500 { error, statusCode }
    end
:::

## Implementation Details

- The policy uses a managed identity to authenticate to Cosmos DB (AAD token inserted into a stored proc call).
- Stored procedure `generatePathMappings` returns all path mappings. Passing a single-element array filters to that apiPath.
- Partition key is fixed in the policy (`RUNTIMECI`).
- Defensive error handling: any non-200 from Cosmos yields a 500 with an error payload including the upstream status code.
- Response body from Cosmos is returned verbatim when successful; ensure downstream consumers can parse arrays of mapping objects.
- Filtering logic: If `apiPath` header is empty, sends `[]` (which instructs the sproc to return all mappings); otherwise sends `["{apiPath}"]`.

## Notes

- For large result sets clients should consider caching locally; the endpoint always executes the stored procedure.
- Fields such as `ci`, `backendType`, or `resourcePoolName` may evolve; build clients to ignore unknown properties.
- The example object is illustrative; actual fields depend on stored procedure output.
