# Identity Object Lookup

## Overview

Resolves an Entra ID object by GUID. The lookup first attempts to find a directory object by objectId; if not found, it attempts to resolve a managed identity by clientId (service principal appId). Useful for validating IDs before granting access or storing references (e.g., in Manage MSI flows).

## Endpoint

`GET /tmds/idcheck/{id}`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate (`api://trapi`) audience claim.

## Request Parameters

### Path Parameters

- `id` (required, GUID): The identifier to resolve.
  - Tries `objectId` first (directory object).
  - If not found, tries managed identity by `clientId`/service principal `appId`.

### Headers

- `Authorization` (required): Bearer token.

## Responses

### 200 OK — Object found

Example (Managed Identity):

```json
{
  "name": "contoso-app-mi",
  "type": "ManagedIdentity",
  "objectId": "00000000-0000-0000-0000-000000000000"
}
```

Example (User):

```json
{
  "name": "Adele Vance",
  "type": "User",
  "objectId": "11111111-1111-1111-1111-111111111111"
}
```

Example (Group):

```json
{
  "name": "TRAPI Group",
  "type": "Group",
  "objectId": "11111111-1111-1111-1111-111111111111"
}
```

Example (Directory Object / App Registration):

```json
{
  "name": "trapi-oauth-backend",
  "type": "DirectoryObject",
  "objectId": "00000000-0000-0000-0000-000000000000"
}
```

### 400 Bad Request — Invalid id

```json
{
  "error": "Invalid id. Expected a GUID."
}
```

### 404 Not Found — No matching object

```json
{
  "error": "No object found for the provided id as objectId or clientId."
}
```

### 502 Bad Gateway — Upstream error

```json
{
  "error": "Upstream Graph lookup failed."
}
```

## Examples

### curl

```bash
curl -X GET \
  "https://trapi.research.microsoft.com/tmds/idcheck/00000000-0000-0000-0000-000000000000" \
  -H "Authorization: Bearer eyJ0eXAi..."
```

Typical 200 OK response:

```json
{
  "name": "contoso-app-mi",
  "type": "ManagedIdentity",
  "objectId": "00000000-0000-0000-0000-000000000000"
}
```

### PowerShell

```pwsh
# Acquire an AAD token for TRAPI (adjust resource if needed)
$token = (Get-AzAccessToken -ResourceUrl "api://trapi").Token

$id = "00000000-0000-0000-0000-000000000000"
$url = "https://trapi.research.microsoft.com/tmds/idcheck/$id"
$headers = @{ Authorization = "Bearer $token" }

Invoke-RestMethod -Method GET -Uri $url -Headers $headers | ConvertTo-Json -Depth 5
```

Example output:

```json
{
  "name": "contoso-app-mi",
  "type": "ManagedIdentity",
  "objectId": "00000000-0000-0000-0000-000000000000"
}
```

## Service Flow

::: mermaid
sequenceDiagram
  participant Client
  participant APIM
  participant TMDS
  participant Graph as Microsoft Entra / Graph

  Client->>APIM: GET /tmds/idcheck/{id}
  APIM->>APIM: Validate AAD token (audience {{oauth-appid}})
  APIM->>TMDS: Prepare lookup input
  TMDS->>Graph: Lookup directory object by objectId={id}
  alt found
    Graph-->>TMDS: Object details
    TMDS-->>APIM: 200 { name, type, objectId }
    APIM-->>Client: 200 OK
  else not found
    TMDS->>Graph: Lookup managed identity by clientId/appId={id}
    alt found
      Graph-->>TMDS: MI details
      TMDS-->>APIM: 200 { name, type=ManagedIdentity, objectId }
      APIM-->>Client: 200 OK
    else still not found
      TMDS-->>APIM: 404 No matching object
      APIM-->>Client: 404 Not Found
    end
  end
:::

## Notes

- Source spec: `api-management-policies/tmds/TMDS - TRAPI Metadata Service.openapi+json.json` (operationId: `idcheck`).
- Common uses: validate a provided GUID represents a User, Group or Managed Identity before storing or authorizing it.