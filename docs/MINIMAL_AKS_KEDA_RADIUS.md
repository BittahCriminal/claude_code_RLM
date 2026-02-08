# Minimal AKS Cluster with KEDA and Radius

**Purpose**: Lightweight AKS cluster for Radius-based infrastructure/app provisioning requests  
**Use Case**: Single-purpose cluster that receives deployment requests and provisions infra/apps via Radius

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Minimal AKS Cluster                          │
│                    (Standard_B2s - 2 vCPU, 4GB)                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   kube-system namespace                  │    │
│  │  • CoreDNS, kube-proxy, metrics-server                  │    │
│  │  • KEDA operator (~150m CPU, ~256Mi)                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  radius-system namespace                 │    │
│  │  • Radius Controller (~200m CPU, ~256Mi)                │    │
│  │  • Resource Providers (~100m CPU, ~128Mi)               │    │
│  │  • Dashboard (optional, can disable)                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  radius-apps namespace                   │    │
│  │  • Deployed applications (scale to 0 with KEDA)         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  request-handler namespace               │    │
│  │  • API/Webhook to receive deployment requests           │    │
│  │  • Scales to 0 when idle (KEDA)                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Azure Resources │
                    │ (provisioned    │
                    │  by Radius)     │
                    └─────────────────┘
```

---

## Cluster Specifications

### Smallest Viable Configuration

| Component | Specification | Rationale |
|-----------|--------------|-----------|
| **Node Size** | `Standard_B2s` (2 vCPU, 4GB RAM) | Burstable, lowest cost for light workloads |
| **Node Count** | 1 node (can scale to 2 for HA) | Minimum footprint |
| **OS** | Azure Linux | Smaller image, faster boot, lower overhead |
| **Max Pods** | 30 (default for small VMs) | Sufficient for system + Radius components |

### Resource Budget

| Component | CPU Request | Memory Request | Notes |
|-----------|-------------|----------------|-------|
| **System Reserved** | ~140m | ~750Mi | AKS reserves for kubelet, OS |
| **CoreDNS** | 100m | 70Mi | 2 pods |
| **KEDA Operator** | 100m | 128Mi | AKS addon |
| **KEDA Metrics Server** | 100m | 128Mi | AKS addon |
| **Radius Controller** | 200m | 256Mi | Core component |
| **Radius Dashboard** | 50m | 64Mi | Optional - can disable |
| **Request Handler** | 100m | 128Mi | Scales to 0 when idle |
| **Available for Apps** | ~600m | ~1.5Gi | Remaining capacity |

**Total Cluster Overhead**: ~1.4 vCPU, ~2.5GB used by system/control plane  
**Available for Workloads**: ~0.6 vCPU, ~1.5GB

---

## Deployment

### Option 1: Azure CLI (Quickest)

```bash
#!/bin/bash
set -e

# Variables
RG_NAME="rg-radius-minimal"
LOCATION="eastus2"
AKS_NAME="aks-radius-mini"

# Create resource group
az group create --name $RG_NAME --location $LOCATION

# Create minimal AKS cluster with KEDA addon
az aks create \
    --resource-group $RG_NAME \
    --name $AKS_NAME \
    --location $LOCATION \
    --node-count 1 \
    --node-vm-size Standard_B2s \
    --os-sku AzureLinux \
    --enable-keda \
    --enable-managed-identity \
    --network-plugin azure \
    --network-plugin-mode overlay \
    --tier free \
    --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group $RG_NAME --name $AKS_NAME

# Verify KEDA is running
kubectl get pods -n kube-system -l app=keda-operator

# Install Radius
curl -fsSL "https://get.radapp.io/tools/rad/install.sh" | /bin/bash
rad install kubernetes

# Initialize Radius with Azure provider
rad init --full

echo "Minimal AKS with KEDA and Radius ready!"
```

### Option 2: Bicep (Infrastructure as Code)

```bicep
// infra/minimal-aks.bicep
@description('Location for resources')
param location string = resourceGroup().location

@description('AKS cluster name')
param clusterName string = 'aks-radius-mini'

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${clusterName}-identity'
  location: location
}

