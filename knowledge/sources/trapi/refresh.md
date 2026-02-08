# Cache Refresh Endpoint

## Overview

-`POST /tmds/refresh` refreshes one or more cached runtime artifacts for a specific API identified by its `apiPath`, and also handles global property caches. It supports:

- Full reload (default – all sections)
- Selective reload (explicit list of section tokens)


**apiPath is only required if any API-specific section (`backends`, `groups`, `identities`) is requested, or for a full reload.**
If only global sections (`rateLimits`, `accountModelLimits`) are being refreshed, `apiPath` is optional and may be omitted.

It is typically invoked after drift is detected via `/tmds/testconfig` (which may now include global sections).

Refreshable sections (tokens):

| Token | Scope | Description | Underlying Cache Key(s) | Source |
|-------|-------|-------------|-------------------------|--------|
| `backends` | API | Backend routing / selection configuration | `TRAPIconfig-{apiId}` (+ transient `Blockconfig-{apiId}`) | Cosmos sproc: `spGetBackends` |
| `groups` | API | Allowed AAD security groups | `TRAPIgroups-{apiId}` | Cosmos sproc: `spGetAllowedGroups` |
| `identities` | API | Allowed managed identities (objectIds) | `TRAPImanagedIdentities-{apiId}` | Cosmos sproc: `spGetAllowedGroups` |
| `rateLimits` / `globalRateLimits` | Global | Global rate limit definition payload | `globalRateLimits` | Cosmos sproc: `spGetRateLimits` |
| `accountModelLimits` | Global | Per account+deployment model rate limit entries | `accountModelLimits` | Cosmos sproc: `getDeploymentRateLimits` |


Notes:

- `groups` and `identities` share a single Cosmos stored procedure call; if only one is requested the call still occurs but only the requested cache(s) are stored.
- Global sections each invoke their respective stored procedure.
- Section requests are case-insensitive.
- Non-requested sections in selective mode are reported with status `skipped`.


## Endpoint


```
POST /tmds/refresh
Content-Type: application/json
Authorization: Bearer <AAD JWT>
```


## Request Body


```json
{
  "apiPath": "gcr/shared/openai",
  "reloadSections": ["backends","groups"]
}
```


### Properties


| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `apiPath` | string | Conditional | Required if any API-specific section (`backends`, `groups`, `identities`) is requested; optional if only global sections (`rateLimits`, `accountModelLimits`) are being refreshed. |
| `reloadSections` | array<string> or string | No | Omit or empty => full reload. If supplied restricts reload to listed section tokens. |



### `reloadSections` Accepted Forms


1. Array form:

  ```json
  "reloadSections": ["backends","groups","identities"]
  ```

2. Delimited string (commas or semicolons):

  ```json
  "reloadSections": "backends, groups; rateLimits"
  ```

3. Mixed whitespace and casing tolerated:

  ```
  "reloadSections": "  BackEnds ; GROUPS "
  ```

4. The token `globalRateLimits` is accepted as an alias for `rateLimits` (case-insensitive).



If `reloadSections` is:

- Missing or parses to zero valid tokens ⇒ Full reload (`reloadMode: "full"`).
- Present with ≥1 valid token ⇒ Selective reload (`reloadMode: "selective"`).

Invalid tokens are ignored (not an error) and effectively reduce the requested list. If after filtering none remain, behavior falls back to full reload.


## Behavior Summary


| Mode | Determination | Sections Acted On | Non-acted Sections | apiPath Requirement |
|------|---------------|-------------------|--------------------|---------------------|
| Full | `reloadSections` absent/empty | All (API + global) | N/A | **Required** |
| Selective | ≥1 valid token provided | Only requested | Reported as `skipped` | **Required if any API section (`backends`, `groups`, `identities`) is requested; optional if only global sections** |


## Status Semantics
Per cache operation:
- `success` – Reloaded and stored successfully.
- `failed` / `failed-<code>` – Reload attempted but failed (optionally suffixed with HTTP status).
- `failed-exception` – Unhandled processing error.
- `skipped` – Not requested in selective mode.

Aggregate:
- `overallStatus: "success"` – All *non-skipped* operations returned `success`.
- `overallStatus: "partial"` – At least one *non-skipped* operation failed.


## Response Structure


```json
{
  "apiPath": "gcr/shared/openai",
  "apiId": "670528256820ca7d1ddc6857",
  "timestamp": "2025-09-04T11:22:33.456Z",
  "overallStatus": "success",
  "reloadMode": "selective",
  "cacheOperations": [
    { "cache": "TRAPIconfig", "key": "TRAPIconfig-670528256820ca7d1ddc6857", "status": "success" },
    { "cache": "TRAPIgroups", "key": "TRAPIgroups-670528256820ca7d1ddc6857", "status": "success" },
    { "cache": "TRAPImanagedIdentities", "key": "TRAPImanagedIdentities-670528256820ca7d1ddc6857", "status": "skipped" },
    { "cache": "globalRateLimits", "key": "globalRateLimits", "status": "skipped" },
    { "cache": "accountModelLimits", "key": "accountModelLimits", "status": "skipped" }
  ]
}
```

For global-only refreshes, `apiId` and API-specific cache keys will be `null`.



### Field Notes

| Field | Description |
|-------|-------------|
| `apiId` | Resolved by calling `/tmds/deployments` and matching `apiPath`. Will be `null` for global-only refreshes. |
| `reloadMode` | `full` or `selective` based on logic above. |
| `cacheOperations` | Ordered list: config, groups, identities, rateLimits, accountModelLimits. API-specific keys will be `null` for global-only refreshes. |
| `overallStatus` | See Status Semantics. |


## Example Scenarios

