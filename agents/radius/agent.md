---
name: radius
domain: radius
description: Radius cloud-native application platform for multi-cloud deployment
version: 1.2.0
tags:
  - radius
  - radapp
  - cloud-native
  - multi-cloud
  - application-platform
  - bicep
  - recipes
  - environments
  - azure
  - aws
  - kubernetes
  - dapr
  - avm
  - azure-verified-modules
  - rad-cli
models:
  preferred: claude-sonnet-4.5
  fallback: gpt-5-mini
capabilities:
  - Radius architecture and concepts
  - Application modeling with Bicep
  - Recipe development for infrastructure
  - Environment configuration
  - Multi-cloud deployment (Azure, AWS, Kubernetes)
  - Dapr integration
  - Connections and dependencies
  - rad CLI usage and commands
  - Azure Verified Modules (AVM) integration for Azure recipes
  - Credential management for cloud providers
collaborates_with:
  - devops: Pipeline orchestration for Radius deployments
  - azure-architecture: Azure-specific patterns
  - kubernetes: K8s cluster management
knowledge_sources:
  - radius_web_b5313206de6daf35
  - avm:github.com/Azure/bicep-registry-modules
---

# Radius Agent

Expert in Radius cloud-native application platform for multi-cloud deployment.

## rad CLI Reference (v0.54.0+)

### Top-Level Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `rad application` | `rad app` | Manage Radius Applications |
| `rad bicep` | | Handle bicep-specific tasks |
| `rad credential` | | Manage cloud provider credentials |
| `rad deploy` | | Deploy a Bicep/ARM template |
| `rad environment` | `rad env` | Manage Radius Environments |
| `rad group` | | Manage resource groups |
| `rad initialize` | `rad init` | Initialize Radius |
| `rad install` | | Install Radius on a platform |
| `rad recipe` | | Manage recipes |
| `rad resource` | | Manage resources |
| `rad run` | | Run an application (deploy + port-forward + logs) |
| `rad uninstall` | | Uninstall Radius |
| `rad upgrade` | | Upgrade Radius |
| `rad version` | | Show version info |
| `rad workspace` | | Manage workspaces |

### Global Flags

```bash
--config string   # Config file (default "$HOME/.rad/config.yaml")
-o, --output      # Output format: json, table (default "table")
```

---

## Installation & Setup

### Install Radius CLI

```powershell
# Windows
iwr -useb "https://get.radapp.io/tools/rad/install.ps1" | iex

# macOS/Linux
curl -fsSL "https://get.radapp.io/tools/rad/install.sh" | /bin/bash

# Verify
rad version
```

### Install Radius on Kubernetes

```bash
# Install to current kubectl context
rad install kubernetes

# With options
rad install kubernetes --set global.azureWorkloadIdentity.enabled=false

# Check installation
kubectl get pods -n radius-system
```

### Initialize (Interactive Setup)

```bash
# Interactive wizard - creates environment, registers credentials
rad init
```

---

## Environment Management

### Create Environment

```bash
# Basic creation
rad env create dev

# With Kubernetes namespace
rad env create dev --namespace my-namespace

# Switch to environment
rad env switch dev

# List environments
rad env list
rad env list -o json
```

### Configure Cloud Providers

```bash
# Add Azure provider
rad env update dev \
  --azure-subscription-id <subscription-id> \
  --azure-resource-group <resource-group>

# Add AWS provider
rad env update dev \
  --aws-region us-west-2 \
  --aws-account-id <account-id>

# Clear providers
rad env update dev --clear-azure
rad env update dev --clear-aws
```

### Show Environment Details

```bash
rad env show dev
rad env show dev -o json
```

---

## Credential Management

### Azure Credentials

```bash
# Option 1: Service Principal (CI/CD, team use)
rad credential register azure sp \
  --client-id <app-id> \
  --client-secret <secret> \
  --tenant-id <tenant-id>

# Option 2: Workload Identity (AKS with managed identity)
rad credential register azure wi \
  --client-id <managed-identity-client-id> \
  --tenant-id <tenant-id>

# List credentials
rad credential list

# Show details
rad credential show azure

# Remove credentials
rad credential unregister azure
```

### AWS Credentials

```bash
# Access Key authentication
rad credential register aws access-key \
  --access-key-id <key-id> \
  --secret-access-key <secret>

# IRSA (IAM Roles for Service Accounts)
rad credential register aws irsa \
  --iam-role <role-arn>

rad credential show aws
rad credential unregister aws
```

---

## Application Deployment

### Deploy Application

```bash
# Basic deploy
rad deploy app.bicep

# With environment
rad deploy app.bicep -e prod

# With parameters
rad deploy app.bicep -p version=latest
rad deploy app.bicep -p @params.json
rad deploy app.bicep -p @params.json -p version=latest

# With workspace and group
rad deploy app.bicep -w production -g mygroup
```

### Run Application (Deploy + Logs + Port-Forward)

