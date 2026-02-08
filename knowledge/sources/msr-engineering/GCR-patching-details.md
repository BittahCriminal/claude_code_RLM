

**This page has been Deprecated on 4/17/2024 refer to this [page](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/8580/SES-Patching-Scope) for current SES patching scope**



**Azure automation account for GCR patching**: [GCR-automation](https://ms.portal.azure.com/#@72f988bf-86f1-41af-91ab-2d7cd011db47/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-automation/providers/Microsoft.Automation/automationAccounts/gcr-automation/overview)

**Log Analytics workspace for GCR patching**: [GCR-patching](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/40641f8d-33f8-4948-b0ae-3df7e85e94e9/resourcegroups/gcr-patching/providers/microsoft.operationalinsights/workspaces/gcr-patching/Overview)

**Workspace id:** 383511da-50b6-4c5b-afef-8b2295dbc42b

**Workspace location:** West US 2

**workspace subscription :** Grand Central resources production 2

**List of clusters that are onboarded and part of Azure patch management as of 10/13/2022**


**Azure GPU Linux VMs GCRprodex2 subscription:**

GCRAZGDL1XXX **RG** GPU-SANDBOX and GPU-SANDBOX2

**Azure GPU Linux VMs GCRprodex3 subscription:**

GCRAZGDL2XXX **RG** GPU-Sandbox 

**Azure CPU Linux VMs GCRprodex1 subscription:**

GCRAZCDLXXX **RG** CPU-Sandbox 

**Azure CPU Windows VMs GCRprodex1 subscription:**

GCRAZCDWXXX **RG** CPU-Sandbox 



Note: **For patching the above you must schedule 2 patch deployment one for all Linux nodes and one for All Windows nodes and include their current resource group**

# Systems and Services Not covered

**OnPrem Nodes managed by MLS team:**

-  Linux Onprem GCRSANDBOX*** ( GCRSANDBOX1XX && GCRSANDBOX2XX && GCRSANDBOX3XX ) - Moved to MLS patching by Steve not part of GCR patching anymore. 12/20/2021

- All GCR-SANDBOX && MSR-SANDBOX onprem.  2/14/2022

