# AKS Private Cluster POC with Radius Integration

**Date**: February 4, 2026  
**Purpose**: POC for private AKS cluster with VNet integration, Bastion access, certificates, and Radius deployment

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Azure Subscription                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        Virtual Network (10.0.0.0/16)                 │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │    │
│  │  │  AKS Subnet      │  │  API Server      │  │  Bastion Subnet  │   │    │
│  │  │  10.0.1.0/24     │  │  Subnet          │  │  10.0.3.0/26     │   │    │
│  │  │                  │  │  10.0.2.0/28     │  │  (AzureBastionSubnet)│  │    │
│  │  │  ┌────────────┐  │  │                  │  │                  │   │    │
│  │  │  │ AKS Private│  │  │  ┌────────────┐  │  │  ┌────────────┐  │   │    │
│  │  │  │ Cluster    │◄─┼──┼──│API Server  │  │  │  │ Bastion    │  │   │    │
│  │  │  │ (Radius)   │  │  │  │ Endpoint   │  │  │  │ Host       │  │   │    │
│  │  │  └────────────┘  │  │  └────────────┘  │  │  └─────┬──────┘  │   │    │
│  │  └──────────────────┘  └──────────────────┘  └────────┼─────────┘   │    │
│  └───────────────────────────────────────────────────────┼─────────────┘    │
│                                                          │                   │
│  ┌─────────────────────────────────────────────────────┐ │                   │
│  │                   Supporting Services                │ ▼                   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐     ┌──────────┐     │
│  │  │ Key Vault    │  │ Container    │  │ Managed    │     │ Jump VM  │     │
│  │  │ (Certs)      │  │ Registry     │  │ Identity   │     │ (optional)│    │
│  │  └──────────────┘  └──────────────┘  └────────────┘     └──────────┘     │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Option 1: Radius on ACI (Simpler for POC)

