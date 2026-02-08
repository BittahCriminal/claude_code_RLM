# Health Check Reports

## Overview

Returns the most recent TMDS health check report stored in the `trapireportstorage` storage account. The policy first tries to download `latest_healthcheck.json`. If that blob is missing it enumerates every blob in the `healthcheck-reports` container, finds the most recently modified entry, and returns its contents instead. The raw JSON payload is streamed back to the caller along with the blob name that satisfied the request.

Use this endpoint when you need the current health telemetry that TRAPI publishes for monitoring or troubleshooting dashboards.

## Endpoint

`GET /tmds/healthcheckreports`

## Authentication

Requires an Azure AD bearer token for the standard TMDS audience (`api://trapi`). Unauthorized callers receive `401` due to the common TMDS auth pipeline.

## Request Parameters

No query parameters, headers, or body values are required beyond `Authorization`.

## Response

### Success Response

**Status Code:** 200 OK

Headers:

- `Content-Type`: Content type from the blob (defaults to `application/json`).
- `X-TRAPI-HealthCheck-Blob`: Name of the blob that fulfilled the request (either `latest_healthcheck.json` or the fallback blob).

Example body (`application/json`):

```json
{
  "generatedAt": "2025-10-15T12:00:00Z",
  "status": "healthy",
  "checks": [
    { "name": "storage-connectivity", "status": "pass" },
    { "name": "apim-probe", "status": "pass" }
  ]
}
```

### Error Responses

#### 404 Not Found

```json
{ "error": "No health check reports found" }
```

Returned when the container is empty or the fallback blob download fails.

#### 500 Internal Server Error

```json
{ "error": "Failed to retrieve health check report", "statusCode": 500 }
```

Raised when Storage returns an unexpected error or enumeration cannot be performed.

## Examples

### Curl

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/healthcheckreports \
  -H "Authorization: Bearer eyJ0eXAi..."
```

### PowerShell

```pwsh
$apiAuthScope = "api://trapi"
$token = Get-AzAccessToken -ResourceURL $apiAuthScope -AsSecureString

$headers = @{ Authorization = "Bearer $($token.Token)" }
Invoke-RestMethod -Method GET -Uri "https://trapi.research.microsoft.com/tmds/healthcheckreports" -Authentication OAuth -Token $token.token
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: GET /tmds/healthcheckreports
    APIM->>APIM: Validate Azure AD token
    APIM->>Storage: GET latest_healthcheck.json (managed identity)
    alt Blob exists
        Storage-->>APIM: 200 JSON
        APIM-->>Client: 200 JSON + X-TRAPI-HealthCheck-Blob header
    else Blob missing (404)
        APIM->>Storage: GET container list (comp=list)
        Storage-->>APIM: XML blob inventory
        APIM->>Storage: GET most recent blob
        alt Fallback success
            Storage-->>APIM: 200 JSON
            APIM-->>Client: 200 JSON + header (fallback blob name)
        else No blobs / download fails
            APIM-->>Client: 404 {"error": "No health check reports found"}
        end
    end
:::

## Implementation Details

- Auth: Uses the shared TMDS Azure AD validation fragment (audience `{{oauth-appid}}`).
- Storage access: Employs the APIM system-assigned managed identity with `authentication-managed-identity resource="https://storage.azure.com"` to call `trapireportstorage` directly.
- Preferred blob: Attempts to fetch `latest_healthcheck.json` to avoid listing overhead when the symbolic blob exists.
- Fallback discovery: When the preferred blob returns `404`, the policy issues `?restype=container&comp=list` to enumerate blobs, parses the XML to find the most recently modified entry, and downloads that blob instead.
- Response metadata: Always echoes the blob name in `X-TRAPI-HealthCheck-Blob`, allowing callers to understand whether data came from the canonical name or a fallback file.
- Error handling: Unexpected Storage errors produce `500`; empty containers or failed fallback downloads result in `404`.

## Notes

- The container listing is only triggered when `latest_healthcheck.json` is absent, which keeps the hot path efficient.
- If you batch-call this endpoint, respect caching on your side; the report content only changes when health jobs update the blob.
- The policy does not modify the JSON payload—clients receive exactly what the TRAPI reporting job published.
