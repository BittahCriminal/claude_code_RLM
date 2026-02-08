# Backstage Knowledge Base
## Platform Engineering Developer Portal Framework

**Source**: [backstage/backstage](https://github.com/backstage/backstage) (GitHub)
**License**: Apache-2.0
**Status**: CNCF Incubation project (graduated from Sandbox March 2022)
**Created by**: Spotify
**Latest stable**: Check [releases](https://github.com/backstage/backstage/releases)

---

## 1. What is Backstage?

Backstage is an **open source framework for building developer portals**. It provides a centralized software catalog that restores order to microservices and infrastructure, enabling product teams to ship high-quality code quickly without compromising autonomy.

### Core Value Propositions
- **Engineering Managers**: Maintain standards/best practices across the org, manage tech ecosystem
- **Developers**: Fast standardized component creation, central project/docs management
- **Platform Engineers**: Extensibility via plugins, integrate new tools/services easily
- **Everyone**: Single consistent experience tying all infrastructure tooling together

### Out-of-the-Box Features
1. **Software Catalog** - Centralized metadata for all software (services, libraries, data pipelines, ML models, etc.)
2. **Software Templates (Scaffolder)** - Quickly spin up new projects with org best practices
3. **TechDocs** - "Docs like code" approach using Markdown files alongside code
4. **Kubernetes Plugin** - Service health monitoring across clusters
5. **Search** - Customizable search across the Backstage ecosystem

---

## 2. Architecture Overview

### Three Main Layers

```
┌─────────────────────────────────────────────────┐
│                   FRONTEND                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  App     │  │ Plugins  │  │ Extensions│      │
│  │ (React)  │  │(Catalog, │  │(Overrides,│      │
│  │          │  │Templates,│  │ Routes,   │      │
│  │          │  │TechDocs) │  │ APIs)     │      │
│  └──────────┘  └──────────┘  └──────────┘      │
├─────────────────────────────────────────────────┤
│                   BACKEND                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Backend  │  │ Plugins  │  │ Services  │      │
│  │Instance  │  │(separate │  │(logging,  │      │
│  │          │  │ micro-   │  │ DB, auth, │      │
│  │          │  │ services)│  │ config)   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
├─────────────────────────────────────────────────┤
│               DATABASE (PostgreSQL)              │
│  Separate logical DB per plugin via Knex         │
└─────────────────────────────────────────────────┘
```

### Three Component Types
1. **Core** - Base functionality from open-source project
2. **App** - Deployed instance, customized by org's productivity team
3. **Plugins** - Additional functionalities (company-specific or open-source)

### Frontend Building Blocks
- **App**: Root of frontend application, wires things together
- **Extensions**: Visual and non-visual building blocks forming an "app extension tree"
- **Frontend Plugins**: Feature providers (Catalog, Templates, TechDocs, K8s, Search)
- **Extension Overrides**: High-priority extensions that replace existing ones
- **Utility APIs**: TypeScript interfaces for shared functionality between plugins
- **Routes**: Indirection layer for inter-plugin routing without explicit URL knowledge

### Backend Building Blocks
- **Backend Instance**: Unit of deployment (can split into multiple for scaling)
- **Backend Plugins**: Independent microservices communicating only over the wire
- **Services**: Utilities (logging, DB, config) - also customization points
- **Extension Points**: Encoded patterns for plugin extension (e.g., entity providers for Catalog)
- **Modules**: Use Extension Points to add features to plugins (e.g., Scaffolder Actions)

### Database
- **Production**: PostgreSQL (recommended)
- **Development/Testing**: SQLite (in-memory)
- Uses **Knex** library - separate logical DB per plugin
- MySQL variants reported to work but not fully tested

### Plugin Architecture Types
1. **Standalone**: Runs entirely in browser (e.g., Tech Radar)
2. **Service Backend**: Makes API requests to org-internal services (e.g., Lighthouse)
3. **Third-party Backend**: Communicates with external SaaS via proxy (e.g., CircleCI)

---

## 3. Software Catalog

### What It Does
- Centralized system tracking ownership and metadata for ALL software in ecosystem
- Built around **metadata YAML files** stored with code, harvested and visualized in Backstage
- Available at `/catalog` in the UI

### Two Main Use Cases
1. Teams manage and maintain their own software with a uniform view
2. All software in the company becomes discoverable (no more orphan software)

### Adding Components
1. **Manual Registration**: Go to `/create` → "Register Existing Component" → provide full YAML URL
2. **Software Templates**: Auto-registered when created through Backstage templates
3. **Static Configuration**: Add to `app-config.yaml` under `catalog.locations`
4. **External Sources**: Azure DevOps Discovery, GitHub Discovery, etc.

### catalog-info.yaml Example
```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: artist-web
  description: The place to be, for great artists
  labels:
    example.com/custom: custom_label_value
  annotations:
    example.com/service-discovery: artistweb
    circleci.com/project-slug: github/example-org/artist-website
  tags:
    - java
  links:
    - url: https://admin.example-org.com
      title: Admin Dashboard
      icon: dashboard
      type: admin-dashboard
spec:
  type: website
  lifecycle: production
  owner: artist-relations-team
  system: public-websites
```

### Entity Kinds
| Kind | Description |
|------|-------------|
| **Component** | Individual pieces of software (services, websites, libraries) |
| **Template** | Software Templates for creating new components |
| **API** | Boundaries between components (REST, GraphQL, gRPC, etc.) |
| **Group** | Organizational units (teams, business units, chapters) |
| **User** | People (typically auto-populated from org systems) |
| **Resource** | Physical or virtual infrastructure (databases, S3 buckets, CDNs) |
| **System** | Collection of entities cooperating to perform a function |
| **Domain** | Relates entities and systems to part of the business |
| **Location** | Marker pointing to other catalog-info.yaml locations |

### Entity Envelope (Common Fields)
- `apiVersion`: `backstage.io/v1alpha1` (current)
- `kind`: Entity type (Component, API, etc.)
- `metadata`: Name, namespace, uid, title, description, labels, annotations, tags, links
- `spec`: Kind-specific specification data

### Naming Rules
- **name**: 1-63 chars, `[a-z0-9A-Z]` separated by `[-_.]`, required
- **namespace**: `[a-zA-Z0-9]` separated by `-`, max 63 chars, defaults to `"default"`
- **tags**: `[a-z0-9:+#]` separated by `-`, max 63 chars each

### Substitutions
- `$text`: Embed file contents as string
- `$json`: Parse and embed JSON file
- `$yaml`: Parse and embed YAML file

---

## 4. Software Templates (Scaffolder)

### Overview
- Tool to create Components inside Backstage
- Loads code skeletons, templates variables, publishes to locations (GitHub, GitLab, etc.)
- Available at `/create` in the UI

### Key Features
- Step-based wizard UI for gathering parameters
- Review page before execution
- Task list with history
- "Start Over" for re-running with pre-filled parameters
- Cancel support for running templates

### Important Notes
- **Action ID naming**: Use camelCase (NOT kebab-case) for custom action IDs
  - Dashes in IDs cause `NaN` errors in template expressions (evaluated as subtraction)
- **Node 20+**: Requires `--no-node-snapshot` flag (`NODE_OPTIONS="--no-node-snapshot"`)
- Auto-registers created components in the catalog

---

## 5. Kubernetes Plugin

- Designed for **service owners**, not cluster admins
- Shows health of services regardless of deployment location
- Elevates visibility of errors with drill-down into deployments, pods, objects
- Two plugins: `@backstage/plugin-kubernetes` (frontend) + `@backstage/plugin-kubernetes-backend`

---

## 6. Plugin Development

### Creating Plugins
- Follow the [Create a Plugin](https://backstage.io/docs/plugins/create-a-plugin) guide
- Community plugins: [backstage/community-plugins](https://github.com/backstage/community-plugins)
- Plugin Directory: [backstage.io/plugins](https://backstage.io/plugins)

### Plugin Package Structure (up to 5 packages)
```
@scope/plugin-<id>           # Frontend plugin
@scope/plugin-<id>-react     # Frontend library (shared with other plugins)
@scope/plugin-<id>-backend   # Backend plugin
@scope/plugin-<id>-node      # Backend library
@scope/plugin-<id>-common    # Isomorphic (shared) library
```

### Key Rules
- Plugins can NOT directly import non-library packages from other plugins
- All inter-plugin communication through libraries and the app
- Backend plugins are independent microservices (communicate over the wire only)
- Modules extend plugins via Extension Points and must deploy with that plugin

---

## 7. Azure DevOps Integration

### Authentication Provider (Microsoft Azure)
- Uses Azure OAuth via `@backstage/plugin-auth-backend-module-microsoft-provider`
- Requires App Registration with:
  - Redirect URI: `https://your-backstage.com/api/auth/microsoft/handler/frame`
  - Delegated permissions: `email`, `offline_access`, `openid`, `profile`, `User.Read`
- Configuration:
```yaml
auth:
  providers:
    microsoft:
      development:
        clientId: ${AZURE_CLIENT_ID}
        clientSecret: ${AZURE_CLIENT_SECRET}
        tenantId: ${AZURE_TENANT_ID}
        domainHint: ${AZURE_TENANT_ID}
        signIn:
          resolvers:
            - resolver: emailMatchingUserEntityProfileEmail
```

### Resolvers Available
- `emailMatchingUserEntityProfileEmail` - Match by email
- `emailLocalPartMatchingUserEntityName` - Match local part of email to entity name
- `emailMatchingUserEntityAnnotation` - Match by `microsoft.com/email` annotation
- `userIdMatchingUserEntityAnnotation` - Match by `graph.microsoft.com/user-id` annotation

### Azure DevOps Discovery (Catalog Auto-Discovery)
- Plugin: `@backstage/plugin-catalog-backend-module-azure`
- Crawls Azure DevOps org and registers entities matching configured path
- **Requires**: Code Search feature enabled in Azure DevOps
- Configuration:
```yaml
catalog:
  providers:
    azureDevOps:
      myProvider:
        organization: myorg
        project: myproject         # supports '*' wildcard
        repository: service-*      # supports wildcards
        path: /catalog-info.yaml
        schedule:
          frequency: { minutes: 30 }
          timeout: { minutes: 3 }
```

### Microsoft Entra ID (Azure AD) Organization Data
- Plugin: `@backstage/plugin-catalog-backend-module-msgraph`
- Imports users and groups from Microsoft Entra ID via Microsoft Graph API
- Supports: Local dev (Azure CLI auth), App Registration, Managed Identity
- Required Graph API permissions: `GroupMember.Read.All`, `User.Read.All` (Application)
- Configuration:
```yaml
catalog:
  providers:
    microsoftGraphOrg:
      default:
        tenantId: ${AZURE_TENANT_ID}
        user:
          filter: accountEnabled eq true and userType eq 'member'
        group:
          filter: >
            securityEnabled eq false
            and mailEnabled eq true
            and groupTypes/any(c:c+eq+'Unified')
        schedule:
          frequency: PT1H
          timeout: PT50M
```
- Supports custom transformers for User, Group, and Organization entities

---

## 8. Deployment

### Technology Stack
- **Frontend**: React (single-page app), TypeScript
- **Backend**: Node.js, TypeScript
- **Database**: PostgreSQL (production), SQLite (dev)
- **Build**: Yarn 4.4.1 workspaces monorepo
- **Bundler**: Rspack
- **CLI**: `@backstage/cli` for create, build, dev operations

### Prerequisites
- Node.js 22 or 24 (Active LTS)
- Yarn 4.4.1
- Docker
- Git
- 20 GB disk, 6 GB memory minimum
- Unix-based OS (Linux, macOS, WSL)

### Quick Start
```bash
npx @backstage/create-app@latest    # Create new app
cd my-backstage-app
yarn start                           # Start dev server (frontend: 3000, backend: 7007)
```

### Kubernetes Deployment
1. Create namespace: `kubectl create namespace backstage`
2. Deploy PostgreSQL with Secret, PersistentVolume, Deployment, Service
3. Build Backstage Docker image
4. Deploy Backstage with Deployment + Service
5. Expose via Ingress or port-forward

### app-config.yaml for K8s
```yaml
app:
  baseUrl: http://localhost
backend:
  baseUrl: http://localhost
  listen:
    port: 7007
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}
```

### Key Config File: app-config.yaml
- Main configuration file for entire Backstage instance
- Supports environment variable substitution: `${VAR_NAME}`
- Sections: `app`, `backend`, `auth`, `catalog`, `integrations`, `proxy`, etc.

---

## 9. Key Packages

| Package | Purpose |
|---------|---------|
| `@backstage/create-app` | CLI to scaffold new Backstage apps |
| `@backstage/cli` | Build, dev, and management CLI |
| `@backstage/backend-plugin-api` | Backend plugin development API |
| `@backstage/frontend-plugin-api` | Frontend plugin development API |
| `@backstage/catalog-model` | Catalog entity type definitions |
| `@backstage/catalog-client` | Client for the Catalog API |
| `@backstage/core-components` | Shared React UI components |
| `@backstage/core-plugin-api` | Core frontend plugin APIs |
| `@backstage/plugin-catalog` | Software Catalog frontend plugin |
| `@backstage/plugin-catalog-backend` | Software Catalog backend plugin |
| `@backstage/plugin-scaffolder` | Software Templates frontend |
| `@backstage/plugin-scaffolder-backend` | Software Templates backend |
| `@backstage/plugin-techdocs` | TechDocs frontend |
| `@backstage/plugin-kubernetes` | Kubernetes frontend plugin |
| `@backstage/plugin-kubernetes-backend` | Kubernetes backend plugin |
| `@backstage/plugin-auth-backend-module-microsoft-provider` | Azure AD auth |
| `@backstage/plugin-catalog-backend-module-azure` | Azure DevOps discovery |
| `@backstage/plugin-catalog-backend-module-msgraph` | Entra ID org data import |

---

## 10. Relevance to TRAPI/Cordillera Platform Engineering

### Why Backstage Matters for This Project
1. **Developer Portal**: Central place for TRAPI API consumers to discover and use services
2. **Software Catalog**: Track all TRAPI services, Cordillera clusters, Radius environments
3. **Software Templates**: Standardized onboarding for new TRAPI consumers (auto-provision API keys, configure quotas)
4. **Azure Integration**: Native support for Azure AD, Azure DevOps, and Microsoft Graph
5. **Kubernetes Plugin**: Monitor Radius clusters, AKS health, pod status from a single pane
6. **TechDocs**: Host all TRAPI documentation alongside code

### Potential Integration Points
- **Catalog Entities**: Model TRAPI deployments, Radius environments, AKS clusters as Backstage entities
- **Azure DevOps Discovery**: Auto-discover TRAPI repos and catalog-info.yaml files
- **Entra ID**: Import Microsoft Research org structure for ownership/team tracking
- **Custom Plugins**: Build TRAPI-specific plugins (batch job monitoring, quota management, API key provisioning)
- **Scaffolder Actions**: Custom templates for "Create new TRAPI consumer" or "Deploy Radius environment"
- **Kubernetes**: Monitor Cordillera clusters and Radius workloads

### Architecture Fit
```
Backstage (Developer Portal)
├── Software Catalog
│   ├── TRAPI API Gateway (Component)
│   ├── Batch Processing Service (Component)
│   ├── Cordillera Bonete Cluster (Resource)
│   ├── Radius POC Environment (Resource)
│   └── trapi-python-lib (Component, type: library)
├── Software Templates
│   ├── "New TRAPI Consumer" template
│   ├── "New Radius Application" template
│   └── "New Cordillera Job" template
├── TechDocs
│   ├── TRAPI API Reference
│   ├── Cordillera User Guide
│   └── Radius Bootstrap Guide
└── Plugins
    ├── Kubernetes (Cordillera cluster monitoring)
    ├── Azure DevOps (CI/CD pipelines)
    └── Custom TRAPI Plugin (batch jobs, quotas)
```

---

## 11. backstage/docs-ui Repository

The `backstage/docs-ui` repository hosts the **Backstage UI Design System** documentation site.

### Key Facts
- It's a deployed static site (NOT a source code library)
- Built with React Server Components (RSC)
- Documents the `@backstage/ui` component library
- Focus: React + TypeScript + vanilla CSS approach
- Design system for building consistent Backstage plugin UIs

### Components Documented
- Layout components (Box, Stack, Grid, Inline)
- Form components (Button, Input, Select, Checkbox)
- Navigation components (Tabs, Breadcrumbs, Sidebar)
- Data display (Table, Card, List)
- Feedback (Alert, Toast, Dialog, Progress)

---

## 12. Quick Reference

### Create a New Backstage App
```bash
npx @backstage/create-app@latest
cd my-backstage-app
yarn start
```

### Register a Component
```yaml
# catalog-info.yaml in your repo root
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
  description: My awesome service
  annotations:
    dev.azure.com/project-slug: MyOrg/MyProject
    dev.azure.com/build-definition: MyPipeline
spec:
  type: service
  lifecycle: production
  owner: my-team
```

### Add Azure DevOps Integration
```yaml
# app-config.yaml
integrations:
  azure:
    - host: dev.azure.com
      credentials:
        - organizations:
            - myorg
          personalAccessToken: ${AZURE_TOKEN}
```

### Deploy to Kubernetes
```bash
# Build image
yarn build-image --tag backstage:1.0.0
# Apply K8s manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/postgres-secrets.yaml
kubectl apply -f kubernetes/postgres-storage.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/postgres-service.yaml
kubectl apply -f kubernetes/backstage-secrets.yaml
kubectl apply -f kubernetes/backstage.yaml
kubectl apply -f kubernetes/backstage-service.yaml
```

---

*Last updated: Session research from backstage/backstage GitHub repository*
*Document generated for Platform Engineering knowledge base*
