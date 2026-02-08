# Check Capacity for API Endpoint

## Overview

This endpoint checks if an API endpoint has sufficient token capacity to handle a request with a given token estimate. It makes a call to a Cosmos DB stored procedure (`getEndpointUsage`) to retrieve the current token usage information for the specified API endpoint and model, then determines whether the additional token usage would exceed defined capacity thresholds.

## Endpoint

`POST /tmds/capacitycheck/{ApiId}/{model}`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim.

## Request Parameters

### Path Parameters

- `ApiId` (required): The ID of the API to check capacity for
- `model` (required): The model/deployment name to check capacity for (e.g., "gpt-4", "gpt-4o")

### Request Body

The request body is tentitively optional. If the request deployment is "quiet" then you would get an immediate `true` response but for best results always provide a `tokenestimate`

```json
{
  "tokenestimate": 1200
}
```

Body Parameters:

- `tokenestimate` (required): The estimated number of tokens that will be used in the upcoming request

## Response

### Success Response

**Status Code:** 200 OK

```json
{
  "result": true
}
```

or 

```json
{
  "result": false
}
```

The `result` field indicates whether the API endpoint has sufficient capacity to handle a request with the estimated token usage:
- `true`: The request can be processed without exceeding capacity limits
- `false`: The request would likely exceed capacity limits and should be throttled

### Error Responses

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

## Example

```bash
curl -X POST \
  https://trapi.research.microsoft.com/tmds/capacitycheck/670528256820ca7d1ddc6857/gpt-4_turbo-2024-04-09 \
  -H 'Authorization: Bearer eyJ0eXAi...' \
  -H 'Content-Type: application/json' \
  -d '{
    "tokenestimate": 1200
  }'
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: POST /tmds/capacitycheck/{ApiId}/{model}
    
    APIM->>CosmosDB: Call getEndpointUsage stored procedure
    Note over APIM,CosmosDB: Passes ApiId and model parameters
    CosmosDB->>APIM: Return token usage statistics
    
    alt No matching documents found
        APIM->>Client: Return result:true (capacity available)
    else Documents found
        alt percentageActive < 80%
            APIM->>Client: Return result:false (insufficient active deployments)
        else maxTokenCount + tokenEstimate > latestPoolLimit * 0.8
            APIM->>Client: Return result:false (capacity limit would be exceeded)
        else Sufficient capacity available
            APIM->>Client: Return result:true (capacity available)
        end
    end
:::

## Implementation Details

The capacity check endpoint performs several evaluations to determine if a request should be allowed:

1. **Document Existence Check**: If no matching documents are found for the API and model combination, the endpoint returns `true` (capacity available) as there's no historical usage data to evaluate against.

2. **Active Deployment Check**: If the percentage of active deployments is less than 80%, the endpoint returns `false` to prevent sending requests to a potentially unhealthy backend with low availability.

3. **Capacity Threshold Check**: If the current maximum token count plus the estimated token usage would exceed 80% of the latest pool limit, the endpoint returns `false` to prevent capacity exhaustion.

4. **Default Approval**: If all checks pass, the endpoint returns `true`, indicating that the request can proceed.

This endpoint allows client applications to proactively check if their request would exceed capacity limits before attempting to make the actual API call, helping to prevent rate limiting and improve the overall user experience.
