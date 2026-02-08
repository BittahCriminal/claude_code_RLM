# Manage Managed Identity Grants

## Overview

These endpoints let authenticated users manage their own Managed Identity grants for a specific API path. Grants are stored in the ADMINCI configuration document in Cosmos DB. Users can list, add/update, or remove identities they own for an API they have access to.

## Endpoint

`GET /tmds/managemsi`  
`POST /tmds/managemsi`  
`DELETE /tmds/managemsi`

## Authentication

Requires an Azure AD OAuth2 token with the appropriate audience claim.

## Access Restrictions

- Access is limited to APIs that the caller is authorized to use (verified through internal access checks).
- GET responses are filtered to only identities whose `owner` equals the caller’s `preferred_username` (falling back to `upn`).
- POST / DELETE always guarantee the calling user remains an owner (the caller is auto-added on POST if omitted and cannot delete their own ownership via the owners-removal path).
- Multiple owners per Managed Identity are now supported. The `owner` field in a POST body may be:
  - A single string: `"alias@microsoft.com"`
  - A CSV string: `"a@microsoft.com,b@microsoft.com"`
  - A JSON array: `["a@microsoft.com","b@microsoft.com"]`
  - A stringified JSON array: `"[\"a@microsoft.com\",\"b@microsoft.com\"]"`
  All forms are normalized to a distinct (case–insensitive) list and merged into a single identity record whose `owner` property is an array of all owners (legacy single-owner records are auto-upgraded).
- POST is restricted to human Users; Managed Identities or service principals cannot create or update grants.
- GCR APIs are not supported for Managed Identities in POST requests (returns 501).

### For Developers

If you need to test or debug these endpoints:

1. Discover API paths you can access: `GET /tmds/myaccess`.
2. Verify the identity id resolves correctly: `GET /tmds/idcheck/{id}` (expects ManagedIdentity/DirectoryObject).
3. Use a user AAD token when calling POST; app/MI tokens are rejected for upserts.
4. Provide the required headers (notably `apiPath`). For POST you may also provide `apiPath` in the JSON body (policy reads header first, then body).

## Request Parameters

### Headers

- `Authorization` (required): Bearer token
- `apiPath`: Required for GET/POST requests (DELETE reads this value from the JSON body)

### GET /tmds/managemsi

Lists caller-owned managed identity grants for `apiPath`.

- Request Body: None

Response

- 200 OK: Array of identity objects owned by the caller
- 400 Bad Request: Missing required header(s)
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Caller does not have access to the `apiPath`
- 404 Not Found: `apiPath` not found
- 500/502: Internal/Upstream error

Response Body (200)

```json
[
  {
    "id": "00000000-0000-0000-0000-000000000000",
    "owner": ["alias@microsoft.com","other@microsoft.com"],
    "name": "Contoso MI",
    "startDate": "2025-01-01",
    "endDate": "2025-12-31"
  }
]
```

### POST /tmds/managemsi

Upserts one or more owner grants for the specified Managed Identity (objectId) under the target `apiPath`.

- Headers:
  - `apiPath` (required); alternatively, `apiPath` can be provided in the JSON body
- Request Body (application/json):

Minimal (single owner implicitly the caller if `owner` omitted):
```json
{
  "apiPath": "msrai4s/shared/openai",
  "objectId": "11111111-1111-1111-1111-111111111111"
}
```

Explicit single owner:
```json
{
  "apiPath": "msrai4s/shared/openai",
  "objectId": "11111111-1111-1111-1111-111111111111",
  "owner": "alice@microsoft.com"
}
```

Multiple owners (JSON array):
```json
{
  "apiPath": "msrai4s/shared/openai",
  "objectId": "11111111-1111-1111-1111-111111111111",
  "owner": ["alice@microsoft.com","bob@microsoft.com"],
  "name": "Contoso MI"
}
```

Multiple owners (CSV string):
```json
{
  "apiPath": "msrai4s/shared/openai",
  "objectId": "11111111-1111-1111-1111-111111111111",
  "owner": "alice@microsoft.com,bob@microsoft.com"
}
```

Stringified JSON array (also accepted):
```json
{
  "apiPath": "msrai4s/shared/openai",
  "objectId": "11111111-1111-1111-1111-111111111111",
  "owner": "[\"alice@microsoft.com\",\"bob@microsoft.com\"]"
}
```

Body Parameters

- `objectId` (required): Managed Identity objectId or clientId resolvable via idcheck
- `owner` (optional, multi-format): Single string, CSV, JSON array, or stringified JSON array. Caller is auto-added if missing.
- `name` (optional): Friendly name (applied/updated per owner entry)
- `startDate` (optional): ISO 8601; normalized to yyyy-MM-dd
- `endDate` (optional): ISO 8601; normalized to yyyy-MM-dd; defaults to today + 360 days if omitted

Behavior Notes
- A single identity record per `objectId` aggregates all owners in an `owner` array (legacy multiple single-owner rows are consolidated on update).
- Re-upserting adds new owners and updates shared fields (name/dates) without removing existing owners unless explicitly deleted.
- Duplicate / whitespace / casing differences are de-duplicated case-insensitively; original casing of first occurrence is preserved.

Response

- 200 OK: Updated list of caller-owned identities for the API
- 400 Bad Request: Missing `objectId`; caller is not a User; invalid object type (not ManagedIdentity/DirectoryObject)
- 401 Unauthorized: Invalid or expired token
- 403 Forbidden: Caller does not have access to the `apiPath`
- 404 Not Found: `apiPath` not found or ADMINCI document missing
- 501 Not Implemented: GCR APIs do not support Managed Identities
- 500/502: Internal/Upstream error

