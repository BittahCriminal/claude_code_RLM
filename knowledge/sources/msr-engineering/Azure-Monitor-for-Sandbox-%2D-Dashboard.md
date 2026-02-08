# Introduction
The [Azure Monitor for Sandbox Dashboard](https://azmon-sandbox-emetebfkh4cyasft.wus2.grafana.azure.com/d/be3yo8b9c6rcwe/azure-alert-consumption?orgId=1&var-mc=Fired&var-as=New&var-sev=Sev0&var-sev=Sev2) is a visualization that contains the following panels:
## Azure Alerts
This shows the current list of alerts from Azure Monitor Alerts. The filter variables at the top of the page allow you to better sort the alerts. If you go to this page without the filters, you'll also see all the auto-resolved, acknowledged, and closed alerts. 

- **Resource Name Links** - The hostnames under "Resource Name" can be clicked to go to the Azure Resource in the Azure Portal.
- **Name Links** - The Alert Names under "Name" can be clicked to go to the alert status. From here you can mark the alert as "acknowledged" or "closed", as well as add notes.
- **Description Links** - The description link can be clicked which will give you the Alert query in Azure Resource Graph (ARG).
- Fired alerts will show up for VMs under the "Monitoring" tab on the alert overview page.
- Alerts will age out after 30 days. This is not configurable.
- Alerts can be disabled so that they do not trigger. To do so: 
  - Find the appropriate alert in the [azmon-sandbox rg](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/overview) or the [azmon-sandbox-arc rg](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/overview).
  - Click on the alert you wish to disable, and click on it.
  - Click the "⏹︎ Disable" button.
- Alert History can also be found in the appropriate alert. After clicking on the alert, click on the "🕔 History" blade.

## Azure Monitor Log Analytics
Items in this panel show all alerts in the last 2 hours that have shown as "CRITICAL" in log analytics workspaces. This panel may be more accurate than the panel above since alerts will age out, but ideally will be the same as the Azure Alerts panel.

- **Computer Links** - The hostnames under "Computer" can be clicked to go to the Azure Resource in the Azure Portal.

## Hosts Missing from Monitoring
Items in this panel are a subtractive union between Azure objects found in scope in Azure Resource Graph, and items that are in the Log Analytics Workspaces (LAW). There are two panels:

### Hosts with no Heartbeat from AMA
These hosts have no entries in the Heartbeat table in the LAW for the last 2 hours. The Azure Monitor Agent will constantly send a log about every minute to the LAW, regardless if it's set to send metrics or not.

These are fairly important to resolve since without a heartbeat:
- Hosts aren't reporting metrics for us to use in identifying their utilization
- Hosts won't alert if there are issues

You can query the logs for [Arc](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.OperationalInsights/workspaces/azmon-sandbox-arc-law/logs) or [VM](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/providers/Microsoft.OperationalInsights/workspaces/azmon-sandbox-law/logs) and try and see if there was a heartbeat previously with a query like:

```kusto
Heartbeat
| where TimeGenerated > now() - 30d
| where Computer == "GCRSANDBOX100"
```

### Hosts with no Syslogs
Similar to the above, any hosts that haven't sent anything to the Syslog table in the last 2 hours, will end up here. You can use a similar query as above to the appropriate LAW to see if it's sent syslogs previously.
```kusto
Syslog
| where TimeGenerated > now() - 30d
| where Computer == "GCRSANDBOX100"
```