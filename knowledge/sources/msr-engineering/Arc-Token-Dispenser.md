# Introduction
This service aims to cover a gap in the security features offered with Azure Arc. This service allows a simulation of the user assigned managed identity. The service is a simple azure function which distributes UAMI tokens in order to authenticate with Azure Services. This service is needed because due to the Safe Secrets Standard KPI we are no longer able to use app registrations with secrets. The access tokens are used to [authenticate with Azure Services](https://learn.microsoft.com/en-us/rest/api/azure/#acquire-an-access-token) via REST.

## Azure Arc Security Gaps
- Azure Arc does not support User Assigned Managed Identities
- Azcopy cannot work with Azure Arc MSIs
- `Az login` command cannot work with Azure Arc MSIs
- Without App Registration secrets, the only way to register an Azure Arc host is [via access tokens](https://learn.microsoft.com/en-us/azure/azure-arc/servers/azcmagent-connect#access-token).

## Token Details
This token dispenser has a number of endpoints detailed below, which dispense tokens to be used with REST requests. In limited testing, it's been found that the token lifetimes are around 24 hours. Though in [their documentation](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens#token-lifetime) it says _"the Microsoft identity platform assigns a random value ranging between 60-90 minutes (75 minutes on average) as the default lifetime of an access token"_.

## Service Lifetime
This service can be sunset once:
- Azure Arc has a method to onboard hosts without access keys or App Registration secrets. This will make the gcr-arc-onboarding endpoint obsolete.
  - Current guidance is to use certificates, which isn't much more secure than this service.
- Azure Arc supports User Assigned Managed Identities. This will make many of the other endpoints obsolete, as long as the rest of the below listed issues are solved.
  - Without UAMIs, we would have to put all 350 Arc hosts into a number of RBAC roles. RBAC has a subscription limitation of 4000 entries. Putting these permissions would put pressure on the RBAC limits and violate [RBAC Best Practices](https://learn.microsoft.com/en-us/azure/role-based-access-control/best-practices). Also, each RBAC role viewer would be clogged up with all the Arc hosts.
  - There is currently some guidance than Azure Arc can use Federated Identity Credentials (FIC).[¹](https://stackoverflow.microsoft.com/questions/398679). One can stack Service Principals under an App Registration with FIC, however given that App Registrations and FIC are all manipulated with Microsoft Graph, one won't easily get permissions to programatically manipulate FIC members in App Registrations. There is a way to have FIC members under a User Assigned Managed Identity, however policy doesn't allow FIC members that are part of the same tenant.

# Azure Details
This service uses a consumption flex azure function so that it can use an IP restriction service to limit where requests come from. For security, the function apps have themselves completely firewalled to the Azure Front Door instance. This is temporarily brought down and then back up during deployments.

### Azure Front Door Profile
This allows two or more Function Apps to be used. This provides advantages of being able to roll out changes without downtime, or being able to recreate a function app if one was corrupted. It also has a number of security features enabled to prevent hacking of the app. Finally, the geo-location features have this limited to only US. There's no way to use NSG style service tags to limit this just to corpnet, which would be my preference.
- [gcr-arc-onboarding](https://ms.portal.azure.com/?l=en.en-us#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/arc-onboarding/providers/Microsoft.Cdn/profiles/gcr-arc-onboarding/overview)

A sample Azure Front door URL:
`https://gcr-arc-onboarding-frghdffpbfd9bjd8.b01.azurefd.net/api/gcr-arc-onboarding-req?code=$FUNCTION_KEY`

- Azure Front Door has been configured to send all logs to the [arc-onboarding-LAW](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/arc-onboarding/providers/Microsoft.OperationalInsights/workspaces/gcr-arc-onboarding-law/Overview). This allows to analyse traffic for service metrics, it also allows for debugging in case any valid traffic is blocked.
- This instance also has bot blocking configured, as well as rate limiting, as required by S360.

### Azure Functions:
Both functions are deployed to the closest datacenter to our on-prem assets, westus2.
- [gcr-arc-onboarding-wus2-1](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/gcr-arc-onboarding-wus2-1/providers/Microsoft.Web/sites/gcr-arc-onboarding-wus2-1/appServices)
- [gcr-arc-onboarding-wus2-1](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/gcr-arc-onboarding-wus2-2/providers/Microsoft.Web/sites/gcr-arc-onboarding-wus2-2/appServices)

- Each Azure Function has a VNET configured that all of its traffic goes through.
- Each Function app's network configuration blocks all traffic except for that coming from the Azure Front Door instance.
- Each Azure Function has a storage account it uses for storing its data and using for deployments. Each Azure Function's storage account has private endpoints deployed to a dedicated subnet, and public net access is turned off for SFI Wave4 compliance.

- The Azure Function has Application Insights enabled, and is able to view all queries made to the function. By default, Application Insights doesn't log the IP address of requests (due to GDPR) without some changes made, which as been done using the command below:
```bash
az rest --method patch --url "https://management.azure.com/subscriptions/46e0b8e9-eb7f-4bbf
-af34-a502c2d310f7/resourceGroups/gcr-arc-onboarding-sc/providers/microsoft.insights/components/gcr-arc-onboarding-sc?api-version=
2018-05-01-preview" --body '{ "location": "SouthCentralUS", "kind": "web", "properties": { "Application_Type": "web", "DisableI
pMasking": true } }'
```

### Codebase: [Azure_Function-arc_token_dispenser](https://dev.azure.com/msresearch/MSR%20Engineering/_git/Azure_Function-arc_token_dispenser)

This service is written entirely in Powershell for better accessibility than Go since it's a relatively uncomplicated service and doesn't need to be highly performance oriented. Requests are typically processed by the function app in under 10ms.

## Token Access
All token endpoints must use an App Key to access them. The App Keys can be found on the [Azure Portal](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/gcr-arc-onboarding-sc/providers/Microsoft.Web/sites/gcr-arc-onboarding-sc/functionsAppKeys).

All token repsonses can be made manually using `curl` like so:
```bash
curl https://gcr-arc-onboarding-sc.azurewebsites.net/api/$ENDPOINT?code=$APP_KEY`
```

Responses will be output in JSON like so:
```json
{
  "access_token": "fo3lieshootha7AenioL4yie6sahnee3loo0aix1ahgoo9toosa1ahzaifahpawaikoocophaenaeGh6EiGaenohg4no8aekeis5okoepohxae2isheet9EijooChahc7Aivifeu1eine2itieg7aegie0xu2yoh3Eeha3wienuth0shaeroo7thie9mao9CaiNg6iithoch0ievahghahNg7aimokaeHalouyoh1yoo9xa0jahR0shufoohudu2thaiyeeXahpheageeth3oQua2vae8pieC0Aph9ieThie3pae9shooD1ohqu0ooch2eetoh7ainohWiuv0shahPoothaizuvaiteaghiaGeeToht2OhYi4leir8etio0Ieliyaedefiepiey6ei6aechae1nan3ohlae4aijaisheiw4ZoCh2aib7eeg1oojeemaiWaik9Tith6oy4iese0fosaic5iZohgaiqua9Vietee8eeloo2aeGheitaipejae3enous3mieNeKoo5Ajiesoe7ahSoo4Le2aZoh3ohCei4ingog7ies0ieraidad4eo8wi6ach0loh7an4eiph7xai9geiw7shah6molaisahfaikeere0Hue0oogh4shoova5eesh8lahYuMei5eevaiyie4Yoe8ic5aich3JeiG5eeph5jiuwael1aishighudiomaivoh8daem9veihiuph0uophohng3eimeequieth0oFeigoHaoyei8naiqu4dei7nei0zeiwohcieghooqu0keu4ooy0hohf7phei5aibohk8tha1rutheewohb3Ear8Aipie2ahbaiQu1iechovai7ma8afaeZa0eeTh9iishooc9Fiepie2thezoong7Wesai8eete5iehaiYeeJeiFohdahG0mei2aiCheifevaxe6noo1shu1uosh5zic6reiZu5ijoonaej8iphaipooTh5eithakao8Iesee3Phah2aL8Xif5mai2Daike1oosheng6yeseseecae1uux1vuFaiT9haeSheNgebaeng5aigievohnoh7FohW5ju1luo8iehieTe1Woo4uf1uatah3shaitheisheifaix3mevaepaiMie0boocu0UFaengefahhiazailaichar8Aedo2yei3Oofieniu1Ug9neicahs0tishoath1woo0Iish8Geichiezefaeshai4chi6bejootee8IF8oot9AtaiquaNgieg7eech6aedeethuc8wooqu6uqueew8hee7gepaodapah4uuphah4Tohsu0ne5haig5ooxaeweeQuee4KuaH1ooNg0xiez7ti0magaeph4eech4Oev6miezeefah8Ieb1eem4chaiy6ri0phevahvuo4ro4sheechoh0ve2ieG4eel2xoh3yae0aijohhoht8rathohmainie0zeik7oiNgohpie2aagh5saughe7rei1Vaveughahphah7",
  "expires_on": "1714492947",
  "resource": "https://management.azure.com/",
  "token_type": "Bearer",
  "client_id": "1C4ABB91-03B2-4C75-9770-9D762B9D203A"
}
```

## Implementation Details
- When using the service, the App Key should at all times be treated as a secret and be encrypted when used as part of other services.

## Token Endpoints
UAMI here means User Assigned Managed Identity.
LAW here means Log Analytics Workstation.

The token endpoints are as follows:
- **ansible-mgmt-req** - Gives a token from the [ansibleaccess](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-ansible/providers/Microsoft.ManagedIdentity/userAssignedIdentities/gcransibleaccess/overview) UAMI under the https://management.azure.com/ context, for ARM requests.
  - Service Supported: [Ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/2282/Ansible)
- **ansible-mon-req** - Gives a token from the [ansibleaccess](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-ansible/providers/Microsoft.ManagedIdentity/userAssignedIdentities/gcransibleaccess/overview) UAMI under the https://monitor.azure.com/ context. Used for primarily Log Analytics Workstation access. In this case, for the [service-metrics](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/service_metrics/providers/Microsoft.OperationalInsights/workspaces/servicemetrics-law/Overview) LAW.
  - Service supported:
    - [Ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/2282/Ansible) - For logging Ansible metrics for the service QBR.
    - [Keyvault SSH Integration](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/811/Keyvault-SSH-integration) - For logging Keyvault SSH Metrics for the service QBR.
- **ansible-stor-req** - Gives a token from the [ansibleaccess](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-ansible/providers/Microsoft.ManagedIdentity/userAssignedIdentities/gcransibleaccess/overview) UAMI under the https://storage.azure.com/ context. Used for accessing the [gcransible](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-ansible/providers/Microsoft.Storage/storageAccounts/gcransible/overview) storage account.
  - Service Supported: [Ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/2282/Ansible) - For downloading binary artifacts and install scripts.
- **ansible-vault-req** Give a token from the [ansibleaccess](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-ansible/providers/Microsoft.ManagedIdentity/userAssignedIdentities/gcransibleaccess/overview) UAMI under the https://vault.azure.net context. Use for accessing the [GCRCMVault](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/GCRCMVault/providers/Microsoft.KeyVault/vaults/GCRCMVault/overview) and [gcrauthvault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/gcrauthvault/providers/Microsoft.KeyVault/vaults/gcrauthvault/overview) keyvaults.
  - Services Supported: [Ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/2282/Ansible), [Keyvault SSH Integration](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/811/Keyvault-SSH-integration)
- **gcr-arc-onboarding-req** - Gives a token from the [GCRArcOnboardingUAMI](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/arc-onboarding/providers/Microsoft.ManagedIdentity/userAssignedIdentities/GCRArcOnboardingUAMI/overview) endpoint under the https://management.azure.com/ context. Used primarily to onboard Arc hosts into Azure.
  - Service Supported: GCR Sandbox - Arc Onboarding to Azure
- **gcr-arc-onboarding-vault-req** - Gives a token from the [GCRArcOnboardingUAMI](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/arc-onboarding/providers/Microsoft.ManagedIdentity/userAssignedIdentities/GCRArcOnboardingUAMI/overview) endpoint under the https://vault.azure.net context. Used primarily to onboard Arc hosts into Azure.
  - Service Supported: GCR Sandbox - Arc Onboarding to Azure.
- **gpumetrics-mon-req** - Gives a token from the [gpumetricsaccess](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/gpumetrics/providers/Microsoft.ManagedIdentity/userAssignedIdentities/gpumetricsaccess/overview) UAMI under the https://monitor.azure.com/ context. Used for primarily Log Analytics Workstation access. In this case, for the [gpumetrics](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/gpumetrics/providers/Microsoft.OperationalInsights/workspaces/gpumetrics/Overview) LAW.
  - Service Supported: [GPU Metrics](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4220/GPUmetrics-service)
- **samle-mon-req** - Gives a token from the [samleaccess](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/samle/providers/Microsoft.ManagedIdentity/userAssignedIdentities/samleaccess/overview) UAMI under the https://monitor.azure.com/ context. Used for primarily Log Analytics Workstation access. In this case, for the [samle-law](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/samle/providers/Microsoft.OperationalInsights/workspaces/samle-law/Overview) LAW.
  - Service supported: [samle](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/7396/Samle-Monitoring)


# References
- [Connect azcmagent with Access Token](https://learn.microsoft.com/en-us/azure/azure-arc/servers/azcmagent-connect#access-token)
- [Authenticate against Azure resources with Azure Arc-enabled servers](https://learn.microsoft.com/en-us/azure/azure-arc/servers/managed-identity-authentication)
- [Identity and access management for Azure Arc-enabled servers](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/hybrid/arc-enabled-servers/eslz-identity-and-access-management)
- [Access tokens in the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
- [Microsoft Access Token Decoder](https://jwt.ms/)
- ¹[Microsoft Stack Overflow - Flexible FIC](https://stackoverflow.microsoft.com/questions/398679)
- ²[Using Federated Identity Credentials (FIC) with App Registrations](https://dev.azure.com/msresearch/Security%20Champs/_wiki/wikis/Security-Champs.wiki/13219/Using-Federated-Identity-Credentials-(FIC)-with-App-Registrations)