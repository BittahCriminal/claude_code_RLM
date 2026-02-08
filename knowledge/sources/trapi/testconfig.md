
# TMDS Test Configuration Inspection (Enhanced)

## Overview

`GET /tmds/testconfig` provides a diagnostic view comparing the **configured** state (Cosmos DB stored procedures) with the **running** state (APIM in-memory cache) for either:

1. A specific API path (traditional mode), and/or
2. One or more supported **global properties** (see below)


### Supported Global Properties

- `globalRateLimits` (Cosmos sproc: `spGetRateLimits` / cache key: `globalRateLimits`)
- `accountModelLimits` (Cosmos sproc: `getDeploymentRateLimits` / cache key: `accountModelLimits`)


The endpoint inspects (API scope):

- Backends (`spGetBackends`)
- Security Groups (`spGetAllowedGroups` → `securityGroups`)
- Managed Identities (`spGetAllowedGroups` → `managedIdentities`)

And (Global scope when requested):

- Global Rate Limits definition
- Account/Deployment Model Limits list

It returns a structured JSON document; it does **not** mutate cache or configuration. Optional diff output can highlight drift between configured and running values for both API and global sections. You can now invoke the endpoint **without** `apiPath` if you only want global property inspection.

## Key Enhancements (2025-09)

- **Flexible Header Parsing:**
  - `globalProperty` header now supports single value, CSV, or JSON array string.
  - Both `apiPath` and/or `globalProperty` can be supplied; at least one is required.
- **Global Property Logic:**
  - Unknown global property names are reported in the response and cause `inSync = false`.
  - If `apiPath` is invalid but valid globals are present, returns 200 with `apiPathStatus=notFoundIgnored` and skips the API section.
  - If `apiPath` is invalid and only unknown globals are present, returns 404.
- **Diff and Drift:**
  - Diff logic (`x-testconfig-includeDiff: true`) now applies to both API and global properties.
  - Drift sections are reported for both API and global mismatches.
- **inSync Logic:**
  - `inSync` is true only if all requested known sections match and are available, and no unknown globals are present.
- **Error Handling:**
  - 400 if neither `apiPath` nor any (known or unknown) `globalProperty` supplied.
  - 404 if `apiPath` not found and no valid known global properties.


## Endpoint

`GET /tmds/testconfig`

## Authentication

Requires an Azure AD OAuth2 token accepted by the standard TMDS security fragment (`trapi-sec-oauth-cosmos`). Access is limited to approved security groups or managed identities (currently includes the TRAPI admin/debug group and automation MI as configured in the policy).

## Access Restrictions

- Caller must be in `allowedGroups` or `allowedIdentities` as enforced by the shared security fragment.
- The `apiPath` supplied must resolve to a deployed API (looked up via internal call to `/tmds/deployments`).
- No write operations occur; this is read-only diagnostics.

### For Developers

Use this endpoint when validating deployment drift or investigating access issues.

1. Determine the apiPath (e.g. via `GET /tmds/deployments`).
2. Call `GET /tmds/testconfig` with `apiPath` header.
3. (Optional) Add header `x-testconfig-includeDiff: true` to include per-section added/removed details and drift sections.
4. Validate `inSync` flag. If `false`, review `comparison` node (when diff enabled) or manually compare `configuredSettings` vs `runningSettings`.


## Request Parameters

### Headers

| Header | Required? | Notes |
|--------|-----------|-------|
| `apiPath` | Conditional | Required if no valid `globalProperty` values are supplied. Trimmed of leading/trailing slashes. |
| `globalProperty` | Conditional | Accepts single value, CSV, or JSON array string. Supported tokens: `globalRateLimits`, `accountModelLimits` (case-insensitive). Required if `apiPath` absent. Unknown tokens are reported and cause `inSync=false` but don't 404 unless *only* unknown globals AND invalid `apiPath` provided. |
| `x-testconfig-includeDiff` | Optional | `true`\|`false` (default `false`). Adds comparison blocks & `driftSections` for both API and global properties. |
| `Authorization` | Required | Bearer token. |


#### `globalProperty` Header Accepted Forms

| Form | Example |
|------|---------|
| Single token | `globalRateLimits` |
| CSV list | `globalRateLimits,accountModelLimits` |
| JSON array string | `["globalRateLimits","accountModelLimits"]` |

Unknown tokens are echoed under `globalSettings.unknown` and force `inSync=false`.


