# Introduction

The Kubernetes GPU Metrics Gather service provides automated collection, processing, and ingestion of GPU metrics from Kubernetes clusters into Azure Log Analytics. This service addresses critical challenges around GPU monitoring in enterprise Kubernetes environments, specifically solving Docker Hub rate limiting issues that prevented reliable metrics collection at scale.

This service evolved from traditional pod-based monitoring approaches to an innovative port-forward methodology that eliminates container image pull dependencies while maintaining comprehensive GPU telemetry coverage.

## SLO/SLI/KVI

| **SLO** | **Ensure GPU metrics collection occurs every 10 minutes with >95% reliability.** Maintain <5% collection failure rate during normal operations. Complete metrics ingestion to Log Analytics within 2 minutes of collection. Support flexible collection frequency scaling (1-60 minute intervals). |
| --- | --- |
| **SLI** | Collection success rate measured via Azure Container Instance execution logs. Log Analytics ingestion latency tracked via Azure Monitor. Port-forward connection reliability monitored through application logs. |
| **KVI** | Number of GPU nodes monitored: Currently targeting B200 cluster infrastructure. Metrics volume: ~8 GPUs per node, multiple metrics per GPU every 10 minutes. Dashboard usage: [GPU Metrics Dashboard](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.OperationalInsights/workspaces/kmg-law-kadahk4i7rtmm/logs) for visualization and analysis. |

## Overview

This service uses the following components:

- **Azure Container Instance (ACI)** - Executes GPU metrics collection scripts in a managed environment
- **kubectl port-forward** - Establishes secure connection to cluster Prometheus without pod creation
- **Python Ingestion Pipeline** - Processes, validates, and batches metrics for optimal Log Analytics ingestion
- **Logic App Scheduler** - Provides automated 10-minute interval triggering with managed identity authentication
- **Log Analytics Workspace** - Stores GPU metrics in structured format for querying and analysis
- **Application Insights** - Provides comprehensive monitoring and alerting for the collection process

### Key Innovation: Port-Forward Approach

The service's core innovation eliminates Docker Hub rate limiting through `kubectl port-forward` instead of creating monitoring pods:

:::mermaid
graph TD
    A[Logic App Trigger] --> B[ACI Activation]
    B --> C[kubectl port-forward to Prometheus]
    C --> D[GPU Metrics Collection]
    D --> E[Data Validation & Processing]
    E --> F[Batch Ingestion to Log Analytics]
    F --> G[Monitoring & Alerting]
:::

This approach provides:

- **Zero Docker Hub Dependencies**: No container pulls required
- **Secure Authentication**: User Assigned Managed Identity for all Azure operations
- **Flexible Scaling**: Easy frequency adjustment from 1-60 minute intervals
- **Comprehensive Monitoring**: Full observability of collection pipeline

## Architecture Components

### Data Collection Pipeline
1. **Logic App Triggers ACI**: Every 10 minutes (configurable)
2. **Port-Forward Establishment**: `kubectl port-forward -n cattle-monitoring-system svc/rancher-monitoring-prometheus 9090:9090`
3. **Prometheus Query Execution**: Collects GPU utilization, memory, temperature, and power metrics
4. **Schema Validation**: Ensures data conforms to Log Analytics table structure
5. **Batch Processing**: Groups metrics for optimal ingestion performance
6. **Log Analytics Ingestion**: Uses Azure Monitor Ingestion API with managed identity

### Security Architecture
- **Network Isolation**: VNet with private endpoints for all storage and Key Vault access
- **Identity-Based Authentication**: No shared keys or SAS tokens
- **Private DNS Resolution**: Secure endpoint resolution within VNet
- **RBAC Enforcement**: Principle of least privilege access patterns
- **TLS 1.2 Minimum**: All communications encrypted

## Deployment

### Scope
This service targets Kubernetes clusters with:
- **GPU Infrastructure**: NVIDIA GPU-enabled nodes with DCGM metrics
- **Prometheus Monitoring**: Rancher Monitoring stack in `cattle-monitoring-system` namespace
- **Network Accessibility**: ACI must have kubectl access to target cluster
- **Resource Coverage**: Currently focused on B200 cluster infrastructure

### Resource Requirements
- **Azure Container Instance**: 1-2 CPU cores, 2-4GB RAM
- **Network Bandwidth**: Minimal during collection windows (~100KB per collection cycle)
- **Storage**: Log Analytics workspace with 30-day retention
- **Identity Permissions**: Contributor access to resource group for ACI management

## Resource Locations

- All resources are deployed in the [k8s-gpumetrics-gather Resource Group](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/overview) in the **westus3** region.
- Kuberenetes user setup artifacts can be found in the [gcrk8sconfigs](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcrk8sconfigs?path=/users/k-monu) repo.

