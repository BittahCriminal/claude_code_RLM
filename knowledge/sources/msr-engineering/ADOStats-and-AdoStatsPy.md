#What is it?
**AdoStatsPy** is an Azure App Service that is intended to support our Azure DevOps reporting by retrieving data from the ADO API.
[**ADOStats**](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/overview) is the resource that contains this app service and its supporting infrastructure, a service bus, key vault and a blob store.

Source code for the functions can be found in the [AdoStats](https://dev.azure.com/msresearch/MSR%20Engineering/_git/AdoStats) repository.

Inside of AdoStatsPy are a small collection Azure Functions on timers that execute daily. These functions are:
* [TimerTriggerProjectStatus](https://ms.portal.azure.com/#view/WebsitesExtension/FunctionMenuBlade/~/functionOverview/resourceId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2Fadostats%2Fproviders%2FMicrosoft.Web%2Fsites%2FAdoStatsPy%2Ffunctions%2FTimerTriggerProjectStatus), triggered on a timer to retrieve a list of projects along with details like project name, ID, last change, and then sends this data as a message through a service bus topic.
* [TopicTriggerGitDataStatus](https://ms.portal.azure.com/#view/WebsitesExtension/FunctionMenuBlade/~/functionOverview/resourceId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2Fadostats%2Fproviders%2FMicrosoft.Web%2Fsites%2FAdoStatsPy%2Ffunctions%2FTopicTriggerGitDataStatus), which triggers upon receiving message from service bus topic and then gathers Git-related data about each project, formatting into JSON and outputting as a blob into our storage account.
* [TopicTriggerWikiStatus](https://ms.portal.azure.com/#view/WebsitesExtension/FunctionMenuBlade/~/functionOverview/resourceId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2Fadostats%2Fproviders%2FMicrosoft.Web%2Fsites%2FAdoStatsPy%2Ffunctions%2FTopicTriggerWikiStatus) Similar to GitDataStatus, but pulls data on wiki names, recent changes, and authors for each project. 
* [TopicTriggerWorkItemStatus](https://ms.portal.azure.com/#view/WebsitesExtension/FunctionMenuBlade/~/functionOverview/resourceId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2Fadostats%2Fproviders%2FMicrosoft.Web%2Fsites%2FAdoStatsPy%2Ffunctions%2FTopicTriggerWorkItemStatus) Similar to GitdataStatus, but pulls data on most recent work items, count of modified work items, and last project changes.
* [TimerTriggerPrincipal](https://ms.portal.azure.com/#view/WebsitesExtension/FunctionMenuBlade/~/functionOverview/resourceId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2Fadostats%2Fproviders%2FMicrosoft.Web%2Fsites%2FAdoStatsPy%2Ffunctions%2FTimerTriggerPrincipal), which triggers on a timer and retrieves details on all project administration groups and users associated with these groups for each project. The collected data is formatted into JSON and stored as a blob.

# Authentication and Authorization
All functions run using a personal access token (PAT) for a service account, msradom@microsoft.com. 

If you have questions regarding service account PAT, contact @<CF599EAD-570E-4E54-829B-A84AAF63D4CC> 


# MSRadom Service Account
Information including credentials and access to the service account: msradom@microsoft.com 

- Current owners of the account: @<768B9E72-CDD5-4BA5-B577-B30ABB4C6B8A>, @<B054BF3E-4FEF-461C-8B29-DD83807B59CA>, @<CF599EAD-570E-4E54-829B-A84AAF63D4CC> 

- Credentials for the account can be found in ADOStats Keyvault secret: [MSRADOM-Svc-Account](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://adostats.vault.azure.net/secrets/MSRADOM-Svc-Account/9e38be6a30cc4ac2b3f1adccdff64cd2) under "Secret Value".

- Account PAT can also be found stored as a secret in the [ADOStats Keyvault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/providers/Microsoft.KeyVault/vaults/ADOStats/secrets) under [ADO-PAT](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://adostats.vault.azure.net/secrets/ADO-PAT/de266737e1114d209b822bc215399b25)

- Account set to expire on **05/04/2024**, extension and other settings can be configured on [CoreIdentity](https://coreidentity.microsoft.com/manage/Service/redmond/msradom)

# Making Changes
To make changes to these functions, I recommend the following steps:
1. Install the Azure Functions extension for Visual Studio code
1. Clone this repository
1. Open the *folder* using VSCode. _Not the file!_
1. Make the appropriate changes to the code or configuration
1. Test locally
   1. Press F5 with the project folder loaded and VSCode will launch a local server that emulates the Azure Function cloud architecture.
   1. Wait. The server takes about 15-20 seconds to start. 
   1. On the far-left nav bar in VSCode, select **Azure** ![image.png](/.attachments/image-beccd854-50c6-4046-a337-b796b065e9f5.png), then right click on the name of the function you've changed, and select **Execute function**.
![image.png](/.attachments/image-bdfd4227-8948-4314-943d-c28b51d188cd.png)
   * If you have any errors in your code, this will not go smoothly, and you'll get some odd dialog boxes and then you'll get your error after you wait a while if you try to force it through.
1. Upload your modified function to Azure. See screenshot below for reference
![image.png](/.attachments/image-73f8f1c5-f930-4ba5-907c-8b2e72a5d0ea.png)
1. It will look like nothing has happened, but VSCode's command palette (see screenshow) should be open and showing you a list of subscriptions you have access to. Select Microsoft Research Engineering.
![image.png](/.attachments/image-9bf121e4-a37a-41c7-9530-308091653319.png)
Note: If you don't have access to the _Microsoft Research Engineering_ subscription, you'll need to resolve that.
1. When prompted for Azure App Service (again in the command palette) select *AdoStatsPy*.
1. VSCode may/will prompt you with a number of dialog boxes that are either obvious or don't matter. Click through these.
![image.png](/.attachments/image-1054c77c-843f-4e40-bd14-4353e2b45087.png)
1. Deployment will start, and takes about a minute.

# PowerBI
Our PowerBI report is based on the JSON files generated from our funcions, and directly draws from the most up-to-date JSON files in the timertriggerprincipal container.

[PowerBI Report](https://msit.powerbi.com/groups/fd26e2e0-b498-478b-ac30-039597e1c8b7/reports/3acafad2-138e-49a2-920d-729ff0f9b2b0/ReportSection?experience=power-bi)

