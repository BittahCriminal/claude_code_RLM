[[_TOC_]]

#In Microsoft Research
If you are looking for read-only projects for all projects in the msresearch organization, please reach out to the [MSR-ADO](mailto:msr-ado@microsoft.com) alias with justification. We maintain an All Projects Read Access group for this purpose.

#In your own Azure DevOps organization
##Through the Azure DevOps user interface
If you want to create a custom group that will grant access to all projects in an ADO org, you can do so with the process described below. Note that this will not track new projects and is not maintained in any way by the system, so the fidelity of this group's access may degrade over time. 

![image.png](/.attachments/image-7e61f50e-087d-4ca3-ad79-627b088467df.png)
1. Go to your organization's settings page and select the **Users** entry from the left-side nav bar
1. Click **Group rules**
1. Click **Add a group rule**
![image.png](/.attachments/image-c2e0f189-bc22-4aa0-88fd-1cb8f76ed22b.png)
1. Click **Create a new Azure DevOps group**
1. Click the **Projects** dropdown
1. Click the **Add all** button
![image.png](/.attachments/image-6f167245-70ec-4c06-9f4c-f39e90f8cc8c.png)
1. From the **Azure DevOps Groups** dropdown, select **Project Readers**

## Using a PowerShell script
If you need your org-level readers group to stay up to date with all the projects in the org and not slowly be removed from groups by overzealous project administrators, you'll want to use a PowerShell script and either run it manually on some schedule or automate with an Azure Function or similar. Below is a sample script to do this. Please note the following:
- The script is dependent on having [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) installed, as well as the [azure-devops extension for Azure CLI](https://github.com/Azure/azure-devops-cli-extension). Be sure to log in before attempting to run the script.
- It is naive and will always attempt to add every project's readers group.

```ps
Start-Transcript "MakeAPRA-$(get-date -Format "yyMMdd-HH.mm").log"

$orgUrl = https://dev.azure.com/msresearch

Write-Host "Getting project list... ($(get-date -Format "HH:mm"))"
$allProjects = @()
$thisRun = az devops project list --org https://dev.azure.com/msresearch| ConvertFrom-Json
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

Write-Host "Getting all groups... ($(get-date -Format "HH:mm"))"
$allOrgGroups = @()
$thisRun = az devops security group list --org $orgUrl --scope organization | ConvertFrom-Json
while($thisRun.ContinuationToken)
{
	Write-Host "Got $($thisRun.graphGroups.count) groups this pass"
	$allOrgGroups += $thisRun.graphGroups
	$thisRun = az devops security group list --org $orgUrl --scope organization `
		--continuation-token $thisRun.ContinuationToken | ConvertFrom-Json
}
$allOrgGroups += $thisRun.graphGroups
Write-Host "Got $($thisRun.graphGroups.count) groups this pass"
Write-Host "Got $($allOrgGroups.count.ToString("n0")) groups in total"

$apra = $allOrgGroups | Where-Object principalName -like "*All Projects Read Access" # Get the details for the All Projects Read Access group
$readerGroups = $allOrgGroups | Where-Object principalName -like "*Readers" # Get all readers groups. There should be one per ADO project.

#Add the All Projects Read Access group to every project's valid user group
foreach($readerGroup in $readerGroups)
{
    Write-Host "Adding $($readerGroup.principalName)..."
    az devops security group membership add --member-id $apra.descriptor --group-id $readerGroup.descriptor --org $orgUrl
}


### Attempt to confirm the above script worked. ###
#Gets an oddly formatted list of group memberships
Write-Host "Getting APRA group membership... ($(get-date -Format "HH:mm"))"
$apra = $allOrgGroups | Where-Object principalName -like "*All Projects*"
$apramsSource = az devops security group membership list --org $orgUrl --id $apra.descriptor --relationship memberof --debug
$aprams = $apramsSource | ConvertFrom-Json
#Turn properties into list items
$membershipCache = New-Object System.Collections.ArrayList
foreach($membership in $aprams.PSObject.Properties)
{
    $membershipCache.Add($membership.value) > $null
}

#Display list of assigned groups to user
$membershipCache.principalName | Sort-Object | Write-Host
Write-Host "Now assigned to $($membershipCache.Count) groups."
Stop-Transcript
```
## History
We originally needed an org-wide read-only group to enable some security review. William reached out to the Azure CLI team (AzDevInMIProToColCLI@microsoft.com) and confirmed that the approaches described here are as good as it gets as of 2020/01/22. There are some hints of future changes to this, but no solid information.