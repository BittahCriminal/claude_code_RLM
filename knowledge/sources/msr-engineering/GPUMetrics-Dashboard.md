# Introduction
The [GPUMetrics dashboard](https://gpumetricsdashboards-grcfbqgrawd9hca0.wus3.grafana.azure.com/d/eejpgf0thnuo0f/gpumetrics?orgId=1) has a number of panels which show the spread of deployment of the metrics agent. However, some of these panels may be confusing or counter intuitive. This wiki page tries to explain some of that.

# The number panels

Many of the number panels are clickable, and will take you to Azure Resource Graph Explorer with the query, which you can do yourself and manipulate, assuming you have the correct permissions to query across the resources in question.

## Azure GPUs in Scope
This is an [Azure Resource Graph](https://ms.portal.azure.com/#view/HubsExtension/ArgQueryBlade) query that polls for just the hosts [in scope](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4220/GPUmetrics-service?anchor=scope). The definition of what is in-scope can be found [here](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4220/GPUmetrics-service?anchor=scope).

## Hosts reporting to LAW in the last 24 hours
This queries the [Log Analytics Workstation](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/6d92c829-42ca-4ce0-91d0-6eedf32a2658/resourceGroups/gpumetrics/providers/Microsoft.OperationalInsights/workspaces/gpumetrics-wus3-law/logs), and gets the unique hosts which have reported into the database in the last 24 hours.

## Systems Not Reporting In
This is the result of a "negative join" query where the hosts from "Hosts reporting to LAW in the last 24 hours" are subtracted from "Azure GPUs in Scope". The remaining hosts are reported.

- Why isn't this value the result of Hosts reporting to LAW minus Azure GPUs in Scope?
  Mostly because this is the cloud, and hosts aren't static. Thus, some hosts reporting in the last 24 hours could have been recently put out-of-scope for a variety of reasons, including:
  - Have been recently been deallocated or deleted
  - Have a broken waagent daemon, thus it won't report it's OS and is now out of scope
   
## Systems without Azure Agent
These are systems who's OS version and distribution aren't being reported to Azure. For linux systems, this means their [Azure Linux agent](https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/agent-linux) has been disabled which can be for a variety of reasons, including:
- A problem with the agent itself
- For Ubuntu, the debian packaging system is broken for some reason
- The agent has been intentionally disabled

## Systems without Azure Agent
- These are systems who's OS version and distribution aren't being reported to Azure. For linux systems, this means their [Azure Linux agent](https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/agent-linux) has been disabled which can be for a variety of reasons, including:
- A problem with the agent itself
- For Ubuntu, the debian packaging system is broken for some reason
- The agent has been intentionally disabled

## Azure GPUs Out of Scope
This report shows systems out of scope for reporting. These include:
- Windows systems
- End of Life Linux versions such as Ubuntu 16.04
- Non-Ubuntu Linux distributions

## Azure GPUs Offline
This reports on all N series hosts in our AMG scopes who's power state is not "Powerstate/running".
There is no corresponding host table since we don't plan on actioning these, but data can be explored in Azure Resource Explorer.

# Host Table Lists
Explanations in the above should explain the systems listed in the tables below.