# Get Detailed Token Usage Information

## Overview

This endpoint retrieves comprehensive token usage information for all accounts and deployments, including token capacities, suspension status, current token counts, and tracking epochs. It aggregates data from the Cosmos DB stored procedure `getLatestTokenUsage` to provide a complete view of system-wide token consumption.

## Endpoint

`GET /tmds/tokenusage`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim. 

## Response

### Success Response

**Status Code:** 200 OK

```json
[
  {
    "account": "gcrgpt4aoai9",
    "deployment": "gpt-4o_2024-11-20",
    "tokenCount": 17728,
    "epoch": "2025-04-15 08:12",
    "resourcePool": "gcrshared",
    "limits": {
      "account": 300000,
      "pool": 600000
    },
    "activeUsers": 3,
    "deploymentState": "active",
    "trapiEndpoints": [
      "/gcr/shared/openai"
    ],
    "activeRecord": true
  },
  {
    "account": "gcraoai6sw2",
    "deployment": "o1_2024-12-17",
    "tokenCount": 15178,
    "epoch": "2025-04-15 08:11",
    "resourcePool": "msri",
    "limits": {
      "account": 600000,
      "pool": 600000
    },
    "activeUsers": 2,
    "deploymentState": "active",
    "trapiEndpoints": [
      "/msri/openai"
    ],
    "activeRecord": false
  }
]
```

Response fields:

* `account`: The account identifier
* `deployment`: The model/deployment name
* `capacity`: Maximum token limit configured for this account/deployment
* `tokenCount`: Current token usage count for the current tracking period
* `epoch`: Timestamp of the current tracking period UTC minute (typically reset each minute)
* `resourcePool`: The resource pool associated with the account/deployment
* `limits`: Object containing the token limits for the account and resource pool
  * `account`: Token limit for the account
  * `pool`: Token limit for the resource pool
* `activeUsers`: Number of active users for the account/deployment
* `deploymentState`: Current state of the deployment (e.g., active, suspended)
* `trapiEndpoints`: List of TRAPI endpoints associated with the account/deployment
* `activeRecord`: Indicates if the record is active or not in the current tracking period

### Error Responses

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

**Status Code:** 503 Service Unavailable

```json
{
  "error": "TRAPI: Account model limits configuration unavailable"
}
```

## Example

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/tokenusage \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

```powershell
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString
$tokenUsage = Invoke-RestMethod -Method GET -Uri "https://trapi.research.microsoft.com/tmds/tokenusage" -ContentType "application/json" -Authentication OAuth -Token $token.Token -ResponseHeadersVariable ResponseHeaders -StatusCodeVariable ResponseCode
$tokenUsage | Where-Object {$_.epoch -ge ((Get-Date).ToUniversalTime()).AddMinutes(-5).toString("yyyy-MM-dd hh:mm")} | ft * -AutoSize
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/tokenusage
    APIM->>CosmosDB: Call getLatestTokenUsage stored procedure
    CosmosDB->>APIM: Return token usage data
    APIM->>Client: Return complete token usage array
:::

## Implementation Details

The endpoint performs these operations:

1. Calls the Cosmos DB stored procedure `getLatestTokenUsage` to retrieve token usage data.
2. Processes the response from Cosmos DB.
3. Returns the data as a JSON array to the client.

This endpoint provides a holistic view of token usage across all configured models and accounts, making it useful for monitoring, reporting, and capacity planning.
