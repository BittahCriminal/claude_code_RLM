# Azure Management Groups

## What are management groups?

If your organization has many subscriptions, you may need a way to efficiently manage access, policies, and compliance for those subscriptions. You organize Azure subscriptions into containers called "management groups" and apply your governance conditions to the management groups. All subscriptions within a management group automatically inherit the conditions applied to the management group.

<IMG width="600" height="321" style="background-image: none;border-bottom-color: currentColor;border-bottom-style: none;border-bottom-width: 0px;border-left-color: currentColor;border-left-style: none;border-left-width: 0px;border-right-color: currentColor;border-right-style: none;border-right-width: 0px;border-top-color: currentColor;border-top-style: none;border-top-width: 0px;color: rgb(0, 0, 0);font-family: inherit;font-size: inherit;font-style: inherit;font-variant: inherit;font-weight: inherit;height: auto;letter-spacing: normal;line-height: inherit;margin-bottom: 0px;margin-left: 0px;margin-right: 0px;margin-top: 0px;padding-bottom: 0px;padding-left: 0px;padding-right: 0px;padding-top: 0px;text-align: center;text-decoration: none;text-indent: 0px;text-transform: none;vertical-align: bottom;white-space: normal;word-spacing: 0px" alt="tree" src="https://docs.microsoft.com/en-us/azure/azure-resource-manager/media/management-groups/mg_overview.png" border="0"/>

## T&R Implementation of Management Groups

* Microsoft Tenant - The AMG tree is automatically created/maintained/populated to match Service Tree hierarchy. More info here: https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/3493/Azure-Management-Groups-RTE-Command-Control

* PME Tenant - The AMG tree consists of the top level "Technology & Research" group with 3 child AMGs:
** TnR_Transfer - this is the AMG all incoming or outgoing subs should be placed in.
** TnR_DevTest - this is where all development and testing subs should go.
** TnR_Prod - this is where all true production subs should go.
![PME_AMG_Tree.PNG](/.attachments/PME_AMG_Tree-989bc2a1-ea97-4b6d-a3c8-e6745f472dc2.PNG)

### Guiding Principles
* Simple
* Flexible to account for re-orgs
* Allow service owners to control RBAC and their own policies
* Allow security teams to deploy governance to service teams with minimal service team interaction
* Allow for exclusions of each policy
* Should not require service teams do additional work
* Can be used to apply both security and non-security policies
* Be able to manage different environments (Prod/NonProd/Demo/Dev/Test)
* Be used to apply policy to all resource types

## Governance Council 

* TBD

### Related Services

* Azure Blueprints
* Azure Policy
* Azure Cost Management
* Privileged Identity Management (Azure PIM)
* Azure JIT (Support coming - ETA)