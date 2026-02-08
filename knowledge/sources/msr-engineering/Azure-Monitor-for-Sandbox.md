# Introduction

This is our monitoring service for sandbox. 

Its initial purpose is to reduce toil with the operationalization effort for the GPUMetrics agent. This checks that GPU Drivers are working and other considerations, in order to eliminate toil from people needing to log into many systems and diagnose the issue.

It consists of the following components:

- Azure Monitor Agent (AMA)
  - This is the agent, instaled by Azure extension that gathers information from the host and sends it to a specified location.
- Data Collection Rule (DCR)
  - This is where hosts are configured to be associated with, and these hold the configurations of what data is to be gathered from the host. A host can be associated with more than one DCR.
- Log Analytics Workspace (LAW)
  - This is the point where information is stored. The data is stored in tables which can be queried with Kusto (aka KQL).
- Grafana
  - This is the visualization/dashboard portion of the alert and metrics monitoring. 

![azmon-sandbox.drawio.png](/.attachments/azmon-sandbox.drawio-e9f2bef4-b924-4f5b-9c8e-603d2b94267f.png)


## Overview
- **Agent Install** - All hosts have an Azure Monitor Agent installed via an Azure extension
  - These are kept up to date with Azure Policy. There are 5 polices, one for each Resource Group, which ensure that Azure Monitor is installed on the hosts in scope.
  - These policies insure:
    - That Azure Monitoring Agent is installed
    - That each host is associated with the appropriate Data Collection Rule
    - [Policy GCR Arc/GPU Sandbox Policy -> azmon-sandbox-arc-dcr](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyComplianceDetail.ReactView/assignmentId/%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7%2Fresourcegroups%2Fgpu-sandbox%2Fproviders%2Fmicrosoft.authorization%2Fpolicyassignments%2F909b9b9f01ef4a368f3e927f/scopes~/%5B%22%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7%22%2C%22%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%22%2C%22%2Fsubscriptions%2F84ed0d97-78a4-44d4-b12f-c977bf141102%22%5D/policyDefinitionId/%2Fproviders%2Fmicrosoft.authorization%2Fpolicydefinitions%2Fd5c37ce1-5f52-4523-b949-f19bf945b73a)
    - [Policy GCRProdEx2/GPU-Sandbox -> azmon-sandbox-dcr](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyComplianceDetail.ReactView/assignmentId/%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%2Fresourcegroups%2Fgpu-sandbox%2Fproviders%2Fmicrosoft.authorization%2Fpolicyassignments%2Fae3f8b4a4ec841749da7d9a2/scopes~/%5B%22%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7%22%2C%22%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%22%2C%22%2Fsubscriptions%2F84ed0d97-78a4-44d4-b12f-c977bf141102%22%5D/policyDefinitionId/%2Fproviders%2Fmicrosoft.authorization%2Fpolicydefinitions%2F2ea82cdd-f2e8-4500-af75-67a2e084ca74)
    - [Policy GCRProdEx2/GPU-Sandbox1 -> azmon-sandbox-dcr](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyComplianceDetail.ReactView/assignmentId/%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%2Fresourcegroups%2Fgpu-sandbox1%2Fproviders%2Fmicrosoft.authorization%2Fpolicyassignments%2Faec103cd9f3a4254baca6974/scopes~/%5B%22%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7%22%2C%22%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%22%2C%22%2Fsubscriptions%2F84ed0d97-78a4-44d4-b12f-c977bf141102%22%5D/policyDefinitionId/%2Fproviders%2Fmicrosoft.authorization%2Fpolicydefinitions%2F2ea82cdd-f2e8-4500-af75-67a2e084ca74)
    - [Policy GCRProdEx2/GPU-Sandbox2 -> azmon-sandbox-dcr](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyComplianceDetail.ReactView/assignmentId/%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%2Fresourcegroups%2Fgpu-sandbox2%2Fproviders%2Fmicrosoft.authorization%2Fpolicyassignments%2F43f19f5a715e4bb5a9e6d04d/scopes~/%5B%22%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7%22%2C%22%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%22%2C%22%2Fsubscriptions%2F84ed0d97-78a4-44d4-b12f-c977bf141102%22%5D/policyDefinitionId/%2Fproviders%2Fmicrosoft.authorization%2Fpolicydefinitions%2F2ea82cdd-f2e8-4500-af75-67a2e084ca74)
    - [Policy GCRProdEx2/GPU-Sandbox3 -> azmon-sandbox-dcr](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyComplianceDetail.ReactView/assignmentId/%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%2Fresourcegroups%2Fgpu-sandbox3%2Fproviders%2Fmicrosoft.authorization%2Fpolicyassignments%2F4c46284930004688a04fe5a0/scopes~/%5B%22%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7%22%2C%22%2Fsubscriptions%2F46da6261-2167-4e71-8b0d-f4a45215ce61%22%2C%22%2Fsubscriptions%2F84ed0d97-78a4-44d4-b12f-c977bf141102%22%5D/policyDefinitionId/%2Fproviders%2Fmicrosoft.authorization%2Fpolicydefinitions%2F2ea82cdd-f2e8-4500-af75-67a2e084ca74)
