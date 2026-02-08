# Background

Azure is severely constrained on GPUs in all regions. Internal workloads (such as MSR) are being prioritized lower to keep Azure’s 3rd party (paying customers) workloads satisfied.  

With demand constantly outstripping supply, we need a way to ensure that we are consistently using every chip that we own. This is required to help us stay in the running to lead in the AI space, even with a limited investment in hardware.   

This project aligns with Kevin Scott’s strategy document, Beyond the Boundaries. 

This project defines the measurements and KPIs component of the overall GPU Capacity Management Service. 

This service originally was meant to use the Geneva [MetricsExtension](https://eng.ms/docs/products/geneva/getting_started/createmetricsacct) in mid 2019, however we found that Geneva wasn't a good fit for getting the reports we wanted. We then ended up making our own service to capture these metrics.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal; color: inherit;">• Ensure we have >90% coverage on all in-scope hosts.<br> • Ensure a data retention period of 30 days.<br>• Detect host issues within 1 hour of the occurrence.<br> • The monitoring agent should have no more than a 1% false positive rate.</span>|
| --- | --- |
| SLI | Metrics showing the above |
| KVI | • Number of hosts using the service can be found in [this dashboard](https://gpumetricsdashboards-grcfbqgrawd9hca0.wus3.grafana.azure.com/d/eejpgf0thnuo0f/gpumetrics?orgId=1) |



# Overview
 ![==image_0==.jpg](/.attachments/==image_0==-cd26a2e2-22e5-4603-801c-862aba7e8b69.jpg) 
 ![==image_0==.jpg](/.attachments/==image_0==-496b02d5-5408-4139-bf37-eee8c1191d6d.jpg)
 ![==image_0==.jpg](/.attachments/==image_0==-fc572451-94b1-4f90-9664-cb301bc75750.jpg) 
This service uses the following components:
- **Azure Monitor Agent** - To gather metrics from syslog and import into a Log Analytics Workspace
- **Data Collection Rule** - Used to specify which hosts will be connecting to the Log Analytics Workspace
- **Log Analytics Workspace** - Used to store the data
- **Logic Apps** - Used to onboard hosts.

## Deployment

### Scope
Our scope is the following Azure Subscriptions which are under Peter Lee (see below). However, we are currently deploying to hosts where we can troubleshoot the agent as we can only be responsible for what we can control.

| AMG Group Name| AMG Group ID|
|--|--|
| Accelerator | 154ed17d-a59b-43f7-a5cf-4e3dba514826 |
| AI Frontiers | 5f547a4b-81dc-4a59-a5da-df3f9d21e29f |
| AI4Science | dca5617c-4bf6-4546-b429-78c95ad258a5 |
| AIArch Futures | 5ae73c56-c440-46cb-8a47-c5a49304197d |
| Health Futures | 4d6dd9e3-c51e-4910-82a2-647eb90444e8 |
| MSR Core | 2ff1fddd-a7c1-448e-836c-af4461858a1e |
| R&I Services | b9bca0b1-1448-405a-8306-18bde1c0eb13 |

The query itself includes all the following parameters:
- All VMs and VMSS instances in the "N" series
- VMs and VMSS instances in Powerstate/running
- Running Ubuntu Linux
- Not running any End of Life Ubuntu distributions such as 16.04 or 18.04.

Our deployment mechanism lives in the [gpumetrics-deploy RG](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics-deploy/overview)and runs once a day.

### Logic Apps
| Logic App Name | Function |
|-|-|
| deploygpumetrics | Executes the Azure runCommand on VMs to run the shell script that installs gpumetrics components |
| deploygpumetrics-all | Executes the Azure runCommand on all VMs targets to run the shell script that installs gpumetrics components |
| deploygpumetrics-vmss | Executes the Azure runCommand on VMSS instances to run the shell script that installs gpumetrics components |
| gpumetricsapplyama | Installs the Azure Management Agent on all VM targets not showing that the extension is installed |
| gpumetricsapplyamavmss | Installs the Azure Management Agent on all VMSS not showing that the extension is installed |
| gpumetricsapplydcr | Associates in-scope VMs with the Data Collection Rule that are not already associated |
| gpumetricsapplydcr-arc | Associates in-scope Arc Computers with the Data Collection Rule that are not already associated |
| gpumetricsapplydcr-vmss | Associates the in-scope VMSS with the Data Collection Rule that are not already associated |



### Deployment Considerations
- This code queries the syslog table in the [gpumetrics LAW](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics/providers/Microsoft.OperationalInsights/workspaces/gpumetrics-wus3-law/logs) as well as the hosts in scope. Any hosts in scope that haven't written to the table in the last 30 days will be attempted to be installed so long as the AMA extension shows that its installed.
- It then uses the [Azure RunCommand](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/run-command) facility to execute these scripts against the hosts found.
- The Azure RunCommand stores artifacts on the host in `/var/lib/waagent/run-command/download/$number`, where `$number` is the number of runcommand instances. The latest one is always the last number. Inside the `$number` directory will be the script itself, a `stderr` and `stdout` file. The script can be run again if needed.
- Deployment happens with a script that makes some basic checks before it installs ansible. This will also write a file in /etc/default/gpumetricsonly to ensure that only gpumetrics is installed on these hosts.
- Status (OK or Error) is written to the deploygpumetrics_CL table in the [autodeploymentLAW Log Analytics Workspace](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/autodeployment/providers/Microsoft.OperationalInsights/workspaces/autodeploymentLAW/Tables). Since this just deploys daily, you can get stats as to the current failures with the following simple query on the [LAW query screen](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/autodeployment/providers/Microsoft.OperationalInsights/workspaces/autodeploymentLAW/logs), using the time range of Last 24 Hours:
  ```
  deploygpumetrics_CL 
  | limit 100 
  ```
  Most of the cases here are failures, even if the `messagetype` is `OK` since there are uninvestigated issues with some of these GPU hosts, and these hosts are outside our control.

### Azure Deployment Method
- Deployment is currently done with an [Azure Logic Apps](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics-deploy/overview)
- The Logic Apps are set to run once a day


## Agent - `/usr/local/bin/gpumetrics.sh`

The agent is currently a simple bash script hosted on [Github](https://github.com/rtepublic/gpumetrics).
.

By default, the agent is set to run every 10 minutes, and will report stored metrics every 30 minutes plus a random number from 0-30 minutes.

### Agent Files
| File| Description|
|-|-|
| `/etc/cron.d/gpumetrics` | The crontab which runs the script every 10 minutes.
| `/etc/logrotate.d/gpumetrics` | The logrotate configuration that will rotate the `/var/log/gpumetrics.log` files every 7 days.
| `/var/db/microsoft/gpumetricstome/report.db` | The file where cached metrics are stored, in JSON format, for metrics that haven't been sent yet
| `/etc/rsyslog.d/70-gpumetrics.conf` | The rsyslog configuration. This currently uses the local4 faculty, which the DCR is configured to transport to the LAW
| `/usr/local/bin/gpumetrics.sh`| This script runs `rocm-smi` or `nvidia-smi` depending on the GPU found. The data is formatted, and sent to syslog using the `logger` program.


### Deployment Dashboard
A preliminary dashboard to track GPUMetrics deployments can be found [here](https://gpumetricsdashboards-grcfbqgrawd9hca0.wus3.grafana.azure.com/d/eejpgf0thnuo0f/gpumetrics?orgId=1).


## Log Analytics Workspace
The Log Analytics Workspace is the data collection point of the gpumetricstome agent. As per the [tutorial](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-portal), it has the following objects:
- The Log Analytics Workspace itself called [gpumetrics-wus3-law](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics/providers/Microsoft.OperationalInsights/workspaces/gpumetrics-wus3-law/logs)
  - All log entries end up in the Syslog table
- The Log Analytics Data Collection Endpoint called [gpumetrics-wus3-dce](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics/providers/Microsoft.Insights/dataCollectionEndpoints/gpumetrics-wus3-dce/overview)
  - This is responsible for receiving data over HTTP
- The Log Analytics Data Collection Rule (DCR) called [gpumetrics-wus3-dcr](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics/providers/Microsoft.Insights/dataCollectionRules/gpumetrics-wus3-dcr/overview)
  - This keeps the resource list, and is needed to add new hosts for logging to the LAW


### Log Analytics Custom Table Schema for Syslog
It's possible to make a query to break out the columns from the SyslogMessage column like so:
```kql
Syslog
|extend GPU_Name=tostring(todynamic(SyslogMessage).GPUName), 
        GPU_DriverVersion=tostring(todynamic(SyslogMessage).GPUDriverVersion),
        GPU_TotalRAM=tostring(todynamic(SyslogMessage).GPUTotalRAM),
        GPU_UsedRAM=tostring(todynamic(SyslogMessage).GPUUsedRAM),
        GPU_MemPercentUsed=tostring(todynamic(SyslogMessage).GPUMemPercentUsed),
        GPU_UtilPercent=tostring(todynamic(SyslogMessage).GPUUtilPercent),
        GPU_Temperature=tostring(todynamic(SyslogMessage).GPUTemperature),
        GPU_PowerDraw=tostring(todynamic(SyslogMessage).GPUPowerDraw),
        GPU_PowerCap=tostring(todynamic(SyslogMessage).GPUPowerCap),
        GPU_Instance=tostring(todynamic(SyslogMessage).GPUInstance)
|extend resourceGroup=tostring(split(_ResourceId,'/')[4])
| take 100
```

**Azure Columns**
| Column Name | Description | Type |
|--|--|--|
|_ResourceId|A unique identifier for the resource that the record is associated with| String |
|_SubscriptionId|A unique identifier for the subscription that the record is associated with| String|
|TenantId||Guid|
|Type|The name of the table | String|
**Custom Columns**
| Column Name | Description | Type |
|--|--|--|
|GPUDriverVersion||String|
|GPUInstance||Int
|GPUMemPercentUsed||Int
|GPUName||String
|GPUTemperature|GPU temperature in Celcius|Int
|GPUTotalRAM|Total GPU RAM in MiB|Int
|GPUUsedRAM|Total GPU Ram in MiB|Int
|GPUUtilPercent||Int
|GPUUtilPercentAvg||Int
|GPUPowerDraw|GPU power draw in watts|int
|GPUPowerCap|GPU power cap in watts|int
|ReportTime||Datetime
|ResourceID||String
|TimeGenerated||Datetime

### Log Analytics Custom Log References
- [Tutorial: Send data to Azure Monitor Logs by using a REST API (Azure portal) - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-portal)
- [Logs Ingestion API in Azure Monitor - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/logs-ingestion-api-overview)
- [Azure Data Collection Rule Structure](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-collection-rule-structure#custom-logs)
- [GPUMetrics Summer 2025.pptx](https://microsoft.sharepoint.com/:p:/t/TnREng7/EddYcZwpMORHuhvS52TLP_gBtoBF3CHKbcVz3jamhIq6lg?e=yd5Sls)