### Core Infrastructure
- **Resource Group**: [k8s-gpumetrics-gather](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/overview)
- **Virtual Network**: [kmg-vnet](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/virtualNetworks/kmg-vnet) - Network isolation with dedicated subnets
- **Storage Account**: [kmgsakadahk4i7rtmm](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Storage/storageAccounts/kmgsakadahk4i7rtmm) - Secure storage with private endpoint
- **Key Vault**: [kmg-kv-kadahk4i7rtmm](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.KeyVault/vaults/kmg-kv-kadahk4i7rtmm) - Secret management with RBAC
- **Managed Identity**: [kmg-uami](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.ManagedIdentity/userAssignedIdentities/kmg-uami) - Authentication for all Azure operations
- **NAT Gateway**: [kmg-natgw](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/natGateways/kmg-natgw) - Controlled outbound connectivity

### Collection & Monitoring Infrastructure
- **Container Instance**: [kmg-aci-b200](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.ContainerInstance/containerGroups/kmg-aci-b200) - Metrics collection execution environment
- **Logic App**: [kmg-aci-scheduler](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Logic/workflows/kmg-aci-scheduler) - Automated scheduling and orchestration
- **Log Analytics Workspace**: [kmg-law-kadahk4i7rtmm](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.OperationalInsights/workspaces/kmg-law-kadahk4i7rtmm) - 30-day retention, Customer ID: 74d8bfc3-1a88-4d9e-b0d1-ebabb0b42353
- **Application Insights**: [kmg-ai-kadahk4i7rtmm](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Insights/components/kmg-ai-kadahk4i7rtmm) - Performance monitoring and alerting

### Security Infrastructure
- **Private DNS Zones**:
  - [privatelink.blob.core.windows.net](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net) - Storage account resolution
  - [privatelink.vault.azure.net](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/privateDnsZones/privatelink.vault.azure.net) - Key Vault management plane
  - [privatelink.vaultcore.azure.net](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net) - Key Vault data plane
- **Private Endpoints**:
  - [kmg-sa-pe](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/privateEndpoints/kmg-sa-pe) - Storage account private access
  - [kmg-kv-pe](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Network/privateEndpoints/kmg-kv-pe) - Key Vault private access

## Monitoring & Operations

### Azure CLI Commands for Management

```bash
# View service health and recent executions
az container logs --resource-group k8s-gpumetrics-gather --name kmg-aci-b200

# Check Logic App execution history
az logic workflow show --resource-group k8s-gpumetrics-gather --name kmg-aci-scheduler --query "state"

# Monitor Log Analytics ingestion
az monitor log-analytics query --workspace 74d8bfc3-1a88-4d9e-b0d1-ebabb0b42353 --analytics-query "b200_gpumetrics_CL | summarize count() by bin(TimeGenerated, 10m) | order by TimeGenerated desc"

# Container instance operations
az container restart --resource-group k8s-gpumetrics-gather --name kmg-aci-b200
az container exec --resource-group k8s-gpumetrics-gather --name kmg-aci-b200 --exec-command '/bin/bash'

# Logic App control
az resource update --ids "/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Logic/workflows/kmg-aci-scheduler" --set properties.state=Disabled
az resource update --ids "/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/k8s-gpumetrics-gather/providers/Microsoft.Logic/workflows/kmg-aci-scheduler" --set properties.state=Enabled
```

### Log Analytics Queries

```kusto
// GPU utilization trends
b200_gpumetrics_CL
| where TimeGenerated > ago(1h)
| summarize avg(GPUUtilization) by bin(TimeGenerated, 5m), NodeName, GPU
| render timechart

// Collection health monitoring
b200_gpumetrics_CL
| summarize LastCollection=max(TimeGenerated) by NodeName
| where LastCollection < ago(15m)
| project NodeName, LastCollection, AlertMessage="Missing GPU metrics"

// Memory utilization analysis
b200_gpumetrics_CL
| where TimeGenerated > ago(24h)
| summarize avg(GPUMemoryUsedMiB), avg(GPUMemoryFreeMiB) by NodeName, GPU
| extend MemoryUtilization = round(avg_GPUMemoryUsedMiB / (avg_GPUMemoryUsedMiB + avg_GPUMemoryFreeMiB) * 100, 2)

// Collection error detection
ContainerInstanceLog_CL
| where TimeGenerated > ago(1h) and LogEntry_s contains "ERROR"
| project TimeGenerated, LogEntry_s, Source_s
```

### Performance Metrics

Current service metrics (as of September 2025):
- **Collection Frequency**: Every 10 minutes
- **Average Collection Time**: ~30-45 seconds per cycle
- **Data Volume**: ~100KB per collection cycle
- **Log Analytics Retention**: 30 days
- **Success Rate**: >95% (target >95%)
- **Resource Utilization**: 1 CPU core, 2GB RAM (typical)

## Troubleshooting

### Common Issues and Resolutions

