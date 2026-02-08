Currently the [scope](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/8580/SES-Patching-Scope) for GCR patching service is all GCR Sandboxes Onprem and Azure Windows and Linux. 

Linux nodes gets onboarded to our patching service via Ansible and Azure policy.
 
Windows Onprem needs to onboard to Azure arc first and then from there it will be automatically onboard to our patching service via Azure policy.

If you intend to onboard different nodes than GCR sandbox to our service or nodes that are outside of RTE please reach out to gcradmin for discussion. 


**How to onboard Windows Onprem to GCR azure arc to be onboarded to GCR patching.**

- RDP to the node you want to onboard to arc. Make sure you have elevated permissions via PIM to [GCR-arc sub](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/overview)

- Open PowerShell as administrator and run below script. It will ask to login to Azure via your sc-alt creds ( If SC-alt isn't ready to use on node, select back and enter code into www.microsoft.com/devicelogin.) and then it will onboard the node to our GCR arc sub from there it wil be automatically onboarded to GCR patching service. 


```
try {
    $env:SUBSCRIPTION_ID = "46e0b8e9-eb7f-4bbf-af34-a502c2d310f7";
    $env:RESOURCE_GROUP = "GPU-Sandbox";
    $env:TENANT_ID = "72f988bf-86f1-41af-91ab-2d7cd011db47";
    $env:LOCATION = "westus";
    $env:AUTH_TYPE = "token";
    $env:CORRELATION_ID = "066c988a-f600-4a04-8650-4f71686d19d7";
    $env:CLOUD = "AzureCloud";
    

    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor 3072;

    # Download the installation package
    Invoke-WebRequest -UseBasicParsing -Uri "https://aka.ms/azcmagent-windows" -TimeoutSec 30 -OutFile "$env:TEMP\install_windows_azcmagent.ps1";

    # Install the hybrid agent
    & "$env:TEMP\install_windows_azcmagent.ps1";
    if ($LASTEXITCODE -ne 0) { exit 1; }

    # Run connect command
    & "$env:ProgramW6432\AzureConnectedMachineAgent\azcmagent.exe" connect --resource-group "$env:RESOURCE_GROUP" --tenant-id "$env:TENANT_ID" --location "$env:LOCATION" --subscription-id "$env:SUBSCRIPTION_ID" --cloud "$env:CLOUD" --tags "Datacenter=B99,City=Redmond,StateOrDistrict=WA,CountryOrRegion=USA" --correlation-id "$env:CORRELATION_ID";
}
catch {
    $logBody = @{subscriptionId="$env:SUBSCRIPTION_ID";resourceGroup="$env:RESOURCE_GROUP";tenantId="$env:TENANT_ID";location="$env:LOCATION";correlationId="$env:CORRELATION_ID";authType="$env:AUTH_TYPE";operation="onboarding";messageType=$_.FullyQualifiedErrorId;message="$_";};
    Invoke-WebRequest -UseBasicParsing -Uri "https://gbl.his.arc.azure.com/log" -Method "PUT" -Body ($logBody | ConvertTo-Json) | out-null;
    Write-Host  -ForegroundColor red $_.Exception;
}
```