- **Agent Configuration** - Each DCR holds configuration to gather certain metrics for each AMA attached to it.
- **Data Shipment** - The AMA, matching the configuration of the DCR is associated with, will send the appropriate data to the LAW in the form of tables. This goes for data like syslog and for metrics data, if that's configured.
- **Alerts** - All alerts are configured as a log based alert, where a search is made on the LAW, and if conditions are met, they will trigger an alert.
- **Dashboarding** - All dashboards are in a managed Grafana instance. 

## SLO/SLI/KVI

The following are definitions of SLO/SLI and KVI. No actual metrics are available for this service currently.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal; color: inherit;">• Ensure that the dashboard for metrics shows up to date data 99% of the time.<br> • Ensure under 10 false positives a week </span>|
| --- | --- |
| SLI |  |
| KVI | • Number of hosts using the service.<br>• Number of checks used. |

## Resource Locations
All resources are in the [SES Monitoring](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/overview) subscription.
- [azmon-sandbox Resource Group](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/overview)
  - Where the alerts, Data Collection Rules (DCR), Data Collection Endpoint (DCE), Log Analytics Workspace (LAW) for VMs are stored. The Grafana instance is also here.
- [azmon-sandbox-arc Resource Group](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/overview)
  - Where the alerts, Data Collection Rules (DCR), Data Collection Endpoint (DCE), Log Analytics Workspace (LAW) for Arc instances are stored. 
- [Azure Monitor for Sandbox Dashboard](https://azmon-sandbox-emetebfkh4cyasft.wus2.grafana.azure.com/d/be3yo8b9c6rcwe/azure-alert-consumption?orgId=1&var-mc=Fired&var-as=New&var-sev=Sev0&var-sev=Sev1&var-sev=Sev2)
  - The dashboard showing current issues and sandbox metrics

**SLO** - 
**SLI** - The dashboard availability would be fairly simple. I think Azure has this out of the box For false positives, need to log this more manually. Perhaps through ADO reporting.
**KVI** - Uncertain if we can figure out the dashboards used by this, or the number access times of the dashboards connected to this service.

# Check Standard

The checks themselves conform to the [Nagios Plugin return code standard](https://nagios-plugins.org/doc/guidelines.html#AEN78), so checks from Nagios or Sensu can be reused with our Azure Monitor system.

The following is required for the check output:
- Each check must output an exit code:
  - 0 for OK
  - 1 for Unknown
  - 2 for Error
- The output must be in the form of:
`NAME_CHECK STATUS - Check Log Data`
Some examples:
`CHECK_GPUMETRICS OK - All Checks are OK`
`CHECK_GPUMETRICS WARNING - There is a problem with the GPU`
`CHECK_GPUMETRICS CRITICAL - The GPU is in danger of exploding`

The output must be one line only with the formatting above, otherwise unpredictable things may happen with the logging.

### Scope
Our current Scope consists of the following:
| Subscription Name | Subscription ID |Resource Group |
|-|-|-|
|GCR Arc | 46e0b8e9-eb7f-4bbf-af34-a502c2d310f7  | [GPU-Sandbox](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/GPU-Sandbox/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox1](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox1/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox2](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox2/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox3/overview)

## Additional Topics
- [Agent](/Team-Pages/SES/Service-Management/Services/Azure-Monitor-for-Sandbox/Azure-Monitor-for-Sandbox-%2D-Agent)
- [Dashbord](/Team-Pages/SES/Service-Management/Services/Azure-Monitor-for-Sandbox/Azure-Monitor-for-Sandbox-%2D-Dashboard)
- [Alert Creation](/Team-Pages/SES/Service-Management/Services/Azure-Monitor-for-Sandbox/Azure-Monitor-for-Sandbox-%2D-Alert-Creation)
