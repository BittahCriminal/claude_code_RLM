# Hybrid K8s Namespace Automation Architecture

## Purpose
Provide a secure, auditable, and automated workflow for creating and reallocating Kubernetes namespaces in on-prem clusters, governed by Azure Entra ID groups and PIM, and exposed via an API suitable for PowerApps integration.

## Scope
- On-prem Kubernetes clusters host workloads.
- Azure hosts the control plane services, identity, and audit signals.
- Two admin groups:
  - Cluster Admins: global authority across clusters; can allocate CPU/memory/storage with storage only increasing.
  - Lab Admins: scoped to their assigned namespaces; can update quotas within those namespaces, storage only increasing.

## High-Level Architecture
- PowerApps UI submits requests to a single Azure API endpoint.
- Azure API validates identity (Entra ID) and triggers an orchestration service.
- Orchestrator applies GitOps changes or submits a NamespaceRequest CRD to the clusters.
- Admission policies enforce quota rules and group ownership.
- Kubernetes RBAC maps Entra ID groups to Roles/ClusterRoles.
- Centralized audit and observability in Azure.

## Components
1. PowerApps
   - UI for namespace create/resize/transfer requests.
   - Uses Azure API Management endpoint.

2. Azure API Management (APIM)
   - Front door for API; enforces rate limiting and authn.
   - Validates JWT from Entra ID.

3. Namespace Automation API (Azure App Service or AKS)
   - REST API used by PowerApps.
   - Performs request validation and authorization checks.
   - Writes intent to Git (preferred) or posts CRDs to clusters.

4. Orchestrator/Controller
   Option A: GitOps (Recommended)
   - API writes a commit to a Git repo (namespace-as-code).
   - Argo CD/Flux deploys Namespace resources to clusters.
   - Policy engines validate and enforce rules at admission.

   Option B: NamespaceRequest CRD
   - API posts a NamespaceRequest to a management cluster.
   - Controller reconciles and applies to target clusters.

5. Policy Enforcement (Gatekeeper or Kyverno)
   - Storage can only increase (deny decreases to requests.storage).
   - Lab Admins can only modify namespaces labeled owner=<lab>.
   - Quota bounds for each namespace and optional lab-level caps.

6. RBAC Integration
   - Entra ID groups mapped to Kubernetes RBAC via OIDC.
   - Cluster Admins group: ClusterRoleBinding to elevated ClusterRole.
   - Lab Admins group: RoleBinding to namespace-scoped custom Role.
   - PIM used for just-in-time elevation.

7. Connectivity
   - Secure private connectivity from Azure to on-prem clusters.
   - ExpressRoute preferred; VPN acceptable with strict allowlisting.

8. Observability and Audit
   - Kubernetes audit logs forwarded to Log Analytics/Sentinel.
   - Entra ID sign-ins and PIM activations logged and correlated.
   - API request logs retained for compliance.

## Request Flow
1. User requests namespace create/update from PowerApps.
2. PowerApps calls APIM with Entra ID token.
3. API validates token, checks group membership, and enforces business rules.
4. API writes desired state to Git or creates NamespaceRequest CRD.
5. GitOps/controller applies namespace objects and quota changes.
6. Admission policy validates storage-only-increase and ownership rules.
7. Audit logs captured and correlated in Azure.

## RBAC Model
Cluster Admins:
- ClusterRole: create/update/delete namespaces, resource quotas, limit ranges, network policies.
- PIM: activation required, MFA, approval, limited duration.

Lab Admins:
- Role: get/list/update namespace, resource quotas, limit ranges within owned namespaces.
- No cluster-scoped permissions.

Namespace Ownership:
- Namespace labels: owner=<lab-group>, environment=<env>.
- Policies restrict lab admins to owner-matching namespaces.

## Policy Examples (Conceptual)
- Deny any update to ResourceQuota if requests.storage decreases.
- Deny RoleBinding/Role changes not created by the automation service.
- Require owner label on namespace create.

## Best Automation Approach
1. GitOps first:
   - Single source of truth; easy audit and rollback.
   - PowerApps/API creates a PR or commit with namespace definition.
   - Argo CD/Flux enforces desired state to clusters.

2. Policy-first enforcement:
   - All writes go through admission policy so rules cannot be bypassed.

3. API as the only mutation path:
   - Disallow direct kubectl except for break-glass.
   - PIM for all privileged operations.

4. Separate environments:
   - Dev/Test/Prod clusters with separate Git paths and RBAC.

## API Surface (for PowerApps)
- POST /namespaces
  - Body: name, ownerGroup, clusterId, quotas (cpu/memory/storage)
- PATCH /namespaces/{name}/quotas
  - Body: updated quotas (storage increases only)
- GET /namespaces?ownerGroup=&clusterId=

## Security Considerations
- Entra ID group claims must be present in tokens; use group IDs.
- API validates ownership; no client-side trust.
- Service uses managed identity to access Git or cluster API.

## Rollout Plan
1. Pilot in one cluster and one lab group.
2. Add policy enforcement, then lock down direct cluster access.
3. Expand to all clusters and integrate with PowerApps.

## Open Decisions
- GitOps tool choice (Argo CD vs Flux).
- Policy engine choice (Gatekeeper vs Kyverno).
- Management cluster vs direct target cluster reconciliation.
