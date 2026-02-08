# Summary
A node will have a heartbeat issue when there aren't any recent heartbeat entries in the appropriate Log Analytics Workspace. The Azure Monitor Agent (AMA) is responsible for sending these entries. Causes for this can be:
- The host is unresponsive or offline
- The AMA agent/extension isn't installed
- The AMA agent isn't associated with the Data Collection Rule (DCR)
- The AMA agent is malfunctioning.

This guide has methods on how to fix the last 3 issues listed.

Windows Servers are currently not supported for monitoring. If you want to exclude it from monitoring, simply tag the node in the Azure portal with **OS: Windows**, and it will be excluded from the dashboard.
![image (5).png](/.attachments/image%20(5)-10ac45bf-ee43-44a6-a715-2d3866636090.png)

# Check the host
- Since there's no monitoring going on the host with the AMA agent not reporting in, you'll need to check somethings on the host itself including:
	- Disk space
	- Does an ansible-run execute without errors?
	- How are the azure monitor agent daemons?

# Arc Only - Ensure the Arc object says things are ok
Go to the host in the Azure Portal, and ensure that:
- The top of the page doesn't say "This server is not connected to Azure. Click here for more info"

# Ensure AMA is installed in the extensions blade and the version is current.
- Check that the AzureMonitorLinuxAgent shows up in the extensions blade, and that the version is the latest. (at or past 1.33.1 as of this writing). You can upgrade the agent from the portal with a fair amount of ease. Though it'll take about an hour.

# AMA Agent Membership
Check to see if the Arc agent is part of the DCR at this page:
[azmon-sandbox-arc-dcr - Microsoft Azure](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.Insights/dataCollectionRules/azmon-sandbox-arc-dcr/machines)

For VMs the DCR is here:
[azmon-sandbox-dcr - Microsoft Azure](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/providers/Microsoft.Insights/dataCollectionRules/azmon-sandbox-dcr/machines)

Search the list to see if you can find it. If you can't find it, and it looks like the agent is working correctly, you can add it from the UI, or skip down to the section "Add the host to the DCR" and perform that command.

If you add the host and wait for as little as 1 minute and up to 20 minutes and you're still not seeing a heartbeat following the "Check Heartbeat" on the instructions below, proceed with the below instructions.

# Prerequisite permissions for below commands to work
"az login" to the GCR Arc sub.
![gcrarcsub.png](/.attachments/gcrarcsub-4560d3e0-4265-479a-b3a6-d08d0aea28dc.png)
You can also do `az account set --subscription "GCR Arc"`

Elevate to necessary subs too.
| Subscription Name | Subscription ID |Resource Group |
|-|-|-|
|GCR Arc | 46e0b8e9-eb7f-4bbf-af34-a502c2d310f7  | [GPU-Sandbox](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/GPU-Sandbox/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox1](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox1/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox2](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox2/overview)
|GCRProdEx2| 46da6261-2167-4e71-8b0d-f4a45215ce61 | [GPU-Sandbox3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46da6261-2167-4e71-8b0d-f4a45215ce61/resourceGroups/GPU-Sandbox3/overview)


# Disconnecting/Reconnecting the Arc Agent

## Save the tags
You can use this script to get the command to recreate the current tags for the host:
```bash
#!/bin/bash

# Variables 
export TARGETHOSTNAME="GCRSANDBOX100"

resource_id="/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/GPU-Sandbox/providers/Microsoft.HybridCompute/machines/$TARGETHOSTNAME"

# Get tags from the source resource
# tags=$(az tag list --resource-id $resource_id --query "properties.tags" -o tsv)
tags=$(az tag list --resource-id $resource_id --query "properties.tags"|sed '/[{}]/d'|sed 's/^[[:space:]]*//g'|sed 's/:\ /=/g'|tr -d '"' | tr ',\n' ' ')

# Apply the tags to the target resource
echo "az tag create --resource-id $resource_id --tags $tags"
# az tag create --resource-id $resource_id --tags $tag_args
```