### 1. Full Reload (no reloadSections)
Request:
```bash
curl -X POST https://trapi.research.microsoft.com/tmds/refresh \
 -H "Authorization: Bearer <token>" \
 -H "Content-Type: application/json" \
 -d '{"apiPath":"gcr/shared/openai"}'
```
Effect: All five sections refreshed (includes global caches).

### 2. Selective Reload (Array)
```json
{
  "apiPath": "gcr/shared/openai",
  "reloadSections": ["groups","identities"]
}
```
Effect: Shared security sproc invoked once; only groups & identities caches updated; others skipped.

### 3. Selective Reload (String)
```json
{
  "apiPath": "gcr/shared/openai",
  "reloadSections": "backends;rateLimits;accountModelLimits"
}
```

### 4. Invalid Tokens Are Ignored
```json
{
  "apiPath": "gcr/shared/openai",
  "reloadSections": ["backends","foo","bar"]
}
```
`foo`, `bar` ignored ⇒ treated as selective with `["backends"]`.

### 5. All Invalid ⇒ Fallback to Full
```json
{
  "apiPath": "gcr/shared/openai",
  "reloadSections": "foo,bar"
}
```
Parses to zero valid ⇒ full reload.

## Integration with /tmds/testconfig
`/tmds/testconfig` (with header `x-testconfig-includeDiff: true`) returns:
- `inSync`
- `driftSections`: e.g. `["backends","groups","globalRateLimits","accountModelLimits"]`

Mapping to refresh tokens:
| testconfig token | refresh token |
|------------------|--------------|
| `globalRateLimits` | `rateLimits` |
| `accountModelLimits` | `accountModelLimits` |

Example selective API + global refresh:
```json
{
  "apiPath": "gcr/shared/openai",
  "reloadSections": ["backends","rateLimits"]
}
```

If you desire a conservative reload strategy:
1. Call `/tmds/testconfig` (diff enabled).
2. If `inSync == false` and `driftSections` non-empty, invoke `/tmds/refresh` with just those sections.
3. Re-run `/tmds/testconfig` to confirm convergence.

## Operational Flow (Selective Example)

::: mermaid
sequenceDiagram
    Client->>APIM: POST /tmds/refresh (apiPath, reloadSections=["groups"])
    APIM->>Deployments: GET /tmds/deployments
    Deployments-->>APIM: Deployment list
    APIM->>Cosmos: POST spGetAllowedGroups
    Cosmos-->>APIM: Groups + Managed Identities
    APIM->>Cache: Remove TRAPIgroups-{apiId}
    APIM->>Cache: Store TRAPIgroups-{apiId}
    APIM-->>Client: JSON result (groups=success, identities=skipped)
:::


## Error Responses



| HTTP | JSON Example | Cause |
|------|--------------|-------|
| 400 | `{"error":"apiPath is required for requested sections", "status":400}` | `apiPath` missing when required for non-global or full reload. |
| 401 | `{"error":"TRAPI: Unauthorized. Invalid or expired token."}` | Token invalid/expired. |
| 404 | `{"error":"No API found with the specified apiPath","status":404}` | `apiPath` not in deployments list. |
| 500 | `{"error":"Internal server error during cache refresh","status":500}` | Unhandled error branch. |


## Idempotency and Concurrency

- Multiple concurrent refreshes for same `apiPath` overwrite the same keys; last writer wins.
- Safety: Each selective operation only touches requested keys (except shared security sproc call).

## Performance Considerations

- Prefer selective reload to reduce Cosmos RU consumption.
- Combine `groups` + `identities` when both are known out-of-date to avoid redundant calls later.
- Only include global sections when drift detected to keep global RU impact low.

## Suggested Enhancements (Future)

| Enhancement | Benefit |
|-------------|---------|
| Include RU charge metadata | Observability & cost insights |
| Add per-section duration ms | Performance troubleshooting |
| Accept `force=true` flag to bypass skip semantics | Emergency revalidation |
| Expose hash fingerprints in `/testconfig` | O(1) drift detection client-side |
| Introduce `dryRun` mode | Preview reload impact without mutation |
| Accept global-only refresh (no apiPath) | Operational convenience |

## Quick Reference



| Goal | Recommended Action | apiPath Required? |
|------|--------------------|------------------|
| Full reset after config migration | Omit `reloadSections` | Yes |
| Refresh only drifted items | Use `driftSections` from `/testconfig` (map globals) | Yes if any API section, No if only global |
| Refresh backends + rate limits | `"reloadSections": "backends;rateLimits"` | Yes |
| Refresh account model limits only | `"reloadSections": "accountModelLimits"` | No |
| Refresh all global caches | `"reloadSections": "rateLimits,accountModelLimits"` | No |
| Validate remediation | Invoke `/tmds/testconfig` post-refresh | N/A |


## Minimal Client Pseudocode

```csharp
// 1. Detect drift
var comparison = GET /tmds/testconfig (x-testconfig-includeDiff=true)
if (!comparison.inSync) {
  var drift = comparison.driftSections; // e.g. ["backends","globalRateLimits"]
  // 2. Selective refresh (map globalRateLimits -> rateLimits)
  var mapped = drift.Select(d => d == "globalRateLimits" ? "rateLimits" : d).ToArray();
  POST /tmds/refresh { apiPath, reloadSections: mapped }
  // 3. Re-check
  var final = GET /tmds/testconfig
}
```

## Security

- Requires same AAD authorization model as other TMDS administrative endpoints.
- Authorization enforced before any Cosmos or cache operations.

## Summary

Use `/tmds/refresh` to efficiently reconcile runtime caches with authoritative configuration, integrating tightly with `/tmds/testconfig` for targeted remediation while minimizing unnecessary reloads.