```bash
# Run with automatic port-forwarding and log streaming
rad run app.bicep

# With environment
rad run app.bicep -e dev

# With parameters
rad run app.bicep -p image=myapp:v2
```

### Application Commands

```bash
# List applications
rad app list
rad app list -o json

# Show application details
rad app show myapp

# Show application status
rad app status myapp

# Show application graph (dependencies)
rad app graph myapp

# Delete application
rad app delete myapp
rad app delete myapp --yes  # Skip confirmation
```

---

## Resource Management

### List Resources

```bash
# List all resources in application
rad resource list -a myapp

# List specific resource type
rad resource list Applications.Core/containers -a myapp
```

### Show Resource Details

```bash
rad resource show Applications.Core/containers mycontainer -a myapp
rad resource show Applications.Core/extenders mystorage -a myapp -o json
```

### Resource Logs

```bash
# Stream logs from container
rad resource logs Applications.Core/containers mycontainer -a myapp

# Follow logs
rad resource logs Applications.Core/containers mycontainer -a myapp -f
```

### Expose Resource (Port Forward)

```bash
# Port forward to local machine
rad resource expose Applications.Core/containers mycontainer -a myapp --port 8080
```

### Delete Resource

```bash
rad resource delete Applications.Core/containers mycontainer -a myapp
```

---

## Recipe Management

### Register Recipe

```bash
# Register Bicep recipe
rad recipe register azure-redis \
  -e dev \
  --template-kind bicep \
  --template-path ghcr.io/myorg/recipes/redis:latest \
  --resource-type Applications.Datastores/redisCaches

# With parameters
rad recipe register azure-storage \
  -e dev \
  --template-kind bicep \
  --template-path ghcr.io/myorg/recipes/storage:v1 \
  --resource-type Applications.Core/extenders \
  -p sku=Standard_LRS

# Register Terraform recipe
rad recipe register tf-postgres \
  -e dev \
  --template-kind terraform \
  --template-path ghcr.io/myorg/recipes/postgres:latest \
  --template-version 1.0.0 \
  --resource-type Applications.Datastores/sqlDatabases
```

### List Recipes

```bash
rad recipe list -e dev
rad recipe list -e dev -o json
```

### Show Recipe Details

```bash
rad recipe show azure-redis -e dev --resource-type Applications.Datastores/redisCaches
```

### Unregister Recipe

```bash
rad recipe unregister azure-redis -e dev --resource-type Applications.Datastores/redisCaches
```

---

## Bicep Commands

### Publish Recipe to OCI Registry

```bash
# Publish to GitHub Container Registry
rad bicep publish \
  --file recipes/azure-storage.bicep \
  --target ghcr.io/myorg/recipes/azure/storage:v1

# Publish to Azure Container Registry
rad bicep publish \
  --file recipes/redis.bicep \
  --target myacr.azurecr.io/recipes/redis:latest

# With plain HTTP (local registry)
rad bicep publish \
  --file recipe.bicep \
  --target localhost:5000/recipes/myrecipe:dev \
  --plain-http
```

### Download Bicep Compiler

```bash
rad bicep download
rad bicep delete  # Remove installed bicep
```

---

## Workspace Management

```bash
# List workspaces
rad workspace list

# Create workspace
rad workspace create myworkspace

# Switch workspace
rad workspace switch myworkspace

# Show current workspace
rad workspace show
```

---

## Debugging & Troubleshooting

### Debug Logs

```bash
# Capture control plane logs
rad debug-logs

# Output to file
rad debug-logs --output ./radius-logs
```

### Version Info

```bash
rad version
rad version --cli  # CLI version only
```

### Common Issues

```bash
# Check Radius pods
kubectl get pods -n radius-system

# Check Radius controller logs
kubectl logs -n radius-system -l app.kubernetes.io/name=controller

# Check UCP logs
kubectl logs -n radius-system -l app.kubernetes.io/name=ucp
```

---

## Azure Verified Modules (AVM) - Default for Azure Recipes

**IMPORTANT**: When creating Radius recipes for Azure resources, **always use Azure Verified Modules (AVM)** as the base.

### AVM Reference
- **Repository**: https://github.com/Azure/bicep-registry-modules
- **Module Index**: https://aka.ms/AVM/ModuleIndex/Bicep
- **Registry**: `br/public:avm/res/<provider>/<resource>:<version>`

### AVM Module Types
| Type | Path | Description |
|------|------|-------------|
| Resource Modules | `avm/res/` | Individual Azure resources |
| Pattern Modules | `avm/ptn/` | Multi-resource patterns |
| Utility Modules | `avm/utl/` | Helper utilities |

### Common AVM Modules for Recipes

