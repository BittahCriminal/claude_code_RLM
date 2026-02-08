# Capability Example Assets

## Overview

This endpoint returns code examples from the TRAPI example suite. It reads the `capability_mapping.json` manifest from Azure Storage and selects the correct example file based on the request filters. Clients can preview the example inline or download the file directly.

## Endpoint

`POST /tmds/examples`

## Authentication

Requires an Azure AD OAuth2 token issued for the TRAPI audience (`{{oauth-appid}}`).

## Request Body

JSON payload with the following properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `capability` | string | Yes | Capability key from `capability_mapping.json` (for example `audio`, `chatCompletion`). |
| `api-version` | string | No | Version bucket to use (for example `v1`, `fallback`). Defaults to the capability's configured value if omitted. |
| `language` | string | No | Language bucket (for example `python`, `cURL`, `powershell`). Defaults to the capability defaults or the first available entry. |
| `example` | string | No | Specific example node inside the language bucket. Falls back to the capability `default`. |
| `display` | string | No | When set to `online`, the response is rendered as text. Any other value (or omission) returns the file as a download. |

### Sample Request

```json
{
  "capability": "audio",
  "api-version": "fallback",
  "language": "python",
  "display": "online"
}
```

## Response

### Success (inline preview)

**Status Code:** 200 OK  
**Content-Type:** `text/plain`  
**Headers:**

- `X-TRAPI-Example-Capability`: Capability key that resolved to the asset.
- `X-TRAPI-Example-Version`: Version bucket that was selected (for example `v1`, `fallback`).
- `X-TRAPI-Example-Language`: Language bucket used for the example.

```python
# Text-to-speech preview example
from openai import OpenAI

client = OpenAI()
...
```

### Success (file download)

**Status Code:** 200 OK  
**Content-Type:** inherits from the stored blob (defaults to `application/octet-stream`).  
**Headers:**

- `Content-Disposition: attachment; filename="speech.py"`
- `X-TRAPI-Example-Capability`
- `X-TRAPI-Example-Version`
- `X-TRAPI-Example-Language`

Body contains the file bytes.

### Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid JSON payload or missing `capability`. |
| 401 | Failed Azure AD token validation. |
| 404 | Capability, language, example, or blob asset not found. |
| 500 | Failed to parse capability mapping or resolve an example path. |
| 503 | Capability mapping manifest unavailable. |

## Examples

### cURL

```bash
curl -X POST \
  https://trapi.research.microsoft.com/tmds/examples \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
        "capability": "chatCompletion",
        "api-version": "v1",
        "language": "python",
        "display": "download"
      }' --output chat-completion.py
```

### PowerShell

```pwsh
$body = @{
    capability = "audio"
    "api-version" = "fallback"
    language = "powershell"
    display = "online"
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post `
    -Uri "https://trapi.research.microsoft.com/tmds/examples" `
    -Authentication OAuth `
    -Token (Get-AzAccessToken -ResourceUrl "api://trapi" -AsSecureString).Token `
    -ContentType "application/json" `
    -Body $body
```

## Service Flow

::: mermaid
sequenceDiagram
    Client->>APIM: POST /tmds/examples (JSON filters)
    APIM->>Azure Storage: GET capability_mapping.json
    Azure Storage-->>APIM: Mapping manifest
    APIM->>APIM: Resolve capability, version, language, example
    APIM->>Azure Storage: GET /examples/{env}{apiPath}/{example}
    Azure Storage-->>APIM: Example blob contents
    APIM-->>Client: Return inline text or downloadable file
:::

## Implementation Details

- Uses the same Azure AD validation policy as other TMDS endpoints.
- Loads `capability_mapping.json` from `https://{{Trapi-Config-Storage-Account}}/examples/{{Trapi-Environment}}{context.Api.Path}/`.
- Applies capability defaults (`defaults` block or capability `default`) when optional fields are omitted.
- Supports inline preview via `display = online`; otherwise emits an attachment using the blob content type and file name.
- Returns descriptive error payloads for invalid JSON, missing capability data, and unavailable blobs.
