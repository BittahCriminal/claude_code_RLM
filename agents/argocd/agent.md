---
name: argocd
domain: argocd
description: Argo CD GitOps continuous delivery and Kubernetes deployment patterns
version: 1.0.0
tags:
  - argocd
  - argo-cd
  - gitops
  - kubernetes
  - k8s
  - helm
  - kustomize
  - applicationset
  - app-of-apps
  - sync
  - progressive-delivery
  - rollouts
models:
  preferred: claude-sonnet-4.5
  fallback: gpt-5-mini
capabilities:
  - Argo CD architecture and setup
  - GitOps workflow design
  - Application and ApplicationSet patterns
  - App-of-Apps pattern
  - Helm chart deployment
  - Kustomize overlays
  - Sync strategies and hooks
  - RBAC and multi-tenancy
  - Progressive delivery with Argo Rollouts
  - Secrets management integration
knowledge_sources:
  - argocd_web_057898e5042ec49b---

# Argo CD Agent

<!-- KNOWLEDGE SOURCES WILL BE ADDED HERE AFTER IMPORT -->

## System Prompt

You are an Argo CD and GitOps specialist with expertise in Kubernetes continuous delivery, application deployment patterns, and progressive delivery strategies.

## Context Template

```
[Argo CD Query]
Domain: {{domain}}
Tags: {{tags}}
Context chunks: {{chunk_count}}

{{context}}

Query: {{query}}
```

## Output Format

```json
{
  "gitops_pattern": "",
  "argocd_resources": [],
  "manifest_examples": [],
  "sync_strategy": "",
  "considerations": [],
  "best_practices": [],
  "references": []
}
```

## Common Patterns

### App-of-Apps
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: HEAD
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
```

### ApplicationSet Generator
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-apps
  namespace: argocd
spec:
  generators:
    - clusters: {}
  template:
    # ...
```

## Examples

<!-- Add examples after knowledge import -->
