# Get Current Token Usage State

## Overview

This endpoint retrieves the current token usage state for a specific account and deployment combination. It returns information about the token usage, including whether the account/deployment is suspended, the current token count, and the tracking epoch.

## Endpoint

`GET /tmds/tokenstate/{account}/{deploymentName}`

## Authentication

This endpoint doesn't appear to have explicit authentication requirements in the policy, but it's recommended to include an Authorization token for consistency with other endpoints.

## Request Parameters

### Path Parameters

- `account` (required): The account name to check (e.g., "resrch-api-aiservices")
- `deployment` (required): The deployment name to check (e.g., "gpt-4", "gpt-4o")

## Response

### Success Response

**Status Code:** 200 OK

```json
{
  "Account": "resrch-api-aiservices",
  "Deployment": "gpt-4",
  "Epoch": "2023-05-20T15:30:00",
  "Total": "85624",
  "Suspend": "Active"
}
```

The response includes:

- `Account`: The AOAI account identifier
- `Deployment`: The deployment/model name
- `Epoch`: The timestamp of the current tracking period (typically reset each minute)
- `Total`: The current token count for this account/deployment pair
- `Suspend`: The suspension status ("Active" if not suspended, otherwise contains suspension reason []`429`|`exhausted`|`preemptive`])

## Example

``bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/tokenstate/resrch-api-aiservices/gpt-4
``

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/tokenstate/{account}/{deploymentName}
    
    APIM->>APIM: Extract account and deployment from URL
    
    APIM->>APIM Cache: Lookup Epoch-{account}-{deployment}
    APIM->>APIM Cache: Lookup Total-{account}-{deployment}
    APIM->>APIM Cache: Lookup Suspend-{account}-{deployment}
    
    APIM->>APIM: Format response with Liquid template
    
    APIM->>Client: Return token state information
:::

## Implementation Details

This endpoint performs three cache lookups to retrieve the current state data:

1. **Epoch lookup**: Gets the timestamp for the current tracking period
2. **Total lookup**: Gets the current token count for this account/deployment
3. **Suspend lookup**: Checks if the account/deployment is currently suspended

The data is retrieved from the APIM distributed cache, where values are typically set by the `/tmds/tracktokens` endpoint as tokens are consumed. If a value isn't found in the cache, default values are provided:

- Epoch: "null"
- Total: "0"
- Suspend: "Active"

This endpoint is useful for monitoring current token usage and determining if an account/deployment is currently suspended before attempting to use it.