## GET /tmds/testconfig

Returns a JSON object summarizing configured vs running settings and an `inSync` flag. When `x-testconfig-includeDiff: true` is set, adds comparison statistics and lists of added/removed items for each dimension.


### Response Codes

| Code | Condition |
|------|-----------|
| 200 | Diagnostic object returned (even if `apiPath` not found but at least one known global property requested). |
| 400 | Neither `apiPath` nor any (known or unknown) `globalProperty` supplied. |
| 401 | Invalid / missing token. |
| 403 | Caller not in allowed group / identity. |
| 404 | `apiPath` not found AND no valid known global properties (only unknown globals or none). |
| 500 | Unhandled execution error. |


### Response Body (200 Basic – API + Globals Example)

 
```json
{
  "apiPath": "msrai4s/shared",
  "apiId": "tmds-msrai4s-shared-openai",
  "apiPathStatus": "ok",
  "timestamp": "2025-09-04T12:34:56.789Z",
  "configuredSettings": {
    "status": "ok",
    "backends": ["backendA"],
    "groups": ["11111111-1111-1111-1111-111111111111"],
    "identities": ["22222222-2222-2222-2222-222222222222"]
  },
  "runningSettings": {
    "status": "ok",
    "backends": ["backendA"],
    "groups": ["11111111-1111-1111-1111-111111111111"],
    "identities": ["22222222-2222-2222-2222-222222222222"]
  },
  "globalSettings": {
    "requested": ["globalRateLimits","accountModelLimits"],
    "unknown": [],
    "properties": {
      "globalRateLimits": {
        "status": "ok",
        "match": true,
        "configured": {"defaultPerMinute":100},
        "running": {"defaultPerMinute":100}
      },
      "accountModelLimits": {
        "status": "ok",
        "match": true,
        "configured": [ {"account":"acc1","deploymentName":"depA","rpm":50} ],
        "running":   [ {"account":"acc1","deploymentName":"depA","rpm":50} ]
      }
    }
  },
  "inSync": true
}
```

### Response Body (200 With Diff – Global + API Drift)

 
```json
{
  "apiPath": "msrai4s/shared/openai",
  "apiId": "tmds-msrai4s-shared-openai",
  "apiPathStatus": "ok",
  "timestamp": "2025-09-04T12:34:56.789Z",
  "configuredSettings": { "status":"ok", "backends":["backendA"], "groups":[], "identities":[] },
  "runningSettings": { "status":"ok", "backends":["backendA","backendB"], "groups":[], "identities":[] },
  "globalSettings": {
    "requested": ["globalRateLimits"],
    "unknown": [],
    "properties": {
      "globalRateLimits": {
        "status": "mismatch",
        "match": false,
        "configured": { "defaultPerMinute": 100 },
        "running": { "defaultPerMinute": 120 }
      }
    },
    "comparison": {
      "globalRateLimits": {
        "match": false,
        "configuredCount": 1,
        "runningCount": 1,
        "added": [],
        "removed": [],
        "changed": [ { "key": "defaultPerMinute", "configured": 100, "running": 120 } ]
      }
    }
  },
  "comparison": {
    "backends": { "match": false, "configuredCount": 1, "runningCount": 2, "added": ["backendB"], "removed": [] },
    "groups": { "match": true,  "configuredCount": 0, "runningCount": 0, "added": [], "removed": [] },
    "identities": { "match": true, "configuredCount": 0, "runningCount": 0, "added": [], "removed": [] }
  },
  "driftSections": ["backends","globalRateLimits"],
  "inSync": false
}
```

### Error Response Examples

Missing both `apiPath` and `globalProperty`:
 
```json
{ "error": "apiPath or globalProperty header required", "status": 400 }
```

Invalid `apiPath` and only unknown globals provided:
```json
{ "error": "No API found with specified apiPath", "status": 404 }
```

## Example

### Basic (API + Global)

 
```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/testconfig \
  -H "Authorization: Bearer <token>" \
  -H "apiPath: msrai4s/shared/openai" \
  -H "globalProperty: globalRateLimits,accountModelLimits"
```

### Global Only (No apiPath)

 
```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/testconfig \
  -H "Authorization: Bearer <token>" \
  -H 'globalProperty: ["globalRateLimits","accountModelLimits"]'
```

