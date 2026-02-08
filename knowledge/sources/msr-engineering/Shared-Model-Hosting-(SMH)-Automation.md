# Introduction

The Shared Model Hosting service under TRAPI currently requires manual intervention when the models hosted expire. Models will not self-delete when expired, and we have nearly 90 hosted models as of this writing. Thus, automating their deletion when they're about to expire is preferred.

# Scope of endpoints with deletion candidates.
The scope of hosting exists in the Azure Management Group [GCR Azure OpenAI](https://ms.portal.azure.com/#view/Microsoft_Azure_Resources/ManagmentGroupDrilldownMenuBlade/~/overview/tenantId/72f988bf-86f1-41af-91ab-2d7cd011db47/mgId/007c1c50-b506-42e9-963d-95495e3b23e9/mgDisplayName/GCR%20Azure%20OpenAI/mgCanAddOrMoveSubscription~/false/mgParentAccessLevel/Reader/defaultMenuItemId/overview/drillDownMode~/true).

# Solution
Solution Location: [smh-expirations-removal Logic App](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/f0f57942-516a-458e-81d7-7e35ff68dbf1/resourceGroups/SMH-Automations/providers/Microsoft.Logic/workflows/smh-expirations-removal/logicApp)

The above logic app has some configurable parameters which can be found by going to the Logic App Designer blade, and clicking "Parameters":
- daysThreshold - Default 3
  - This configures in how many days a model is to expire before it's deleted.
- testMode - Default value: fales
  - When set, this will run through all actions, but no endpoints will be deleted. A different deletion notice will be sent to the teams channel indicating it's in test mode.


The Azure Logic App which runs daily. This will scan the AOAI endpoints in the above management groups. If any are found to be expired in 3 days, they will be deleted.

When deletion is going to occur, a message in the RTE Private "RTE Service Alert ⛑️" channel will be posted. This is owned by krisz since these hooks can't be owned by a non-person account. The message is in in a similar form as as below:


**🚨 Azure Cognitive Services Model Expiration Alert**
Found **1** deployment(s) with models expiring within **15** days.
**Action:** ❌ Deployments have been deleted

* * *

**📋 Deployment 1:**
**📍 Endpoint:** gcraoaitest1 (swedencentral)
**🔹 Subscription:** 22e98ff1-16b4-4e29-9c76-421aed706f94
**🔹 Deployment:** gpt-4o-realtime-preview_2024-12-17
**🔹 Model:** gpt-4o-realtime-preview v2024-12-17
**🔹 Expires:** 2025-07-02T00:00:00Z
**🔹 Resource Group:** gcrgpt4azureopenai-swc

* * *

_Generated at 2025-06-17T22:57:09.2911198Z_


