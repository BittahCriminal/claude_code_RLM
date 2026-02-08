#Projects
The [Azure DevOps documentation](https://docs.microsoft.com/en-us/azure/devops/integrate/concepts/rate-limits?view=azure-devops) mentions a number of limits, but the limit of 300 projects is only mentioned in the [Cloud Migration Guide](https://azure.microsoft.com/en-us/services/devops/migrate/). The UI doesn't expose the number of projects anywhere, but the following script can pull a list of projects and groups. It is dependent on having [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) installed, as well as the [azure-devops extension for Azure CLI](https://github.com/Azure/azure-devops-cli-extension).

```ps
# Retrieve list of all projects
$allProjects = @()
$thisRun = az devops project list --org https://dev.azure.com/msresearch | ConvertFrom-Json
while($thisRun.ContinuationToken)
{
	Write-Host "Got $($thisRun.value.count) projects this pass"
	$allProjects += $thisRun.value
	$thisRun = az devops project list --org https://dev.azure.com/msresearch `
		--continuation-token $thisRun.ContinuationToken | ConvertFrom-Json
}
$allProjects += $thisRun.value
Write-Host "Got $($thisRun.value.count) projects this pass"
Write-Host "Got $($allProjects.count.ToString("n0")) projects in total"
Write-Host ""

#Retrieve list of groups
$allOrgGroups = @()
$thisRun = az devops security group list --org https://dev.azure.com/msresearch --scope organization | ConvertFrom-Json
while($thisRun.ContinuationToken)
{
	Write-Host "Got $($thisRun.graphGroups.count) groups this pass"
	$allOrgGroups += $thisRun.graphGroups
	$thisRun = az devops security group list --org https://dev.azure.com/msresearch --scope organization `
		--continuation-token $thisRun.ContinuationToken | ConvertFrom-Json
}
$allOrgGroups += $thisRun.graphGroups
Write-Host "Got $($thisRun.graphGroups.count) groups this pass"
Write-Host "Got $($allOrgGroups.count.ToString("n0")) groups in total"
```


#Metrics
We have very few metrics for measuring the performance of our Azure DevOps organization, but users who want to see performance metrics can do so by navigating to [https://dev.azure.com/msresearch/_diagnostics](https://dev.azure.com/msresearch/_diagnostics) and enabling the Perf Bar option.
![image.png](/.attachments/image-1f1f9f4b-b486-4fa3-861f-667944d02a8d.png =300x)