### With Diff (API + Global)

 
```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/testconfig \
  -H "Authorization: Bearer <token>" \
  -H "apiPath: msrai4s/shared/openai" \
  -H "globalProperty: globalRateLimits" \
  -H "x-testconfig-includeDiff: true"
```

### Unknown Global Token Influence

 
```bash
curl -X GET \
  https://trapi.research.microsoft.com/tmds/testconfig \
  -H "Authorization: Bearer <token>" \
  -H "globalProperty: globalRateLimits,fooBar" \
  -H "x-testconfig-includeDiff: true"
```
Result: `fooBar` appears in `globalSettings.unknown`; `inSync=false` even if everything else matches.

## Service Flow

::: mermaid
sequenceDiagram
    participant Client
    participant APIM
    participant TMDS as TMDS (Deployments)
    participant Cache as APIM Cache
    participant Cosmos as CosmosDB (Stored Procs)

    Client->>APIM: GET /tmds/testconfig (apiPath, optional diff header)
    APIM->>APIM: Validate AAD token (security fragment)
    APIM->>TMDS: GET /tmds/deployments
    alt apiPath not found
        APIM-->>Client: 404 Not Found
    else apiPath resolved
        APIM->>Cache: lookup TRAPIconfig-{apiId}
        APIM->>Cache: lookup TRAPIgroups-{apiId}
        APIM->>Cache: lookup TRAPImanagedIdentities-{apiId}
        APIM->>Cosmos: POST spGetBackends
        APIM->>Cosmos: POST spGetAllowedGroups
        APIM->>APIM: Parse & normalize arrays
        APIM->>APIM: Compute status & inSync
        alt diff requested
            APIM->>APIM: Build comparison & driftSections
        end
        APIM-->>Client: 200 Diagnostic JSON
    end
::: 

## Drift & Sync Logic


### API Section

| Field | Meaning |
|-------|---------|
| `configuredStatus` | `ok` both sproc calls 200; `partial` one succeeded; `unavailable` none succeeded. |
| `runningStatus` | `ok` if any cached dimension non-empty; `empty` otherwise. |

API arrays are compared as case-insensitive sets (order-independent) when included.


### Global Properties Section

Each requested known property gets a `status`:

| Status | Meaning |
|--------|---------|
| `ok` | Configured fetch succeeded & matches running cache. |
| `missingRunning` | Configured data available; cache empty. |
| `mismatch` | Both available but differ. |
| `unavailable` | Configured sproc call failed / no data. |

Diff (when enabled):

| Property | Diff Style |
|----------|-----------|
| `globalRateLimits` | Top-level object key set comparison (`added`, `removed`, `changed`). |
| `accountModelLimits` | Identity = `account|deploymentName`; lists of `added`, `removed`, `changed` identities. |


### inSync Evaluation
`inSync` is `true` only if:
1. If API requested & resolved: API structural status is healthy (`configuredStatus == ok` and running empty only when configured empty) AND all three API arrays match.
2. All requested known global properties have `status == ok`.
3. No unknown global tokens were requested.

Any violation sets `inSync=false`.

### Additional Notes
- If both `apiPath` and all `globalProperty` values are missing, returns 400.
- If `apiPath` is invalid and only unknown globals are present, returns 404.
- If `apiPath` is invalid but at least one valid global property is present, returns 200 with `apiPathStatus=notFoundIgnored` and skips the API section.

### Future Enhancements
- Unknown global tokens intentionally downgrade sync to surface client typos early.
- Potential future additions: hash comparison, summary mismatch score, selective global property filtering in refresh pipeline, pagination for large accountModelLimits arrays.
- Designed for ops troubleshooting; can be used in health dashboards.
- All Cosmos calls use APIM Managed Identity with AAD token (`type=aad&ver=1.0&sig=...`).

## Notes & Future Enhancements

- Unknown global tokens intentionally downgrade sync to surface client typos early.
- Potential future additions: hash comparison, summary mismatch score, selective global property filtering in refresh pipeline, pagination for large accountModelLimits arrays.
- Designed for ops troubleshooting; can be used in health dashboards.
- All Cosmos calls use APIM Managed Identity with AAD token (`type=aad&ver=1.0&sig=...`).

## Changelog

- 2025-09: Added global property inspection (`globalRateLimits`, `accountModelLimits`), optional multi-mode invocation, extended diff & inSync semantics.
- 2025-09: Original API-only comparison + optional diff.