resource aks 'Microsoft.ContainerService/managedClusters@2024-01-01' = {
  name: clusterName
  location: location
  sku: {
    name: 'Base'
    tier: 'Free'  // Use Free tier for POC
  }
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    kubernetesVersion: '1.29'
    dnsPrefix: clusterName
    
    // Minimal agent pool configuration
    agentPoolProfiles: [
      {
        name: 'system'
        count: 1
        vmSize: 'Standard_B2s'          // Burstable, 2 vCPU, 4GB
        osType: 'Linux'
        osSKU: 'AzureLinux'             // Smaller footprint
        mode: 'System'
        enableAutoScaling: true
        minCount: 1
        maxCount: 2                      // Allow scale up if needed
        maxPods: 30
      }
    ]
    
    // Network configuration - overlay for lower overhead
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay'       // Lower IP consumption
      networkPolicy: 'azure'
      serviceCidr: '10.0.0.0/16'
      dnsServiceIP: '10.0.0.10'
    }
    
    // Enable KEDA addon
    workloadAutoScalerProfile: {
      keda: {
        enabled: true
      }
    }
    
    // Minimal monitoring (disable Container Insights to save resources)
    addonProfiles: {
      omsagent: {
        enabled: false  // Disable for minimal footprint
      }
    }
  }
}

output aksId string = aks.id
output aksName string = aks.name
output identityClientId string = managedIdentity.properties.clientId
```

---

## Install Radius with Minimal Footprint

### Default Installation

```bash
# Install rad CLI
# Windows:
iwr -useb "https://get.radapp.io/tools/rad/install.ps1" | iex

# Linux/Mac:
curl -fsSL "https://get.radapp.io/tools/rad/install.sh" | /bin/bash

# Install Radius on cluster
rad install kubernetes

# Initialize with Azure provider
rad init --full
```

### Verify Radius Resource Usage

```bash
# Check Radius pods
kubectl get pods -n radius-system

# Check resource usage
kubectl top pods -n radius-system

# Typical output for minimal install:
# NAME                                    CPU(cores)   MEMORY(bytes)
# controller-xxx                          15m          120Mi
# applications-rp-xxx                     10m          80Mi
# ucp-xxx                                 12m          90Mi
```

### Reduce Radius Footprint (Optional)

If you need even smaller footprint, you can manually set resource limits:

```yaml
# radius-resource-limits.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: radius-limits
  namespace: radius-system
spec:
  limits:
  - default:
      cpu: 200m
      memory: 256Mi
    defaultRequest:
      cpu: 50m
      memory: 64Mi
    type: Container
```

```bash
kubectl apply -f radius-resource-limits.yaml
```

---

## KEDA Configuration for Scale-to-Zero

### Request Handler with HTTP Scaler

Create a deployment that scales to 0 when no requests are coming in:

```yaml
# request-handler.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: request-handler
  namespace: request-handler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: request-handler
  template:
    metadata:
      labels:
        app: request-handler
    spec:
      containers:
      - name: handler
        image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 200m
            memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: request-handler
  namespace: request-handler
spec:
  selector:
    app: request-handler
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: request-handler-scaler
  namespace: request-handler
spec:
  scaleTargetRef:
    name: request-handler
  minReplicaCount: 0           # Scale to zero!
  maxReplicaCount: 3
  cooldownPeriod: 300          # 5 minutes before scale down
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-server.monitoring.svc.cluster.local
      metricName: http_requests_total
      threshold: '10'
      query: sum(rate(http_requests_total{service="request-handler"}[1m]))
```

### Azure Service Bus Trigger (Alternative)

For a queue-based request handler:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: radius-job-processor
  namespace: request-handler
spec:
  scaleTargetRef:
    name: radius-job-processor
  minReplicaCount: 0
  maxReplicaCount: 5
  triggers:
  - type: azure-servicebus
    metadata:
      queueName: radius-requests
      messageCount: '5'
    authenticationRef:
      name: azure-servicebus-auth
```

---

## Radius Environment for Infra/App Provisioning

### Create Environment

```bicep
// environments/dev.bicep
import radius as radius

resource env 'Applications.Core/environments@2023-10-01-preview' = {
  name: 'dev'
  properties: {
    compute: {
      kind: 'kubernetes'
      namespace: 'radius-apps'
    }
    providers: {
      azure: {
        scope: '/subscriptions/${subscription().subscriptionId}/resourceGroups/${resourceGroup().name}'
      }
    }
  }
}
```

```bash
rad deploy environments/dev.bicep
rad env switch dev
```

### Sample Application Template

