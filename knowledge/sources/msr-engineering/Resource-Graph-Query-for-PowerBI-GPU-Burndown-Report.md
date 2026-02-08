[[_TOC_]]
# Resource Graph Query for GPU Burndown



## Azure Function - Resource Graph PBI Export Details
Here's a link to see the current [Azure Function Code](https://ms.portal.azure.com/#view/WebsitesExtension/FunctionMenuBlade/~/code/resourceId/%2Fsubscriptions%2Fa5224fa9-985e-4c4a-9636-738af9bc5e82%2FresourceGroups%2FJD-RG-01%2Fproviders%2FMicrosoft.Web%2Fsites%2Fmsr-green-obs%2Ffunctions%2FInventory-ResourceGraph-PBIExport) that is running.

- Azure Function Timer Trigger runs daily
- Queries Azure Resource Graph using the below query
- Exports the results as a .csv to this [storage account](https://ms.portal.azure.com/#view/Microsoft_Azure_Storage/ContainerMenuBlade/~/overview/storageAccountId/%2Fsubscriptions%2Fa5224fa9-985e-4c4a-9636-738af9bc5e82%2FresourceGroups%2FJD-RG-01%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Fmsrgreenobs/path/gpumetrics/etag/%220x8DA762FA45B8F9A%22/defaultEncryptionScope/%24account-encryption-key/denyEncryptionScopeOverride~/false/defaultId//publicAccessVal/None) (blob container)
- PowerBI can connect to the storage account (blob container) where the results are being saved

You can use the Azure Resource Graph powershell module to see the same results that the function is using:



```powershell
# if you haven't installed the Azure PowerShell module and Resource Graph module, you can run the following to do so
Install-Module Az,Az.ResourceGraph

# Resource Graph Query that we're using to get GPU virtual machine information
$query = "resources | join kind=leftouter (ResourceContainers | where type=='microsoft.resources/subscriptions' | where properties['managementGroupAncestorsChain'] contains 'f6f135c8-4691-4b1e-843b-99021f21f425' or properties['managementGroupAncestorsChain'] contains 'b9bca0b1-1448-405a-8306-18bde1c0eb13' or properties['managementGroupAncestorsChain'] contains 'f6f135c8-4691-4b1e-843b-99021f21f425'| project subName=name, subscriptionId) on subscriptionId |where type == 'microsoft.compute/virtualmachines'|extend vmSize = tostring(properties.hardwareProfile.vmSize)|extend powerState = tostring(properties.extended.instanceView.powerState.code)|extend  osName = tostring(properties.extended.instanceView.osName)|extend osVersion = tostring(properties.extended.instanceView.osVersion)|extend gpuMetricsDeployed = tostring(iif(isnotnull(tags.GPUMetricsDeployed), tags.GPUMetricsDeployed,'false'))|extend gpuMetricsDeployDate = tostring(iif(isnotnull(tags.GPUMetricsDeployDate), tags.GPUMetricsDeployDate,''))| where vmSize startswith 'Standard_N'| project subscriptionId, subName, name, resourceGroup, vmSize, powerState, osName, osVersion, location,gpuMetricsDeployed,gpuMetricsDeployDate"

# initial response
$response = Search-AzGraph -Query $query -First 1000 -ov gpuAzResourceGraphResults

# if the results are larger than 1,000, we page through to get the rest of the results
while($response.SkipToken){$response = Search-AzGraph -Query $query -SkipToken $response.SkipToken -ov +gpuAzResourceGraphResults}

#save the results
$graphres = $gpuAzResourceGraphResults.Data

#view the results
$graphres
```

## Resource Graph Explorer
If you just want to view or modify the results of the query, using Azure Resource Graph explorer is likely the quickest option to get started with.

As shown in the snip below:
- Navigate to [Azure Resource Graph Explorer](https://ms.portal.azure.com/#view/HubsExtension/ArgQueryBlade)
- `Open a query`
- `Shared Queries`
- You can see existing queries that we're using. 
    - `[GPU Metrics] GPU VMs - Filtered to RnI` is the most current one 

![image.png](/.attachments/image-9b2470a2-9fb7-4155-8b59-1d2fcc720a19.png)


The below `[GPU Metrics] GPU VMs - Filtered to RnI` query is (very close) to the azure resource graph query we're currently using in the Timer Azure Function
``` csharp
Resources 
| join kind=leftouter (
ResourceContainers 
| where type=='microsoft.resources/subscriptions' 
| where properties["managementGroupAncestorsChain"] contains 'f6f135c8-4691-4b1e-843b-99021f21f425' or properties["managementGroupAncestorsChain"] contains 'b9bca0b1-1448-405a-8306-18bde1c0eb13' or properties["managementGroupAncestorsChain"] contains 'f6f135c8-4691-4b1e-843b-99021f21f425'
| project subName=name, subscriptionId) on subscriptionId 
|where type == 'microsoft.compute/virtualmachines'
|extend vmSize = tostring(properties.hardwareProfile.vmSize)
|extend powerState = tostring(properties.extended.instanceView.powerState.code)
|extend  osName = tostring(properties.extended.instanceView.osName)
|extend osVersion = tostring(properties.extended.instanceView.osVersion)
| //where powerState == "PowerState/running" //removed since we're filtering in PBI
| //where osName == "ubuntu" //removed since we're filtering in PBI
| where vmSize startswith "Standard_N"
| project subscriptionId, subName, name, resourceGroup, vmSize, powerState, osName, osVersion, location
```
