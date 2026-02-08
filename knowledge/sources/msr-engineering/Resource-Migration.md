Some of the details in this page maybe older (~2019) but may still useful. Here is a newer reference:
https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4184/Resource-Move-Guidance

# Azure Migrate

## Purpose

Demonstrate how to move Azure resources to either another Azure subscription or another resource group under the same subscription, along with any limitations you may encounter for particular Azure resources.

[This page](https://docs.microsoft.com/en-us/azure/azure-resource-manager/move-support-resources) details which Azure Resources support the move operation and those that do not natively.

## Pre-requisites

## Move validation

References
https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-move-resources#validate-move

## Performing the move operation

-Portal
-Powershell
-AzCLI

References
https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-move-resources#use-the-portal

SQL Specific Information:

#### TODO - insert table from this page on migration option / purpose.
https://datamigration.microsoft.com/scenario/sql-to-azuresqldb?step=1

[Services and tools available for data migration scenarios](https://docs.microsoft.com/en-us/azure/dms/dms-tools-matrix)

[Data Migration Assistant](https://docs.microsoft.com/en-us/sql/dma/dma-overview?view=sql-server-2017)

[SQL Server Migration Assistant](https://docs.microsoft.com/en-us/sql/ssma/sql-server-migration-assistant?view=sql-server-2017)

## Troubleshooting a Move

Large Requests
When possible, break large moves into separate move operations. Resource Manager immediately returns an error when there are more than 800 resources in a single operation. However, moving less than 800 resources may also fail by timing out.

Resource Not in Succeeded State
When you get an error message that indicates a resource can't be moved because it isn't in a succeeded state, it may actually be a dependent resource that is blocking the move. Typically, the error code is MoveCannotProceedWithResourcesNotInSucceededState.

## Resources

Azure Services and related products

* Azure Migrate
* Azure Site Recovery
* Azure Database Migration Service
* Microsoft Data Migration Assistant

This [page](https://docs.microsoft.com/en-us/azure/azure-resource-manager/move-support-resources) shows which Azure resources are capable of using the move operation. It also provides consideration of special conditions to consider when moving a resource.

[Virtual Machine Move Guidance](https://docs.microsoft.com/en-us/azure/azure-resource-manager/move-limitations/virtual-machines-move-limitations)

[Networking Move Guidance](https://docs.microsoft.com/en-us/azure/azure-resource-manager/move-limitations/networking-move-limitations)

[AppService Move Guidance](https://docs.microsoft.com/en-us/azure/azure-resource-manager/move-limitations/app-service-move-limitations)

[Recovery Services Move Guidance](https://docs.microsoft.com/en-us/azure/backup/backup-azure-move-recovery-services-vault?toc=/azure/azure-resource-manager/toc.json)

[Classic Deployment Move Guidance](https://docs.microsoft.com/en-us/azure/azure-resource-manager/move-limitations/classic-model-move-limitations)

Virtual Machine Note:
If your virtual machine is encrypted with Azure Disk Encryption (ADE), you need to first decrypt the VM, then perform the move operation on the virtual machine, then re-encrypt them again once moved.

Log Analytics (OMS) Note:
Make sure moving to new subscription doesn't exceed [subscription quotas](https://docs.microsoft.com/en-us/azure/azure-subscription-service-limits#azure-monitor-limits)

SQL Note:
A database and server must be in the same resource group. When you move a SQL server, all its databases are also moved. This behavior applies to Azure SQL Database and Azure SQL Data Warehouse databases.

KeyVault Note:
Key Vaults used for disk encryption can't be moved to a resource group in the same subscription or across subscriptions.

HD Insight Note:
You can move HDInsight clusters to a new subscription or resource group. However, you can't move across subscriptions the networking resources linked to the HDInsight cluster (such as the virtual network, NIC, or load balancer). In addition, you can't move to a new resource group a NIC that is attached to a virtual machine for the cluster.
When moving an HDInsight cluster to a new subscription, first move other resources (like the storage account). Then, move the HDInsight cluster by itself.

Redis Cache Note:
If the Azure Cache for Redis instance is configured with a virtual network, the instance can't be moved to a different subscription. See Networking move limitations.

Azure Automation Note:
Runbooks must exist in the same resource group as the Automation Account.

Marketplace Application Note:
A subscription move or merge will also need to redeploy any marketplace applications (not Azure services) you are using within that subscription because it’s a billing change.

Subscription Move Note:
If you transfer subscription to an account in another Azure AD tenant, any administrator roles and Role-based Access Control (RBAC) assignments on the subscription do not transfer. Also, Azure AD App Registrations and other tenant-specific services don't transfer along with the subscription.

### FAQ

* How do I move a subscription in Service Tree?

Start by navigating to your subscription(s) for a given service and click the reassign link in the subscription row you want to move. Set the service where you want the subscription moved and hit submit.