Based on the [Microsoft Tech Community article](https://techcommunity.microsoft.com/blog/azurecompute/use-radius-to-deploy-your-applications-to-azure-container-instances/4428551), Radius now supports deploying applications directly to Azure Container Instances without needing Kubernetes.

### How Radius + ACI Works

1. **Radius Control Plane** still runs on Kubernetes (can be a simple cluster)
2. **Application deployments** can target ACI instead of K8s pods
3. Radius provisions: VNet, Load Balancer, NSG, Container Groups, NGroups

### ACI Environment Definition

```bicep
resource aciEnv 'Applications.Core/environments@2023-10-01-preview' = {
  name: 'aci-poc'
  properties: {
    compute: {
      kind: 'aci'
      resourceGroup: '/subscriptions/<sub-id>/resourceGroups/<rg-name>'
      identity: {
        kind: 'userAssigned'
        managedIdentity: ['/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>']
      }
    }
    providers: {
      azure: {
        scope: '/subscriptions/<sub-id>/resourceGroups/<rg-name>'
      }
    }
  }
}
```

### Required IAM Roles for ACI Managed Identity
- **Contributor** on the subscription
- **Azure Container Instances Contributor** on the resource group

---

## Option 2: Full Private AKS with Radius (Recommended for Production-like POC)

### Prerequisites

```bash
# Set variables
LOCATION="eastus2"
RG_NAME="aks-radius-poc-rg"
VNET_NAME="aks-vnet"
AKS_NAME="aks-private-radius"
KV_NAME="kv-aks-poc-$(openssl rand -hex 4)"
ACR_NAME="acrradius$(openssl rand -hex 4)"
BASTION_NAME="aks-bastion"

# Create resource group
az group create --name $RG_NAME --location $LOCATION
```

---

## Step 1: Deploy Virtual Network with NSG and Subnets

### Understanding Service Tags vs Application Security Groups

| Approach | Use Case | Can Create Custom? |
|----------|----------|-------------------|
| **Service Tags** | Azure-managed IP prefixes for Azure services | ❌ No - Microsoft-managed only |
| **Application Security Groups (ASGs)** | Logical grouping of your resources | ✅ Yes - You create and manage |
| **IP/CIDR Ranges** | Specific IP addresses | ✅ Yes - Manual management |

### Available Service Tags for AKS

| Service Tag | Direction | Purpose |
|------------|-----------|---------|
| `AzureCloud.<Region>` | Outbound | All Azure IPs in region (includes AKS control plane) |
| `AzureContainerRegistry` | Outbound | Pull images from ACR |
| `AzureKeyVault` | Outbound | Access certificates/secrets |
| `AzureMonitor` | Outbound | Metrics and logs |
| `Storage.<Region>` | Outbound | Azure Storage access |
| `AzureActiveDirectory` | Outbound | AAD authentication |

### Bicep Template: `infra/nsg.bicep`

```bicep
@description('Location for all resources')
param location string = resourceGroup().location

@description('Environment name for tagging')
param environment string = 'poc'

// Application Security Group for AKS nodes
resource aksNodesAsg 'Microsoft.Network/applicationSecurityGroups@2023-05-01' = {
  name: 'asg-aks-nodes'
  location: location
  tags: {
    Environment: environment
    Purpose: 'AKS Node Pool Security Group'
  }
}

// Application Security Group for Jump VMs
resource jumpVmAsg 'Microsoft.Network/applicationSecurityGroups@2023-05-01' = {
  name: 'asg-jump-vms'
  location: location
  tags: {
    Environment: environment
    Purpose: 'Jump VM Security Group'
  }
}

// NSG for AKS Subnet
resource aksNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'nsg-aks-subnet'
  location: location
  properties: {
    securityRules: [
      // Inbound Rules
      {
        name: 'AllowBastionToAKS'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.0.3.0/26'  // Bastion subnet
          sourcePortRange: '*'
          destinationApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          destinationPortRanges: ['22', '443']
          description: 'Allow Bastion to access AKS nodes'
        }
      }
      {
        name: 'AllowAPIServerToNodes'
        properties: {
          priority: 110
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.0.2.0/28'  // API Server subnet
          sourcePortRange: '*'
          destinationApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          destinationPortRange: '*'
          description: 'Allow API Server to AKS nodes'
        }
      }
      {
        name: 'AllowAzureLoadBalancer'
        properties: {
          priority: 120
          direction: 'Inbound'
          access: 'Allow'
          protocol: '*'
          sourceAddressPrefix: 'AzureLoadBalancer'  // Service Tag
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
          description: 'Allow Azure Load Balancer health probes'
        }
      }
      {
        name: 'AllowVNetInbound'
        properties: {
          priority: 130
          direction: 'Inbound'
          access: 'Allow'
          protocol: '*'
          sourceAddressPrefix: 'VirtualNetwork'  // Service Tag
          sourcePortRange: '*'
          destinationAddressPrefix: 'VirtualNetwork'
          destinationPortRange: '*'
          description: 'Allow VNet internal traffic'
        }
      }
      {
        name: 'DenyAllInbound'
        properties: {
          priority: 4096
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '*'
          description: 'Deny all other inbound traffic'
        }
      }
      // Outbound Rules
      {
        name: 'AllowAzureCloudOutbound'
        properties: {
          priority: 100
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzureCloud.EastUS2'  // Regional Service Tag
          destinationPortRanges: ['443', '9000', '1194']
          description: 'Allow AKS nodes to Azure services'
        }
      }
      {
        name: 'AllowACROutbound'
        properties: {
          priority: 110
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzureContainerRegistry'  // Service Tag
          destinationPortRange: '443'
          description: 'Allow AKS nodes to pull from ACR'
        }
      }
      {
        name: 'AllowKeyVaultOutbound'
        properties: {
          priority: 120
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzureKeyVault'  // Service Tag
          destinationPortRange: '443'
          description: 'Allow AKS nodes to access Key Vault'
        }
      }
      {
        name: 'AllowAzureMonitorOutbound'
        properties: {
          priority: 130
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzureMonitor'  // Service Tag
          destinationPortRange: '443'
          description: 'Allow AKS nodes to send telemetry'
        }
      }
      {
        name: 'AllowStorageOutbound'
        properties: {
          priority: 140
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'Storage.EastUS2'  // Regional Service Tag
          destinationPortRange: '443'
          description: 'Allow AKS nodes to access Azure Storage'
        }
      }
      {
        name: 'AllowAADOutbound'
        properties: {
          priority: 150
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'AzureActiveDirectory'  // Service Tag
          destinationPortRange: '443'
          description: 'Allow AKS nodes to authenticate with AAD'
        }
      }
      {
        name: 'AllowVNetOutbound'
        properties: {
          priority: 160
          direction: 'Outbound'
          access: 'Allow'
          protocol: '*'
          sourceAddressPrefix: 'VirtualNetwork'
          sourcePortRange: '*'
          destinationAddressPrefix: 'VirtualNetwork'
          destinationPortRange: '*'
          description: 'Allow VNet internal traffic'
        }
      }
      {
        name: 'AllowInternetHTTPS'
        properties: {
          priority: 200
          direction: 'Outbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceApplicationSecurityGroups: [
            { id: aksNodesAsg.id }
          ]
          sourcePortRange: '*'
          destinationAddressPrefix: 'Internet'
          destinationPortRanges: ['80', '443']
          description: 'Allow AKS nodes to access internet (MCR, packages)'
        }
      }
    ]
  }
}

// NSG for API Server Subnet
resource apiServerNsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'nsg-apiserver-subnet'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowAKSNodesToAPIServer'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: '10.0.1.0/24'  // AKS subnet
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRanges: ['443', '4443']
          description: 'Allow AKS nodes to API server'
        }
      }
      {
        name: 'AllowAzureLoadBalancerToAPIServer'
        properties: {
          priority: 110
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourceAddressPrefix: 'AzureLoadBalancer'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '9988'
          description: 'Allow Azure LB health probes to API server'
        }
      }
    ]
  }
}

output aksNsgId string = aksNsg.id
output apiServerNsgId string = apiServerNsg.id
output aksNodesAsgId string = aksNodesAsg.id
output jumpVmAsgId string = jumpVmAsg.id
```

### Bicep Template: `infra/vnet.bicep` (Updated with NSG References)

```bicep
@description('Location for all resources')
param location string = resourceGroup().location

@description('VNet address prefix')
param vnetAddressPrefix string = '10.0.0.0/16'

@description('AKS subnet prefix')
param aksSubnetPrefix string = '10.0.1.0/24'

@description('API Server subnet prefix')
param apiServerSubnetPrefix string = '10.0.2.0/28'

@description('Bastion subnet prefix')
param bastionSubnetPrefix string = '10.0.3.0/26'

@description('Private endpoints subnet prefix')
param peSubnetPrefix string = '10.0.4.0/24'

@description('AKS NSG resource ID')
param aksNsgId string

@description('API Server NSG resource ID')
param apiServerNsgId string

resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: 'aks-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [vnetAddressPrefix]
    }
    subnets: [
      {
        name: 'aks-subnet'
        properties: {
          addressPrefix: aksSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
          networkSecurityGroup: {
            id: aksNsgId  // Associate AKS NSG with service tags
          }
        }
      }
      {
        name: 'apiserver-subnet'
        properties: {
          addressPrefix: apiServerSubnetPrefix
          networkSecurityGroup: {
            id: apiServerNsgId  // Associate API Server NSG
          }
          delegations: [
            {
              name: 'aks-delegation'
              properties: {
                serviceName: 'Microsoft.ContainerService/managedClusters'
              }
            }
          ]
        }
      }
      {
        name: 'AzureBastionSubnet'  // Must be this exact name - Bastion manages its own NSG
        properties: {
          addressPrefix: bastionSubnetPrefix
        }
      }
      {
        name: 'pe-subnet'
        properties: {
          addressPrefix: peSubnetPrefix
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

output vnetId string = vnet.id
output aksSubnetId string = vnet.properties.subnets[0].id
output apiServerSubnetId string = vnet.properties.subnets[1].id
output bastionSubnetId string = vnet.properties.subnets[2].id
output peSubnetId string = vnet.properties.subnets[3].id
```

---

## Step 2: Deploy Azure Bastion

### Bicep Template: `infra/bastion.bicep`

```bicep
@description('Location for all resources')
param location string = resourceGroup().location

@description('Bastion subnet ID')
param bastionSubnetId string

resource bastionPip 'Microsoft.Network/publicIPAddresses@2023-05-01' = {
  name: 'bastion-pip'
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

resource bastion 'Microsoft.Network/bastionHosts@2023-05-01' = {
  name: 'aks-bastion'
  location: location
  sku: {
    name: 'Standard'  // Required for native client support
  }
  properties: {
    enableTunneling: true  // Enables native client tunneling for kubectl
    ipConfigurations: [
      {
        name: 'ipconfig'
        properties: {
          publicIPAddress: {
            id: bastionPip.id
          }
          subnet: {
            id: bastionSubnetId
          }
        }
      }
    ]
  }
}

output bastionId string = bastion.id
```

---

## Step 3: Deploy Key Vault with Self-Signed Certificate

### Bicep Template: `infra/keyvault.bicep`

```bicep
@description('Location for all resources')
param location string = resourceGroup().location

@description('Key Vault name')
param keyVaultName string

@description('Object ID of the user/identity for access')
param objectId string

@description('Tenant ID')
param tenantId string = subscription().tenantId

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenantId
    enableRbacAuthorization: true
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Enabled'  // For POC; use Private Endpoint in prod
  }
}

// Grant Key Vault Administrator role
resource kvAdminRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, objectId, 'Key Vault Administrator')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '00482a5a-887f-4fb3-b363-3b7fe8e74483')
    principalId: objectId
    principalType: 'User'
  }
}

output keyVaultId string = keyVault.id
output keyVaultUri string = keyVault.properties.vaultUri
output keyVaultName string = keyVault.name
```

### Create Self-Signed Certificate

```powershell
# PowerShell - Create self-signed certificate in Key Vault

$keyVaultName = "<your-kv-name>"
$certName = "aks-poc-cert"

# Create certificate policy
$policy = New-AzKeyVaultCertificatePolicy `
    -SubjectName "CN=aks-poc.local" `
    -IssuerName "Self" `
    -ValidityInMonths 12 `
    -KeyType "RSA" `
    -KeySize 2048 `
    -SecretContentType "application/x-pkcs12"

# Create certificate
Add-AzKeyVaultCertificate `
    -VaultName $keyVaultName `
    -Name $certName `
    -CertificatePolicy $policy
```

Or via Azure CLI:
```bash
# Create self-signed certificate
az keyvault certificate create \
    --vault-name $KV_NAME \
    --name aks-poc-cert \
    --policy "$(az keyvault certificate get-default-policy)"
```

---

## Step 4: Deploy Private AKS Cluster

### Bicep Template: `infra/aks.bicep` (with ASG Support)

```bicep
@description('Location for all resources')
param location string = resourceGroup().location

@description('AKS cluster name')
param clusterName string

@description('AKS subnet ID')
param aksSubnetId string

@description('API Server subnet ID')
param apiServerSubnetId string

@description('Application Security Group ID for AKS nodes')
param aksNodesAsgId string = ''

@description('Kubernetes version')
param kubernetesVersion string = '1.29'

@description('Node count')
param nodeCount int = 3

@description('Node VM size')
param nodeVmSize string = 'Standard_D4s_v3'

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${clusterName}-identity'
  location: location
}

