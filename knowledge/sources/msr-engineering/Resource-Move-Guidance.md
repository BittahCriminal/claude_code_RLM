[[_TOC_]]

# Overview

Moving resources in Azure can range from trivially easy, to fairly involved depending on the configuration of workloads, or completely unsupported depending on the resource type which may require redeployment of resources. There are many creative ways to migrate or move many different resource types, both supported and documented and other related/useful information that can be more esoteric. This guide tries to highlight some of the internal specific knowledge in addition to external guidance that is available (and like most things in Azure, constantly changing).

## General Information

[Overview Page](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-resource-group-and-subscription)

[Move Regions](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-resource-group-and-subscription)

[Supported Resources](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-support-resources)
* Tip: Using the powershell module `Az` you can use Get-AzResource to quickly get a list of resource types on a subscription.

`Get-AzResource |select-object -property ResourceType -unique`

## Resource Specific Move Guidance

### Virtual Machine

https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-limitations/virtual-machines-move-limitations
#### Virtual Machine SKU / Capacity Additional information
Note: If you are migrating GPU SKU VMs, you'll want to engage GCRAdmin for awareness as they control GPU capacity for T+R.
* [AI Capital Council Information](https://microsoft.sharepoint.com/teams/BB-8/SitePages/AI-Capital-Council(1).aspx)
* [Restricted GPU SKUs](https://microsoft.sharepoint.com/teams/BB-8/SitePages/GPU-SKUs-Restricted-and-Managed-Through-this-Process.aspx)

* [Internal Azure Capacity up-to-date information](http://aka.ms/azurecapacity) 
    * You can contact CapComms@microsoft.com or Contact Chris Donohue (cdonohue@microsoft.com) or join [azintcom](https://idwebelements/GroupManagement.aspx?Group=AzCapUpdates&Operation=join) (azure internal capacity management DL) for further questions on capacity issues/resolution.

### App Service
https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-limitations/app-service-move-limitations

### Classic Resources

https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-limitations/classic-model-move-limitations

### Networking
https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/move-limitations/networking-move-limitations

### Recovery Services
https://docs.microsoft.com/en-us/azure/backup/backup-azure-move-recovery-services-vault?toc=/azure/azure-resource-manager/management/toc.json

### Azure Automation
https://docs.microsoft.com/en-us/azure/automation/how-to/move-account?toc=/azure/azure-resource-manager/management/toc.json

### Azure DevOps
https://docs.microsoft.com/en-us/azure/devops/organizations/billing/change-azure-subscription?toc=%2Fazure%2Fazure-resource-manager%2Fmanagement%2Ftoc.json&view=azure-devops

## Other References

### Authorized Azure Regions for internal R&D workloads
https://msazure.visualstudio.com/AzureWiki/_wiki/wikis/AzureWiki.wiki/526/Azure-Regions?anchor=authorized-azure-regions-for-internal-r%26d-workloads

### AIRS Support

https://aka.ms/azrinternalesc

### Azure Tenant Migration
Please see this reference and related sub-pages from C+AI:
https://dev.azure.com/msazure/AzureWiki/_wiki/wikis/AzureWiki.wiki/33294/Azure-Subscription-Migration-SOP

### Standard Azure Support
If you run into technical issues / errors that are not helpful and not covered by the documentation, you may need to engage Azure Support from the portal for advisement.

We strongly recommend testing resource moves you haven't done yet on **TnR Engineering external test account** or another subscription before attempting moving customer resources.

Additionally, for escalations/guidance/advisement/hand offs contact MSREng@microsoft.com .

### Customer Subscription Access

PIM Elevation + SC-Alt required (SAW requirement likely coming Summer 2021). If you do not have access to the customer subscription, please contact msr-green@microsoft.com for guidance.

### Move subscription into a different management group
In the Microsoft.com AAD Tenant, we have partnered with the Microsoft Digital Cloud Governance team which has an orchestration sync service. That sync service replicates the hierarchy that subscriptions reside in service tree into management groups that correspond with the service tree IDs of that same hierarchy. To move a subscription into a different management group, the subscription must be moved in Service Tree.

15 minutes after the move is completed, the orchestration sync service will move the subscription automatically.
If subscription are moved to a different division, they will be moved back into the root tenant management group.

### Classify your subscription as production in service tree to avoid deallocation
Ensure you are not running any production workloads on any non-production subscriptions. If you are, move them to a production subscription immediately to avoid deallocation which can happen within a 24 hour notice.

Go to [ServiceTree](https://aka.ms/servicetree) to ensure your subscriptions are accurately marked as either production or nonproduction. If you need help or have questions, please contact msr-green@microsoft.com.

### Older reference / maybe inaccurate:
https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/1746/Resource-Migration