## Optional: Remove Arc agent, etc
```bash
apt-get purge azcmagent azuremonitoragent -y
rm -rf /opt/microsoft/azuremonitoragent/ /etc/opt/microsoft/azuremonitoragent
```

### Arc Only - Disconnect the Arc host from the host itself
```bash
export TOKENDISPENSER_ENDPOINT="gcr-arc-onboarding-frghdffpbfd9bjd8.b01.azurefd.net"
export FUNCTION_KEY="$( az keyvault secret show --name gcr-arc-onboarding-app-key --vault-name gcrcmvault --query value --output tsv)"
azcmagent disconnect --access-token $(curl -s https://$TOKENDISPENSER_ENDPOINT/api/gcr-arc-onboarding-req?code=$FUNCTION_KEY | jq -r '.access_token') --user-tenant-id 72f988bf-86f1-41af-91ab-2d7cd011db47
```

### Arc Only - Reconnect the host

```bash
ssh $ARCHOSTNAME.redmond sudo /usr/local/bin/ansible-onboard-arc
```

# Reinstall the extension (for the impatient)
Policy will eventually get around to installing the extension, but it can take several hours.

## Azure Portal
You can install the agent from the Azure portal going to the node, and clicking on the "Extensions" blade under "Settings". Click on "+ Add" and search for Azure Monitor Agent for Linux. Once you find it, click "Next" through the dialogs till you get to "Review + Create". You do not need to check "Use Proxy".

## CLI Command
### Arc
You can also use the below command to install the AMA extension.  The command below can take anywhere from 30 minutes to an hour or so. You can use the `--no-wait` flag for fire and forget:
```bash
export ARCHOSTNAME="GCRSANDBOX100"

az connectedmachine extension create --name AzureMonitorLinuxAgent --publisher Microsoft.Azure.Monitor --type AzureMonitorLinuxAgent --machine-name $ARCHOSTNAME --resource-group gpu-sandbox --location westus2

#if WINDOWS this is the command 
az connectedmachine extension create --name AzureMonitorWindowsAgent --publisher Microsoft.Azure.Monitor --type AzureMonitorWindowsAgent --machine-name $ARCHOSTNAME --resource-group gpu-sandbox --location westus2
```
### VM
```bash
export VMHOSTNAME="GCRSANDBOX100"
export RESOURCEGROUP="GPU-Sandbox2"

az vm extension set --name AzureMonitorLinuxAgent --publisher Microsoft.Azure.Monitor --vm-name $VMHOSTNAME--resource-group $RESOURCEGROUP --enable-auto-upgrade true
```

# Add the host to the DCR
## Arc
Once the Azure Monitor Agent is installed on the host, you can add it to the DCR.
```bash
export ARCHOSTNAME="GCRSANDBOX100"

az monitor data-collection rule association create  --name $ARCHOSTNAME --rule-id "/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.Insights/dataCollectionRules/azmon-sandbox-arc-dcr/" --resource /subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/GPU-Sandbox/providers/Microsoft.HybridCompute/machines/$ARCHOSTNAME
```
## VM
You'll need to get the Azure ID from the host which has the appropriate
```bash
export VMHOSTNAME="GCRAZGDL1000"
export RESOURCEGROUP="GPU-Sandbox2"
export SUBSCRIPTION="46da6261-2167-4e71-8b0d-f4a45215ce61" #GCRPRodEx2

az monitor data-collection rule association create  --name $VMHOSTNAME --rule-id "/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.Insights/dataCollectionRules/azmon-sandbox-dcr/" --resource /subscriptions/$SUBSCRIPTION/resourceGroups/$RESOURCEGROUP/providers/Microsoft.Compute/virtualMachines/$VMHOSTNAME
```

## Check Heartbeat
After you've added the host to the DCR, it can take anywhere from 1 to 20 minutes or so for the heartbeats to show up.

You can go to the LAW and see if the host has a heartbeat. Heartbeats are sent every minute:
[azmon-sandbox-arc-law - Microsoft Azure](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.OperationalInsights/workspaces/azmon-sandbox-arc-law/logs)

```kusto
Heartbeat
| where Computer == "GCRSANDBOX100"
```