resource aks 'Microsoft.ContainerService/managedClusters@2024-01-01' = {
  name: clusterName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    kubernetesVersion: kubernetesVersion
    dnsPrefix: clusterName
    
    // Private cluster configuration
    apiServerAccessProfile: {
      enablePrivateCluster: true
      enablePrivateClusterPublicFQDN: false
      enableVnetIntegration: true
      subnetId: apiServerSubnetId
    }
    
    // Network configuration
    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'azure'
      serviceCidr: '10.1.0.0/16'
      dnsServiceIP: '10.1.0.10'
      loadBalancerSku: 'standard'
      outboundType: 'loadBalancer'
    }
    
    agentPoolProfiles: [
      {
        name: 'systempool'
        count: nodeCount
        vmSize: nodeVmSize
        mode: 'System'
        osType: 'Linux'
        vnetSubnetID: aksSubnetId
        enableAutoScaling: true
        minCount: 1
        maxCount: 5
      }
    ]
    
    // Security
    aadProfile: {
      managed: true
      enableAzureRBAC: true
    }
    
    // Monitoring
    addonProfiles: {
      omsagent: {
        enabled: true
        config: {}
      }
    }
  }
}

output aksId string = aks.id
output aksName string = aks.name
output aksFqdn string = aks.properties.privateFQDN
output identityId string = managedIdentity.id
output identityClientId string = managedIdentity.properties.clientId
```

### Deploy via CLI (with ASG Support)

```bash
# Create private AKS cluster with VNet integration and ASG
az aks create \
    --name $AKS_NAME \
    --resource-group $RG_NAME \
    --location $LOCATION \
    --network-plugin azure \
    --vnet-subnet-id "<aks-subnet-id>" \
    --enable-private-cluster \
    --enable-apiserver-vnet-integration \
    --apiserver-subnet-id "<apiserver-subnet-id>" \
    --enable-managed-identity \
    --enable-aad \
    --enable-azure-rbac \
    --node-count 3 \
    --node-vm-size Standard_D4s_v3 \
    --nodepool-asg-ids "<asg-aks-nodes-id>" \
    --generate-ssh-keys