```bicep
// apps/sample-app.bicep
import radius as radius

@description('Environment to deploy to')
param environment string

resource app 'Applications.Core/applications@2023-10-01-preview' = {
  name: 'sample-app'
  properties: {
    environment: environment
  }
}

resource container 'Applications.Core/containers@2023-10-01-preview' = {
  name: 'web'
  properties: {
    application: app.id
    container: {
      image: 'nginx:alpine'
      ports: {
        http: {
          containerPort: 80
        }
      }
      resources: {
        cpu: '0.1'       // 100m
        memory: '128Mi'
      }
    }
  }
}

// Optional: Add Azure resources
resource storage 'Applications.Core/extenders@2023-10-01-preview' = {
  name: 'storage'
  properties: {
    application: app.id
    resourceProvisioning: 'recipe'
    recipe: {
      name: 'azure-storage'
    }
  }
}
```

---

## Request Handler API Design

For receiving deployment requests, you can create a simple API:

```python
# request_handler.py
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    """
    Receive deployment request and invoke Radius
    
    Expected payload:
    {
        "app_name": "my-app",
        "template": "apps/sample-app.bicep",
        "environment": "dev",
        "parameters": {}
    }
    """
    data = request.json
    app_name = data.get('app_name')
    template = data.get('template')
    environment = data.get('environment', 'dev')
    params = data.get('parameters', {})
    
    # Build rad deploy command
    cmd = ['rad', 'deploy', template, '-e', environment]
    
    # Add parameters
    for key, value in params.items():
        cmd.extend(['-p', f'{key}={value}'])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return jsonify({
            'status': 'success' if result.returncode == 0 else 'failed',
            'output': result.stdout,
            'error': result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'status': 'timeout'}), 504

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Dockerfile for Request Handler

```dockerfile
FROM python:3.11-slim

# Install rad CLI
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL "https://get.radapp.io/tools/rad/install.sh" | /bin/bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY request_handler.py .

EXPOSE 8080
CMD ["python", "request_handler.py"]
```

---

## Cost Optimization Tips

| Optimization | Savings | How |
|--------------|---------|-----|
| **Free tier AKS** | No control plane cost | `--tier free` |
| **B-series VMs** | ~60% vs D-series | `Standard_B2s` |
| **Spot nodes** (user pools) | ~70% | `--enable-spot` |
| **Azure Linux OS** | Faster, smaller | `--os-sku AzureLinux` |
| **Scale to zero (KEDA)** | Pay only when active | ScaledObject minReplicas: 0 |
| **Disable monitoring** | ~$50/month | Disable Container Insights |
| **Overlay networking** | Fewer IPs needed | `--network-plugin-mode overlay` |

### Estimated Monthly Cost

| Resource | Size | Monthly Cost (East US 2) |
|----------|------|-------------------------|
| AKS Control Plane (Free) | - | $0 |
| Standard_B2s node | 1 node | ~$30 |
| Managed Disk (OS) | 128GB Premium | ~$20 |
| **Total** | | **~$50/month** |

---

## Quick Start Commands

```bash
# 1. Create cluster (5 minutes)
az aks create -g rg-radius -n aks-radius-mini --node-count 1 \
  --node-vm-size Standard_B2s --os-sku AzureLinux --enable-keda \
  --tier free --generate-ssh-keys

# 2. Get credentials
az aks get-credentials -g rg-radius -n aks-radius-mini

# 3. Install Radius (2 minutes)
curl -fsSL "https://get.radapp.io/tools/rad/install.sh" | /bin/bash
rad install kubernetes
rad init --full

# 4. Verify
kubectl get pods -n kube-system | grep keda
kubectl get pods -n radius-system

# 5. Deploy first app
rad deploy apps/sample-app.bicep -e dev
```

---

## Summary

This configuration provides:

✅ **Smallest AKS footprint**: 1x Standard_B2s node (~$50/month)  
✅ **KEDA for scale-to-zero**: Apps and handlers scale down when idle  
✅ **Radius for infra/app provisioning**: Deploy apps and Azure resources via Bicep  
✅ **Request-driven**: API endpoint to receive deployment requests  
✅ **Azure Linux**: Smaller OS footprint, faster boot  
✅ **Overlay networking**: Lower IP consumption  

**Total resource usage**:
- System components: ~1.4 vCPU, ~2.5GB RAM
- Available for apps: ~0.6 vCPU, ~1.5GB RAM (scales up with cluster autoscaler if needed)
