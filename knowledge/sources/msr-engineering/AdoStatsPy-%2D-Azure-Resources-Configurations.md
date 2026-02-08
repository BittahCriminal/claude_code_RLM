## **Introduction**
This page will provide some insights into the setup of crucial Azure resources and components that power the AdoStatsPy project. This includes the AdoStatsPy Function app, Application Insights and Alerts, Service Bus, Storage Account, and PAT token from keyvault.

For all the Azure resources utilized in the project, visit the [**ADOStats**](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/overview) resource group.

## **Function App**
Azure Function App supports a wide range of configuration settings, which are known as "Application Settings." These settings allow us to customize various aspects of the function app, including connection strings to service bus and storage account, authentication, environment variables, and other values that may be required.

Our current function app configuration page [AdoStatsPy - Config Settings](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/adostats/providers/Microsoft.Web/sites/AdoStatsPy/configuration) includes:

![app_settings.png](/.attachments/app_settings-6d4ddb0a-594a-48b2-a5ce-8ce1b32c1954.png)

Which consists of connection endpoints to application insights, service bus, storage, key vault, and other settings.



For a list of all app settings available to us, the official Microsoft Learn page:
[Azure Functions | App Settings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-app-settings)

## Service Bus Configuration

Our TimerTriggerProjectStatus function, instead of storing data in a blob, sends a message to our topic named "projectstatus" within our Azure Service Bus.

When this message is sent to Topic, the Service Bus acts as a mediator and distributes the message to all subscribed functions; each of the three TopicTrigger functions receives a copy of the message and begins processing it independently.

To view our adostatspy service bus topic and subscribed functions: [projectstatus](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/providers/Microsoft.ServiceBus/namespaces/adostatspy/topics/projectstatus/overview)

## Storage Account and Container

The [AdoStatsPy Storage Account](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/providers/Microsoft.Storage/storageAccounts/adostatspy/overview) plays a vital role in serving as a resting place for JSON files produced by four of our functions: TimerTriggerPrincipal, TopicTriggerGitDataStatus, TopicTriggerWikiStatus, TopicTriggerWorkItemStatus.

The [timertriggerprincipal](https://ms.portal.azure.com/#view/Microsoft_Azure_Storage/ContainerMenuBlade/~/overview/storageAccountId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2FADOStats%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Fadostatspy/path/timertriggerprincipal/etag/%220x8DB8C7D322B0C38%22/defaultEncryptionScope/%24account-encryption-key/denyEncryptionScopeOverride~/false/defaultId//publicAccessVal/None) container within the Storage Account serves as the dedicated location where these blob files are securely stored.

## Alerts based on Application Insights

Application Insights is an Azure service that allows us to monitor our application in real time and enabling us to get insights into our function's performances.

The service also provides logs that capture very detailed telemetry data from the various components of the application. These logs are invaluable for troubleshooting any issues in the functions, and even allow us to set up very specific alerts.

For example, here's logs for an execution of TimerTriggerProjectStatus:

![app_logs.png](/.attachments/app_logs-400c836e-4a7f-4a35-b2f3-0d551a63eaea.png)

If we wanted to write an alert based on logs, which would alert us when TimerTriggerProjectStatus has a successful execution, we could pinpoint in the logs fields which indicate a successful run:

![app_logs2.png](/.attachments/app_logs2-6ab3951c-6dbb-487c-93d6-3c9437b46d86.png)

In this case, "prop__status" within "customDimensions" indicates that the runtime was successful.

We could use this information to write a query that will filter for this specific case:

![app_logs3.png](/.attachments/app_logs3-26241987-9d60-4a44-9d17-2af0ac65bde7.png)

Similarly, we could query the logs for any form of metrics we can expect our functions to encounter. Using these queries, we could create conditional alerts that will trigger when the desired metrics are found in the logs.

To view our custom alert rules for the AdoStatsPy Application Insights: [Alerts](https://ms.portal.azure.com/#view/Microsoft_Azure_Monitoring_Alerts/AlertRulesBlade/resourceId/%2Fsubscriptions%2F7bdcf9ec-4326-408b-a69b-c7235c63b5e8%2FresourceGroups%2FADOStats%2Fproviders%2Fmicrosoft.insights%2Fcomponents%2FAdoStatsPy)

Alerts are configured to utilize the [EmailNotify](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/providers/microsoft.insights/actiongroups/EmailNotify/overview) action group, which specifies the msradom account as the email address to send alerts to.