# Or add ASG to existing node pool
az aks nodepool update \
    --resource-group $RG_NAME \
    --cluster-name $AKS_NAME \
    --name systempool \
    --asg-ids "<asg-aks-nodes-id>"
```

### Service Tags Quick Reference for AKS

When configuring NSG rules for AKS, use these service tags:

| Outbound Service Tag | Purpose | Required Ports |
|---------------------|---------|----------------|
| `AzureCloud.<Region>` | AKS control plane communication | 443, 9000, 1194 |
| `AzureContainerRegistry` | Pull container images | 443 |
| `AzureKeyVault` | Access secrets/certs | 443 |
| `AzureMonitor` | Telemetry and logging | 443 |
| `AzureActiveDirectory` | Authentication | 443 |
| `Storage.<Region>` | Persistent volumes, logs | 443 |

---

## Step 5: Connect via Bastion

### Option A: Bastion Native Client Tunneling (Preview)

```bash
# Install Azure CLI Bastion extension
az extension add --name bastion

# Get AKS credentials
az aks get-credentials --resource-group $RG_NAME --name $AKS_NAME

# Connect via Bastion tunnel
az network bastion tunnel \
    --name $BASTION_NAME \
    --resource-group $RG_NAME \
    --target-resource-id "<aks-cluster-id>" \
    --resource-port 443 \
    --port 6443