| Issue | Symptoms | Resolution |
|-------|----------|-----------|
| **Port-Forward Connection Timeout** | "Connection refused" in ACI logs | Verify kubectl connectivity and Prometheus service availability |
| **Logic App Not Triggering** | No recent ACI executions | Check Logic App enabled state and ARM connection authentication |
| **Missing GPU Metrics** | Empty collection results | Validate Prometheus has DCGM metrics available |
| **Authentication Failures** | 401/403 errors in logs | Verify managed identity RBAC assignments |
| **Collection Script Failures** | Python ingestion errors | Check Data Collection Endpoint and Rule configuration |

### Debug Commands

```bash
# Interactive debugging session
az container exec --resource-group k8s-gpumetrics-gather --name kmg-aci-b200 --exec-command '/bin/bash'

# Manual collection test (inside container)
cd /home/scripts
source gpu_metrics_env.sh
python3 gpu_metrics_log_ingestion.py

# Check kubectl connectivity (inside container)
kubectl get pods -n cattle-monitoring-system | grep prometheus

# Test port-forward manually (inside container)
kubectl port-forward -n cattle-monitoring-system svc/rancher-monitoring-prometheus 9090:9090 &
curl http://localhost:9090/-/healthy
```

### Escalation Path

1. **Level 1**: Check container logs and Logic App execution history
2. **Level 2**: Validate network connectivity and authentication
3. **Level 3**: Review infrastructure configuration and scaling requirements
4. **Level 4**: Engage Azure support for platform-level issues

## Service Dependencies

### External Dependencies
- **Kubernetes Cluster**: Target cluster must be accessible via kubectl
- **Rancher Monitoring**: Prometheus service in `cattle-monitoring-system` namespace
- **DCGM Metrics**: NVIDIA Data Center GPU Manager must be running on GPU nodes
- **Network Connectivity**: ACI must have outbound internet access for kubectl operations

### Internal Dependencies
- **Azure Resource Manager**: For Logic App and ACI operations
- **Azure Monitor**: For Log Analytics ingestion and Application Insights telemetry
- **Azure Key Vault**: For secure configuration management
- **Azure Storage**: For artifact and log storage

## Disaster Recovery

### Backup Strategy
- **Infrastructure as Code**: Complete Bicep templates stored in repository
- **Configuration Backup**: Environment variables and secrets in Key Vault
- **Log Analytics**: 30-day retention with export capabilities
- **Monitoring History**: Application Insights data for post-incident analysis

### Recovery Procedures
1. **Infrastructure Recreation**: Deploy using stored Bicep templates
2. **Configuration Restoration**: Apply environment variables from Key Vault
3. **Service Validation**: Execute test collection cycle
4. **Monitoring Restoration**: Verify Log Analytics ingestion and alerting

### RTO/RPO Targets
- **Recovery Time Objective (RTO)**: 2 hours for full service restoration
- **Recovery Point Objective (RPO)**: 10 minutes (maximum data loss)

## Cost Management

**Monthly Operational Costs** (estimated):
- **Azure Container Instance**: ~$15/month (intermittent execution)
- **Log Analytics Workspace**: ~$5/month (based on ingestion volume)
- **Logic App**: ~$1/month (standard connector usage)
- **Storage & Networking**: ~$2/month (minimal data transfer)
- **Total Estimated**: ~$25/month

**Cost Optimization Strategies**:
- Use consumption-based ACI billing (pay per execution)
- Optimize Log Analytics retention based on requirements
- Leverage free tiers for Application Insights where applicable

## Additional Resources

### Documentation
- [Service Repository](https://dev.azure.com/msresearch/MSR%20Engineering/_git/k8s-gpumetrics-gather) - Complete infrastructure code and scripts
- [Logic App Integration Guide](/Team-Pages/SES/Service-Management/Services/Kubernetes-GPUMetrics-Gather/Logic-App-Integration)
- [Log Analytics Configuration](/Team-Pages/SES/Service-Management/Services/Kubernetes-GPUMetrics-Gather/Log-Analytics-Configuration)
- [Troubleshooting Guide](/Team-Pages/SES/Service-Management/Services/Kubernetes-GPUMetrics-Gather/Troubleshooting)

### Related Services
- [GPUmetrics-service](/Team-Pages/SES/Service-Management/Services/GPUmetrics-service/GPUmetrics-service) - VM-based GPU monitoring
- [Azure-Monitor-for-Sandbox](/Team-Pages/SES/Service-Management/Services/Azure-Monitor-for-Sandbox/Azure-Monitor-for-Sandbox) - Sandbox environment monitoring

### Support Contacts
- **Primary Support**: GCR Team - [gcradmin@microsoft.com](mailto:gcradmin@microsoft.com)
- **Infrastructure Questions**: Azure Platform Team
- **Kubernetes Integration**: Container Platform Team