### DELETE /tmds/managemsi

DELETE now supports distinct behaviors depending on which fields are provided.

#### Delete an entire identity (objectId only)

- Body:

  ```json
  {
    "apiPath": "msrai4s/shared/openai",
    "objectId": "11111111-1111-1111-1111-111111111111"
  }
  ```

- Result: the identity whose `id` matches `objectId` is removed completely (whether legacy single-owner or aggregated array).
  - 200 with remaining caller-owned entries if deleted
  - 204 if the identity was not found (idempotent)

#### Remove specific owner(s) from an identity (objectId + owner)

- Body (any accepted multi-owner format). Examples:

  ```json
  {
    "apiPath": "msrai4s/shared/openai",
    "objectId": "11111111-1111-1111-1111-111111111111",
    "owner": ["alice@microsoft.com","bob@microsoft.com"]
  }
  ```

  ```json
  {
    "apiPath": "msrai4s/shared/openai",
    "objectId": "11111111-1111-1111-1111-111111111111",
    "owner": "alice@microsoft.com,bob@microsoft.com"
  }
  ```

- Behavior: All listed owners are removed from the identity’s `owner` array case-insensitively. The authenticated caller is never removed (caller aliases are ignored even if supplied). Empty `owner` lists cause the identity to be deleted after removals.
- Returns:
  - 200 with caller-owned entries if at least one removal occurred
  - 204 if no matching removable owners were found

#### Legacy owner removal without `objectId`

- Body: include the API path plus the `owner` values as above.
- Behavior: Removes the supplied owners (except the caller) wherever they appear within the API’s identities. This path is maintained for backward compatibility, but new callers should prefer supplying `objectId` to scope the change to a single identity.

Owner Field Formats (same as POST; always returned as an array in GET/POST/DELETE responses even if only one owner)

- Single string
- CSV string
- JSON array
- Stringified JSON array

Response Codes

- 200 OK: Remaining caller-owned identities for the API (each identity shows a consolidated owner array)
- 204 No Content: Nothing removed (DELETE) or no matching removable owner
- 400 Bad Request: Missing required `apiPath` or (when targeting a specific identity) `objectId`
- 401 Unauthorized: Missing/invalid Authorization header
- 403 Forbidden: Caller lacks access to `apiPath`
- 404 Not Found: `apiPath` not found
- 500/502: Internal/Upstream error

## Example Requests

### GET

```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/managemsi \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -H "apiPath: msrai4s/shared/openai"
```

### POST (upsert)

```bash
curl -X POST \
  https://trapi.research.microsoft.com/tmds/managemsi \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -H "Content-Type: application/json" \
  -d '{
    "apiPath": "msrai4s/shared/openai",
    "objectId": "11111111-1111-1111-1111-111111111111",
    "name": "Contoso MI",
    "startDate": "2025-01-01",
    "endDate": "2025-12-31"
  }'
```

### DELETE

```bash
curl -X DELETE \
  https://trapi.research.microsoft.com/tmds/managemsi \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -H "Content-Type: application/json" \
  -d '{
    "apiPath": "msrai4s/shared/openai",
    "objectId": "11111111-1111-1111-1111-111111111111"
  }'
```

## Service Flow

::: mermaid
sequenceDiagram
participant Client
participant APIM
participant TMDS
participant Cosmos as CosmosDB

Client->>APIM: GET/POST/DELETE /tmds/managemsi (apiPath header for GET/POST, body for DELETE)
APIM->>APIM: Validate AAD token (audience {{oauth-appid}})
APIM->>TMDS: GET /tmds/deployments (resolve apiId for apiPath)
alt deployments not found
    APIM-->>Client: 404 API not found
else
    APIM->>TMDS: GET /tmds/testaccess (OID, ApiId)
    alt no access
        APIM-->>Client: 403 Forbidden
    else
        APIM->>Cosmos: Query ADMINCI by apiPath
        alt GET
            APIM->>APIM: Filter identities where owner==caller
            APIM-->>Client: 200 [identities...]
        else POST
            APIM->>TMDS: GET /tmds/idcheck/{callerOid} (must be User)
            APIM->>TMDS: GET /tmds/idcheck/{objectId} (must be ManagedIdentity/DirectoryObject)
            APIM->>APIM: Normalize dates (default endDate = today+360d)
            APIM->>Cosmos: Upsert identity in ADMINCI.security.identities
            APIM-->>Client: 200 [caller-owned identities]
        else DELETE
            APIM->>APIM: Remove identity matching {id, owner}
            alt not found
                APIM-->>Client: 204 No Content (idempotent)
            else
                APIM->>Cosmos: Persist updated ADMINCI
                APIM-->>Client: 200 [caller-owned identities]
            end
        end
    end
end
:::

## Updates in Managed Identity Policy

- POST rejects GCR APIs with 501 Not Implemented.
- POST only allows human Users to upsert; ManagedIdentity/service principal tokens are rejected.
- Dates are normalized to yyyy-MM-dd; `endDate` defaults to 360 days from now if not provided.
- DELETE is idempotent: missing identity returns 204 No Content.
- All operations use Cosmos DB with APIM Managed Identity for reads/writes.
- Owner is derived from `preferred_username`, falling back to `upn`.
- Responses always present `owner` as an array (legacy single string persisted values are upgraded on next write).
- Note: DELETE now reads `apiPath`, `objectId`, and `owner` values from the JSON body (headers are ignored for these inputs).