# In another terminal, use kubectl with the tunnel
kubectl get nodes
```

### Option B: Jump VM in VNet

```bash
# Create jump VM in AKS VNet
az vm create \
    --resource-group $RG_NAME \
    --name aks-jumpbox \
    --image Ubuntu2204 \
    --vnet-name $VNET_NAME \
    --subnet aks-subnet \
    --admin-username azureuser \
    --generate-ssh-keys \
    --size Standard_B2ms

# Connect via Bastion to Jump VM
az network bastion ssh \
    --name $BASTION_NAME \
    --resource-group $RG_NAME \
    --target-resource-id "<vm-resource-id>" \
    --auth-type ssh-key \
    --username azureuser \
    --ssh-key ~/.ssh/id_rsa
```

---

## Step 6: Install Radius on AKS

### Install Radius CLI

```powershell
# Windows
iwr -useb "https://get.radapp.io/tools/rad/install.ps1" | iex
```

```bash
# Linux/macOS
curl -fsSL "https://get.radapp.io/tools/rad/install.sh" | /bin/bash
```

### Install Radius on Cluster

```bash
# From jump VM or via Bastion tunnel

# Install Radius
rad install kubernetes

# Verify installation
kubectl get pods -n radius-system

# Initialize Radius with Azure provider
rad init

# Register Azure credentials
rad credential register azure sp \
    --client-id <app-id> \
    --client-secret <secret> \
    --tenant-id <tenant-id>

# Or use Workload Identity (recommended)
rad credential register azure wi \
    --client-id <managed-identity-client-id> \
    --tenant-id <tenant-id>
```

### Create Radius Environment

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
        scope: '/subscriptions/<sub-id>/resourceGroups/${RG_NAME}'
      }
    }
  }
}
```

```bash
rad deploy environments/dev.bicep
rad env switch dev
```

