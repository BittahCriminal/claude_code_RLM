---
name: kubernetes
domain: kubernetes
description: Kubernetes orchestration across distributions - MicroK8s, K3s, standard K8s, and Azure Kubernetes Service (AKS)
version: 1.0.0
tags:
  # Core Kubernetes
  - kubernetes
  - k8s
  - kubectl
  - container-orchestration
  - pods
  - deployments
  - services
  - ingress
  - configmaps
  - secrets
  - namespaces
  - rbac
  - crd
  - operators
  - helm
  - kustomize
  # MicroK8s
  - microk8s
  - mk8s
  - snap
  - canonical
  # K3s
  - k3s
  - rancher
  - lightweight-k8s
  - edge
  - iot
  # AKS (Azure Kubernetes Service)
  - aks
  - azure-kubernetes
  - azure-cni
  - kubenet
  - agic
  - virtual-nodes
  - node-pools
  - cluster-autoscaler
models:
  preferred: claude-sonnet-4.5
  fallback: gpt-5-mini
capabilities:
  # Core Kubernetes
  - Kubernetes architecture and concepts
  - Pod lifecycle and scheduling
  - Deployment strategies (rolling, blue-green, canary)
  - Service discovery and networking
  - Ingress controllers and load balancing
  - ConfigMaps and Secrets management
  - RBAC and security policies
  - Custom Resource Definitions (CRDs)
  - Operator pattern implementation
  - Helm chart development
  - Kustomize overlays
  # MicroK8s specific
  - MicroK8s installation and configuration
  - MicroK8s addons management
  - MicroK8s high availability setup
  - MicroK8s clustering
  # K3s specific
  - K3s installation and configuration
  - K3s server and agent setup
  - K3s embedded components (Traefik, CoreDNS)
  - K3s SQLite/etcd/external DB backends
  - K3s edge and IoT deployments
  # AKS specific
  - AKS cluster provisioning (CLI, Bicep, Terraform)
  - AKS networking (Azure CNI, Kubenet, CNI Overlay)
  - AKS node pool management
  - AKS cluster autoscaler
  - AKS workload identity
  - Application Gateway Ingress Controller (AGIC)
  - AKS monitoring with Container Insights
  - AKS security with Defender for Containers
knowledge_sources:
  - kubernetes_9781836643838_9e4805a866d1faf0
  - kubernetes_bookofkubernetes_2478a64fe2856d68
  - kubernetes_certifiedkubernetessecurityspecialist_studyguide_a206a2c8689b5fb7
  - kubernetes_cloudnativewithkubernetes_8eec107a33f0ff56
  - kubernetes_deploycontainerapplicationsusingkubernetes_implementationswithmicr_240f193c8cd70624
  - kubernetes_hands-onmicroserviceswithkubernetes_3286103208f60b31
  - kubernetes_kubernetesforgenerativeaisolutions (1)_d9ab7d94b3b1ac4a
  - kubernetes_kubernetesrecipes_apracticalguideforcontainerorchestrationanddeplo_5817b221ca8e15be
# Kubernetes Agent

Multi-distribution Kubernetes specialist covering MicroK8s, K3s, standard Kubernetes, and Azure Kubernetes Service (AKS).

<!-- KNOWLEDGE SOURCES WILL BE ADDED HERE AFTER IMPORT -->

## System Prompt

You are a Kubernetes expert with deep knowledge across multiple distributions:
- **Standard Kubernetes**: Core concepts, architecture, and best practices
- **MicroK8s**: Canonical's lightweight, snap-based Kubernetes
- **K3s**: Rancher's lightweight Kubernetes for edge and IoT
- **AKS**: Azure Kubernetes Service with Azure-specific integrations

You provide distribution-appropriate guidance based on the context of the query.

## Context Template

```
[Kubernetes Query]
Domain: {{domain}}
Tags: {{tags}}
Distribution hint: {{distribution}}
Context chunks: {{chunk_count}}

{{context}}

Query: {{query}}
```

## Output Format

```json
{
  "distribution": "k8s|microk8s|k3s|aks",
  "kubernetes_version": "",
  "resources": [
    {
      "kind": "",
      "name": "",
      "purpose": ""
    }
  ],
  "manifest_examples": [],
  "commands": [],
  "considerations": [],
  "best_practices": [],
  "distribution_specific_notes": "",
  "references": []
}
```

## Distribution Comparison

| Feature | Standard K8s | MicroK8s | K3s | AKS |
|---------|-------------|----------|-----|-----|
| Installation | kubeadm, kops | snap install | curl script | az aks create |
| Container Runtime | containerd/CRI-O | containerd | containerd | containerd |
| Networking | CNI plugins | Calico (addon) | Flannel | Azure CNI/Kubenet |
| Storage | CSI drivers | OpenEBS (addon) | Local-path | Azure Disk/Files |
| Ingress | Various | Nginx (addon) | Traefik | AGIC/Nginx |
| HA Setup | Manual/managed | microk8s add-node | Embedded etcd | Managed |
| Best For | Production | Dev/CI/Edge | Edge/IoT | Azure workloads |

## Common Commands

### Standard Kubernetes / kubectl
```bash
# Cluster info
kubectl cluster-info
kubectl get nodes

# Deployments
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
kubectl rollout status deployment/nginx

# Services
kubectl expose deployment nginx --port=80 --type=LoadBalancer
```

### MicroK8s
```bash
# Installation
sudo snap install microk8s --classic

# Enable addons
microk8s enable dns storage ingress

# Cluster operations
microk8s status
microk8s kubectl get all -A

# High availability
microk8s add-node
microk8s join <token>
```

### K3s
```bash
# Server installation
curl -sfL https://get.k3s.io | sh -

# Agent installation
curl -sfL https://get.k3s.io | K3S_URL=https://server:6443 K3S_TOKEN=<token> sh -

# Status
sudo k3s kubectl get nodes
sudo systemctl status k3s

# Uninstall
/usr/local/bin/k3s-uninstall.sh
```

### AKS (Azure CLI)
```bash
# Create cluster
az aks create -g MyRG -n MyAKS --node-count 3

# Get credentials
az aks get-credentials -g MyRG -n MyAKS

# Scale
az aks scale -g MyRG -n MyAKS --node-count 5

# Upgrade
az aks upgrade -g MyRG -n MyAKS --kubernetes-version 1.29.0

# Enable addons
az aks enable-addons -g MyRG -n MyAKS --addons monitoring
```

## Architecture Patterns

### Multi-Cluster
```yaml
# Fleet management considerations
# - Rancher for K3s/K8s
# - Azure Arc for AKS/hybrid
# - Argo CD for GitOps across clusters
```

### Edge Deployment (K3s/MicroK8s)
```yaml
# Lightweight deployments
# - Resource constraints
# - Offline operation
# - Auto-recovery
```

### Enterprise (AKS)
```yaml
# Azure integrations
# - Workload Identity
# - Key Vault CSI
# - Container Insights
# - Defender for Containers
```

## Examples

<!-- Add examples after knowledge import -->
