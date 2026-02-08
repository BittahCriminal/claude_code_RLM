# Introduction
This describes the Linux user/group service that's used chiefly by GCR, but is capable of hosting for much of MSR if needed.

## SLO/SLI/KVI

The following are definitions of SLO/SLI and KVI. No actual metrics are available for this service currently.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal;">Ensure logins take under 5 seconds, and user/group lookups take under 2 seconds.</span>|
| --- | --- |
| SLI | Create a dashboard that shows the above metric |
| KVI | Number of hosts using this service |

### Methodology:
None of the above have been implemented, but here are some proposals and explanations:

**SLO** - May need to be adjusted.  
**SLI** - Would need to make a dummy monitoring host or use an ACI to ensure this is the case. Ideally this would be per replica that I have this service so we can ensure each has the same service level.
**KVI** - Capturing the number of hosts would be somewhat difficult since we don't have any metrics today. Getting the GCR footprint could match the Ansible footprint, but we also have hosts outside of GCR and Ansible management that also use this. Mandating some sort of once a day check-in via cron could be a possibility.

# Client Components
This service allows user and selected group lookups from Ubuntu that are imported from the [Microsoft Graph](https://developer.microsoft.com/en-us/graph/graph-explorer) user and groups.

The client components of the user+group service are libnss-extrausers for Ubuntu. Azure Linux would use nss-altfiles. This allows an additional passwd, group and shadow set of files to be used in addition to the defaults.


# Synchronization Components

Synchronization components can be found in the [groupsync-container-instance](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f0f57942-516a-458e-81d7-7e35ff68dbf1/resourceGroups/groupsync-container-instance/overview) resource group.

Codebase: 
- [usergroupfiles](https://dev.azure.com/msresearch/MSR%20Engineering/_git/usergroupfiles) (for flat files)

## Azure Container Instance (ACI)
All container instances can be deployed using the [bash script](https://dev.azure.com/msresearch/MSR%20Engineering/_git/groupsyncdirpgsql?path=/scripts/execute_bicep_groupsyncpgsql.sh) which with the right Azure permissions, can deploy all four contains below, and will clobber any existing containers if run.

All container instances are running the [Azure Linux base container](https://eng.ms/docs/products/azure-linux/gettingstarted/containers/distroless) which gives a minimized attack surface, reduced noise from vulnerability scanners, and better performance due to the small size (~10MB). It's also the bare minimum needed to run the statically compiled usergroupfiles Go binary. We're able to run use this container as-is without any modifications.

**Cost:** $0.20/day - $6.00/month.

## Group Updates
To update groups you'll need to access the `syncgroups` table in the [groupsyncstorage](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f0f57942-516a-458e-81d7-7e35ff68dbf1/resourceGroups/groupsync-container-instance/providers/Microsoft.Storage/storageAccounts/groupsyncstorage/overview) storage account. 
- This requires you to make the storage account to have public access while you perform this operation, or you'll get access errors (that won't necessarily be about network access).
- Ensure that you use the uid from Entra, and a unique gid. Try and use the next digit available as many old group have used previous numbers.

### Container instance modes and roles

- [usergroupfiles-buildfiles](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f0f57942-516a-458e-81d7-7e35ff68dbf1/resourceGroups/groupsync-container-instance/providers/Microsoft.ContainerInstance/containerGroups/usergroupfiles-buildfiles/overview) This is the container that builds the passwd, group and shadow files. These get put into the https://sescmartifacts.blob.core.windows.net/artifacts/linux/usergroup/ dir.

## Troubleshooting
To troubleshoot the Go binary, it can be run locally, assuming you have the correct permissions in place. It's best to run this inside a test container, see the [execute_bicep_groupsyncpgsql-test.sh](https://dev.azure.com/msresearch/MSR%20Engineering/_git/groupsyncdirpgsql?path=/scripts/execute_bicep_groupsyncpgsql-test.sh) script. If you are using a container that you can log in to, either using the `base` Azure Linux type, or the debug type for Azure Linux Distroless, you can click on the container object, then click on the `Containers` blade, and click on the "connect" tab to have an interactive shell session inside the container.

You can view logs for a single ACI from the portal by clicking on the container object such as [this one](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f0f57942-516a-458e-81d7-7e35ff68dbf1/resourceGroups/groupsync-container-instance/providers/Microsoft.ContainerInstance/containerGroups/usergroupfiles-buildfiles/containers), clicking on the "Containers" blade, and then clicking on the Logs tab.

Logs for all the containers are sent to the [groupsyncLAW](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f0f57942-516a-458e-81d7-7e35ff68dbf1/resourceGroups/groupsync-container-instance/providers/Microsoft.OperationalInsights/workspaces/groupsyncLAW/logs). You can use this in scenarios, such as finding a username to see if they were sync'd or deleted. A query like the below can search for a username in the log text:
```kusto
ContainerInstanceLog_CL
| where Message contains "krisz"
```
These logs are configured to store data at the Log Analytics Workspace default of 30 days. The Custom Log container is created automatically when executing the bicep with this relevant section:
```yaml
    diagnostics: {
      logAnalytics: {
        workspaceId: LAW_WORKSPACE_ID
        workspaceKey: LAW_PRIMARY_KEY
      }
```

# Alerting
All Logic Apps in the resource group have alerts that will trigger if there are 3 failures relative to the times they execute. These failures will be posted in the [RTE Service Alert channel](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/gcrauthvault/providers/Microsoft.KeyVault/vaults/gcrauthvault/overview).

# References
