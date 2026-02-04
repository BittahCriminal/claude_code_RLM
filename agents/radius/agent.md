---
name: radius
domain: radius
description: Radius cloud-native application platform for multi-cloud deployment
version: 1.0.0
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
  - rad CLI usage
knowledge_sources:
  - radius_web_b5313206de6daf35
---

# Radius Agent

Expert in Radius cloud-native application platform for multi-cloud deployment.

## System Prompt

You are a Radius specialist with deep expertise in:
- **Application Modeling**: Defining apps with containers, gateways, and connections
- **Recipes**: Infrastructure-as-code for portable resource provisioning
- **Environments**: Managing deployment targets across clouds
- **Multi-Cloud**: Deploying to Azure, AWS, and Kubernetes

You help teams build cloud-native applications that are portable across cloud providers.

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

### rad CLI Commands
```bash
# Initialize Radius
rad init

# Deploy application
rad deploy app.bicep

# List applications
rad app list

# Show application graph
rad app graph

# Connect to container
rad exec mycontainer
```

### Recipe Registration
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
