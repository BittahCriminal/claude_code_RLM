
# Creating a secure Function app with a Flex Consumption Plan

## Pre create

## VNET
- You can also pre-create a VNET to be used with the Azure Function (see networking). This is used for funneling all traffic from your Azure Function through so you can effectively firewall all storage account traffic from one VNET.
- If you do this, ensure you also create an NSG for the subnet in your VNET or you'll be flagged by S360.
- You'll also need to ensure 2 subnets exist. You can use the default one for the function apps.
- To meet Wave4/Wave5 KPI requirements to lock down storage accounts, you'll want to make a dedicated subnet to be used by the storage account private endpoint.

## Storage Account Considerations
- You'll need to pre-create a storage account for this. You can create a separate deploy and configuration account since it uses a storage account for both of those actions, and can be separate. It's fine to create the same as well.
  - Ensure you use the system assigned identity and give it Storage Account Blob Contributor access.
  - Ensure you precreate the container you plan on using for the `az functionapp create` command.
  - Create a private endpoint in the subnet you created above.
  - Once you've finished the "Networking" step below, you can go to the storage account's "Network" blade, and in the "Firewalls and virtual networks" and set "Public network access" to disabled. The DNS for the VNET will still resolve the `<storage>.blob.core.windows.net` name internally to the private address to the VNET. Test the function app once you've done this to ensure it's working.


## Environment variables
- Ensure that ansible_req_client_id is changed to the new "artifactsaccess" uami
- `AzureWebJobsStorage` needs to be changed to `AzureWebJobsStorage_accountname` with just the storage account name as the value (like `gcrarconboardingtest`) for it to work with MI.

## Configuration
- Ensure this is set to https only

## Networking
- You can lock down the storage account further by clicking on "virtual network integration" and associating a VNET with the outbound traffic. This will allow you to set filtering on the storage account.
	- Under "Networking" in the storage account, you can set "Enabled from selected virtual networks and IP addresses" and use the VNET you created above.
	- This won't affect your ability to deploy from VS Code.

### Restricting to Azure Front Door
You can restrict the Function App to just Azure Front Door
Be sure to match the header with your Azure Front Door ID which can be found in the Azure Portal overview page.
```bash
az functionapp config access-restriction add -g gcr-arc-onboarding-test -n gcr-arc-onboarding-test2 --priority 100 --service-tag AzureFrontDoor.Backend --http-header x-azure-fdid=3726af32-7237-2496-a431-a1aeb266a5de
```

## Code
- Ensure your requirements.psd1 is simply:
```powershell
@{}
```
  Linux doesn't support this file, but your deployment will also fail without it.


## Creation
### Storage Account
```bash
az storage account create \ 
	--name gcrarconboardingtest \ 
	--location eastus \ 
	--resource-group gcr-arc-onboarding-test \ 
	--sku Standard_LRS \ 
	--allow-blob-public-access false
```

### Function App
```bash
az functionapp create \
--resource-group gcr-arc-onboarding-test \ 
--name gcr-arc-onboarding-test \ 
--storage-account gcrarconboardingtest \ 
--flexconsumption-location eastus \ 
--runtime powershell \
--runtime-version 7.4 \
--deployment-storage-name gcrarconboardingtest \ 
--deployment-storage-container-name gcr-arc-onboarding-test-deploy \ 
--deployment-storage-auth-type SystemAssignedIdentity
```


Adding rules to the function app for only front door and ADO:
```bash

az functionapp config access-restriction add -g gcr-arc-onboarding-test -n gcr-arc-onboarding-test2 --priority 100 --service-tag AzureFrontDoor.Backend --http-header x-azure-fdid=3786ae12-7737-4456-a531-c1aef266a5de
```

```bash

export FUNCTION_KEY="YOUR_KEY_HERE"
curl -S https://gcr-arc-onboarding-frghdffpbfd9bjd8.b01.azurefd.net/api/gcr-arc-onboarding-req?code=$FUNCTION_KEY
```

## Deployment
The following variables in the Azure Functions will make it unable to use VSCode to deploy to the site:
```
WEBSITE_ENABLE_SYNC_UPDATE_SITE=true
WEBSITE_RUN_FROM_PACKAGE=1 
```

`WEBSITE_RUN_FROM_PACKAGE` isn't supported with Flex Consumption, and will make the deployment fail.
`WEBSITE_ENABLE_SYNC_UPDATE_SITE` will make it so that VSCode is unable to find the deployment.

### Use of `az functionapp deployment source config-zip`
If you use this command:
```bash
az functionapp deployment source config-zip -g gcr-arc-onboarding-test -n gcr-arc-onboarding-test --src publish.zip
```

You'll see the following:
```
Getting scm site credentials for zip deployment
Starting zip deployment. This operation can take a while to complete ...
Deployment endpoint responded with status code 202 for deployment id "2e6bd2f3-fcf6-453e-9e3f-e5b4e1d67577"
Waiting for sync triggers...
Checking the health of the function app
```
And it'll hang there indefinitely.

