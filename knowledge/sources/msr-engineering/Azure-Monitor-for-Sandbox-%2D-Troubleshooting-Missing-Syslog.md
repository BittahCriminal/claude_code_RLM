# Introduction
Hosts with a "Missing Syslog" status have the same effective result as "Missing Heartbeat" in that they are producing no alert data. Hosts must be reporting to the Heartbeat table and the Syslog table to be working with the Azure Monitor system.

# Method
- Use the same steps as found in the [Azure Monitor for Sandbox - Troubleshooting Heartbeat Issues](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/14198/).

## Verification
Go to the appropriate LAW to query for data: (not accessible via SC-Alt)
- ARC - [azmon-sandbox-arc-law](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.OperationalInsights/workspaces/azmon-sandbox-arc-law/logs)
- VM - [azmon-sandbox-law](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/providers/Microsoft.OperationalInsights/workspaces/azmon-sandbox-law/logs)

You can use the following query to look for Syslog data within the logs (replace gcrsandboxXXX with the actual hostname):
```kql
Syslog
| where TimeGenerated > now() - 24h
and _ResourceId contains "gcrsandboxXXX"
| sort by TimeGenerated
| project _ResourceId
| distinct _ResourceId
| project ResourceID = tolower(_ResourceId), fields = split(_ResourceId, "/")
| mv-expand gmname = fields[8]
| project-away fields
```
If you see no data, then this shows the host isn't emitting data to the sandbox.

## Check the syslog on the system
1.       Check the system log file:
```kgl
sudo tail /var/log/syslog
```
2.       If it’s empty, that’s an indicator that logs are not being written.
3.       Verify if rsyslog is running:
```kgl
systemctl status rsyslog
```
4.       If the service is inactive or dead, restart it:
```kgl
sudo systemctl start rsyslog
```
After restarting, check /var/log/syslog again to confirm that logging has resumed.
```kgl
tail /var/log/syslog
```

## Check to ensure that the Azure Monitor Agent is installed
1. Go to the Azure Portal for the machine (Arc or VM)
2. Go to the Settings > Extensions page
3. Look for AzureMonitorLinuxAgent in the list.
a. If it exists but is outdated, chec, the box and click Update
![image.png](/.attachments/image-a29766d8-41d4-4db1-9633-640e4ea973e6.png)
b. If it is missing the agent, click Add then on the next page search Linux and install the agent
![image.png](/.attachments/image-05acf857-7fa9-43a0-8bf4-d33968fecc61.png)