---

## Step 7: Deploy Sample Application with Radius

### Sample Application: `app.bicep`

```bicep
import radius as radius

@description('The Radius environment')
param environment string

resource app 'Applications.Core/applications@2023-10-01-preview' = {
  name: 'demo-app'
  properties: {
    environment: environment
  }
}

resource frontend 'Applications.Core/containers@2023-10-01-preview' = {
  name: 'frontend'
  properties: {
    application: app.id
    container: {
      image: 'nginx:latest'
      ports: {
        web: {
          containerPort: 80
        }
      }
    }
  }
}

resource gateway 'Applications.Core/gateways@2023-10-01-preview' = {
  name: 'gateway'
  properties: {
    application: app.id
    routes: [
      {
        path: '/'
        destination: 'http://frontend:80'
      }
    ]
  }
}
```

```bash
# Deploy application
rad deploy app.bicep -e dev

# View application graph
rad app graph demo-app

# Get application status
rad app status demo-app
```

---

## Complete Deployment Script

```bash
#!/bin/bash
set -e

# Variables
LOCATION="eastus2"
RG_NAME="aks-radius-poc-rg"
UNIQUE_SUFFIX=$(openssl rand -hex 4)
KV_NAME="kv-poc-${UNIQUE_SUFFIX}"
AKS_NAME="aks-private-radius"

# 1. Create resource group
az group create --name $RG_NAME --location $LOCATION

# 2. Deploy infrastructure
az deployment group create \
    --resource-group $RG_NAME \
    --template-file infra/main.bicep \
    --parameters keyVaultName=$KV_NAME aksName=$AKS_NAME

# 3. Get AKS credentials
az aks get-credentials --resource-group $RG_NAME --name $AKS_NAME --admin

# 4. Create self-signed certificate
az keyvault certificate create \
    --vault-name $KV_NAME \
    --name aks-poc-cert \
    --policy "$(az keyvault certificate get-default-policy)"

# 5. Install Radius
rad install kubernetes

# 6. Initialize and configure Radius
rad init --full

echo "POC deployment complete!"
echo "Connect via Bastion to access the private cluster"
```

---

## Radius on ACI Alternative (Simpler POC)

If you want to skip the full AKS setup for initial testing, you can use Radius with ACI:

```bash
# 1. Create minimal K8s cluster for Radius control plane (can use AKS or local)
# 2. Install Radius
rad install kubernetes

# 3. Create ACI-targeted environment
cat > aci-env.bicep << 'EOF'
resource env 'Applications.Core/environments@2023-10-01-preview' = {
  name: 'aci-poc'
  properties: {
    compute: {
      kind: 'aci'
      resourceGroup: '/subscriptions/<sub>/resourceGroups/<rg>'
      identity: {
        kind: 'userAssigned'
        managedIdentity: ['<managed-identity-id>']
      }
    }
    providers: {
      azure: {
        scope: '/subscriptions/<sub>/resourceGroups/<rg>'
      }
    }
  }
}
EOF

rad deploy aci-env.bicep

# 4. Deploy apps to ACI
rad deploy app.bicep -e aci-poc
```

---

## Testing & Validation Checklist

- [ ] VNet deployed with correct subnets
- [ ] Private AKS cluster created and accessible via Bastion
- [ ] Key Vault deployed with self-signed certificate
- [ ] Bastion can tunnel to AKS API server
- [ ] Radius installed and running in `radius-system` namespace
- [ ] Azure credentials registered with Radius
- [ ] Sample application deployed and accessible
- [ ] Certificate can be retrieved from Key Vault

---

## References

- [AKS Private Cluster](https://learn.microsoft.com/en-us/azure/aks/private-clusters)
- [Connect to Private AKS via Bastion](https://learn.microsoft.com/en-us/azure/bastion/bastion-connect-to-aks-private-cluster)
- [Radius on ACI](https://techcommunity.microsoft.com/blog/azurecompute/use-radius-to-deploy-your-applications-to-azure-container-instances/4428551)
- [Radius Documentation](https://docs.radapp.io/)
- [Azure Key Vault Certificates](https://learn.microsoft.com/en-us/azure/key-vault/certificates/quick-create-portal)
