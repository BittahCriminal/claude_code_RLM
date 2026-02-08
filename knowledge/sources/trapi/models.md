# List All Available Models

## Overview

This endpoint aggregates models from all available API endpoints defined in the TRAPI configuration. It retrieves the models list from each configured endpoint and returns a combined response.

## Endpoint

`GET /tmds/models`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim.

## Response

### Success Response

**Status Code:** 200 OK

The response is a JSON object where each key is an apiPath and the value is the model data from that endpoint:

```json
{
  "openai/gpt4": "{\"data\":[{\"id\":\"gpt-4\",\"object\":\"model\"},{\"id\":\"gpt-4-32k\",\"object\":\"model\"}]}",
  "openai/gpt4o": "{\"data\":[{\"id\":\"gpt-4o\",\"object\":\"model\"}]}",
  "openai/embeddings": "{\"data\":[{\"id\":\"text-embedding-ada-002\",\"object\":\"model\"}]}"
}
```

### Error Responses

**Status Code:** 401 Unauthorized

```json
{
  "error": "TRAPI: Unauthorized. Invalid or expired token."
}
```

## Example

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/models \
  -H 'Authorization: Bearer eyJ0eXAi...'
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/models
    APIM->>Azure Storage: GET /configs/{environment}/trapi-config.json
    Azure Storage->>APIM: Return config JSON
    
    Note over APIM: Extract apiPaths from config
    
    loop For each apiPath in config
        APIM->>Backend: GET https://trapi.research.microsoft.com/{apiPath}/models
        Note over APIM,Backend: Use client's Authorization token
        Backend->>APIM: Return models for this endpoint
        APIM->>APIM: Add response to results object
    end
    
    APIM->>Client: Return combined JSON object
:::

## Implementation Details

The endpoint performs these operations:

1. Loads the main TRAPI configuration file from Azure Blob Storage
2. Extracts the list of apiPaths from the configuration
3. For each apiPath:
   - Makes a request to `/{apiPath}/models` endpoint
   - If the request succeeds (200 OK), adds the response to the results
4. Returns a JSON object where:
    - Keys are the apiPath
    - Values are the raw JSON responses from each models endpoint

This provides a comprehensive view of all available models across all TRAPI endpoints, enabling clients to discover capabilities without making multiple API calls.