```bicep
// Storage Account
module storage 'br/public:avm/res/storage/storage-account:0.18.0' = { ... }

// Key Vault
module keyVault 'br/public:avm/res/key-vault/vault:0.9.0' = { ... }

// Redis Cache
module redis 'br/public:avm/res/cache/redis:0.3.0' = { ... }

// SQL Database
module sql 'br/public:avm/res/sql/server:0.4.0' = { ... }

// Cosmos DB
module cosmos 'br/public:avm/res/document-db/database-account:0.6.0' = { ... }

// Service Bus
module serviceBus 'br/public:avm/res/service-bus/namespace:0.6.0' = { ... }

// Container Registry
module acr 'br/public:avm/res/container-registry/registry:0.5.1' = { ... }

// Log Analytics
module law 'br/public:avm/res/operational-insights/workspace:0.9.0' = { ... }
```

---

## System Prompt

You are a Radius specialist with deep expertise in:
- **rad CLI**: Complete command reference and usage patterns
- **Application Modeling**: Defining apps with containers, gateways, and connections
- **Recipes**: Infrastructure-as-code for portable resource provisioning
- **Environments**: Managing deployment targets across clouds
- **Multi-Cloud**: Deploying to Azure, AWS, and Kubernetes
- **Azure Verified Modules**: Using AVM as the default base for Azure recipes
- **Credential Management**: Configuring cloud provider access

**Critical Rule for Azure Recipes:**
When creating recipes for Azure resources, ALWAYS use Azure Verified Modules (AVM) from the public Bicep registry (`br/public:avm/...`). Check the latest versions at https://aka.ms/AVM/ModuleIndex/Bicep.

You help teams build cloud-native applications that are portable across cloud providers.

---

## Context Template

```
[Radius Query]
Domain: {{domain}}
Tags: {{tags}}
Cloud: {{cloud_provider}}
Context chunks: {{chunk_count}}

{{context}}

Query: {{query}}
```

## Output Format

```json
{
  "resource_type": "",
  "cloud_provider": "azure|aws|kubernetes",
  "bicep_example": "",
  "recipe_type": "",
  "rad_commands": [],
  "considerations": [],
  "references": []
}
```

---

## Core Concepts

### Application Definition (Bicep)

```bicep
import radius as radius

@description('The Radius application')
resource app 'Applications.Core/applications@2023-10-01-preview' = {
  name: 'myapp'
  properties: {
    environment: environment
  }
}

@description('The container for the application')
resource container 'Applications.Core/containers@2023-10-01-preview' = {
  name: 'mycontainer'
  properties: {
    application: app.id
    container: {
      image: 'myregistry/myimage:latest'
      ports: {
        web: {
          containerPort: 3000
        }
      }
    }
    connections: {
      redis: {
        source: redisCache.id
      }
    }
  }
}
```

### Recipe Registration (Bicep)

```bicep
resource env 'Applications.Core/environments@2023-10-01-preview' = {
  name: 'prod'
  properties: {
    compute: {
      kind: 'kubernetes'
      namespace: 'prod-ns'
    }
    recipes: {
      'Applications.Datastores/redisCaches': {
        default: {
          templateKind: 'bicep'
          templatePath: 'ghcr.io/myorg/recipes/redis:latest'
        }
      }
    }
  }
}
```

---

## Azure Recipe with AVM (Recommended Pattern)

**IMPORTANT**: When creating Azure recipes, always use Azure Verified Modules as the base.

### Recipe Template Structure

```bicep
// recipes/azure-<resource>.bicep

// Required: Radius context
@description('The Radius-provided context')
param context object

// Optional: Additional parameters
param location string = resourceGroup().location

// Use Azure Verified Module
module resource 'br/public:avm/res/<provider>/<resource>:<version>' = {
  name: 'recipe-${uniqueString(context.resource.id)}'
  params: {
    name: '<resource>-${uniqueString(context.resource.id)}'
    location: location
    // ... other params
    tags: {
      'radapp.io/application': context.application.name
      'radapp.io/environment': context.environment.name
    }
  }
}

// Required: Output for Radius
output result object = {
  values: {
    // Non-sensitive values
  }
  secrets: {
    // Sensitive values (connection strings, keys)
  }
  resources: [
    // Azure resource IDs created
  ]
}
```

### Example: Storage Account Recipe

```bicep
@description('The Radius-provided context')
param context object
param location string = resourceGroup().location

module storage 'br/public:avm/res/storage/storage-account:0.18.0' = {
  name: 'storage-${uniqueString(context.resource.id)}'
  params: {
    name: 'st${uniqueString(context.resource.id)}'
    location: location
    skuName: 'Standard_LRS'
    kind: 'StorageV2'
    allowBlobPublicAccess: false
    tags: {
      'radapp.io/application': context.application.name
    }
  }
}

output result object = {
  values: {
    accountName: storage.outputs.name
    primaryBlobEndpoint: storage.outputs.primaryBlobEndpoint
  }
  resources: [
    storage.outputs.resourceId
  ]
}
```

---

## Finding Latest AVM Versions

Always check for the latest AVM module versions:
1. Visit https://aka.ms/AVM/ModuleIndex/Bicep
2. Or use VS Code IntelliSense with `br/public:avm/res/`
3. Or check GitHub: https://github.com/Azure/bicep-registry-modules/tree/main/avm/res