There are two aptions:
1. Timeout command
You can use the timeout command to assist with this command exiting
```bash
timeout 300 az functionapp deployment source config-zip -g gcr-arc-onboarding-test -n gcr-arc-onboarding-test --src publish.zip
```
2. Open and Close the Firewall
This is what I chose in the end. If you open and close the firewall for the function app during deployment, you won't end up with delayed issues. I kept the timeout because I know it's possible for the app to hang indefinitely, and I want to remove any chance of that.
```bash
az functionapp config access-restriction set --resource-group gcr-arc-onboarding-wus2-1 --name gcr-arc-onboarding-wus2-1 --use-same-restrictions-for-scm-site true --default-action Allow --scm-default-action Allow
timeout 300 az functionapp deployment source config-zip -g gcr-arc-onboarding-test -n gcr-arc-onboarding-test --src publish.zip
az functionapp config access-restriction set --resource-group gcr-arc-onboarding-wus2-1 --name gcr-arc-onboarding-wus2-1 --use-same-restrictions-for-scm-site true --default-action Deny--scm-default-action Deny
```

## Debugging
One useful tool in debugging is the "live metrics" feature of the Azure Function. You can use this to see if your app is healthy. In my case, I found there was a bug which was causing an exception on each request made, which caused the request duration to increase but about 100ms.

You can find this in the Application Insight object for your Azure Function:
![image.png](/.attachments/image-b9cfd755-9e43-4621-8f27-542ec20f221d.png)


# Azure Front Door Considerations
When creating an Azure Front Door. You'll need to make a WAF profile, likely one that includes the bot firewalls. S360 will also insist that you create a rate limiting rule as well.

The WAF policy will be created as a separate Azure object from the front door one, keep this in mind when naming it.
![image.png](/.attachments/image-805c3908-768a-4df6-a338-1ceae69dfc04.png)

Clicking into the Custom Rules, you can make or view rules that you've made. S360 recommends a rate limit duration of 5 minutes, with a threshold appropriate to your app. I was thinking I wanted no more than 10 requests a second, so I made the rate limit threshold 3000 as seen below:
![image.png](/.attachments/image-ee5e14ff-375f-4664-a099-b4427a329937.png)

## Looking for blocked requests:
Also when testing your app, you'll want to ensure requests aren't getting blocked. I found quite a few blocked requests initially with my app. There's a handy page to view them here:
![image.png](/.attachments/image-5da33bec-97e4-49b9-8316-531d4e18811e.png)

If you find blocked requests, then you'll need to investigate them. I'd recommend creating a separate Log Analytics Workspace to put these in. Then from the Azure Frontdoor instance Go to the "Diagnostic Settings" blade, and click "Add diagnostic setting". Ensure that you check "FrontDoor WebApplicationFirewall Log" and check "Send to Log Analytics Workspace".

Once this is created wait about 10-15 minutes. You'll want to go to the "Logs" blade from Azure FrontDoor, and use this query:
```kql
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.CDN" and Category == "FrontDoorWebApplicationFirewallLog" 
| where action_s == "Block"
```

This will show you your blocked queries. If you don't see them, then the requests aren't being sent to the LAW, either wait, or if it's been a while, try recreating the Diagnostic Setting. I've seen an instance where this didn't work the first time.

You can click into the items of your blocked query, and get some good information about them. However if you want to dig deeper, you'll need the trackingReference:

![image.png](/.attachments/image-3806af13-ee44-4f23-9760-6cedc112586e.png)


Use this query once you have the tracking reference, and you can dig into why the query was blocked:

```kql
AzureDiagnostics
| where trackingReference_s == "20241004T214018Z-r1d78bdccbft94dvp2k39ammbs0000000u4g00000000cg3x"
| project TimeGenerated, Category, ruleName_s, action_s, trackingReference_s
| order by TimeGenerated desc
```

In the case below, you can find that there are two rules that were triggered in blocking the query:
![image.png](/.attachments/image-0574312e-b5c1-480a-b534-5609db9296de.png)


When looking at the blocked reasons, this page is handy:
[Application Gateway CRS Rulegroups](https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/application-gateway-crs-rulegroups-rules?tabs=drs21)


In the above case, one of the reasons was due to "GET or HEAD Request with Body Content.". I found the query was sending content not needed, so I turned it off. I've also seen requests being flagged for "920300 - Request Missing an Accept Header", so you'll need to be sure that your http queries use an [`Accept` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept) so they don't get rejected.

# References:
- [Azure Functions Flex Consumption plan hosting | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan#considerations)
- [Create and manage function apps in a Flex Consumption plan | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-how-to?tabs=azure-cli%2Cvs-code-publish&pivots=programming-language-powershell#view-currently-supported-regions)
- [FY25 Level Up Flex Consumption.pptx (sharepoint.com)](https://microsoft.sharepoint.com/:p:/r/teams/LevelUpSkilling/_layouts/15/Doc.aspx?sourcedoc=%7B5602015D-9233-4396-9BC4-8692416342E9%7D&file=FY25%20Level%20Up%20Flex%20Consumption.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1)
- [Create a function app without default storage secrets in its definition - Azure Functions | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial)
- [Best practices for Azure Web Application Firewall in Azure Front Door | Microsoft Learn](https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/waf-front-door-best-practices)
- 