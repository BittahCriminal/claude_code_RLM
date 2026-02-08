# Overview 
https://aka.ms/TnRDevOpsRole

The intent of the TnR DevOps Role is to align with the CSEO DevOps Role resource provider actions to minimize potential for future disruption, and a convergence at some point towards a unified DevOps role applied at the tenant level.

## SLO/SLI/KVI

The following are definitions of SLO/SLI and KVI. No actual metrics are available for this service currently.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal;">Developers use a DevOps RBAC role that allows them to productively get work done compliantly with minimal overhead.</span>|
| --- | --- |
| SLI | • How many are using compliant roles?<br>• How many are using non-compliant roles? |
| KVI | How many subscriptions use this role?|

### Methodology:
None of the above have been implemented, more work is needed to create methodologies.

**SLO** -
**SLI** -
**KVI** -

## To Request New Resource Provider Actions

Getting new actions added to the DevOps role is managed by our collaborators in DSRE / Cloud Governance team.

1) Request a **Pull Request** for the specific permission requested for the _"FUN-FS-CPECLR-AzureArtifacts"_ repo. (Email: CSEODevOpsRev@microsoft.com with any questions) 
_[Quarterly Reviews in January, April, July, and November]_
- RBAC Definition/List of Permissions for the role: https://microsoftit.visualstudio.com/OneITVSO/_git/IES-HCC-CLDGOV-CloudGovService?path=/Microsoft.CloudGov.DevOpsRole/DevOpsRole.json
2) In the meantime, you can use the SAW+SC-ALT+PIM approach to elevate into a Privileged role to continue that specific action

[reference link](https://microsoftit.visualstudio.com/OneITVSO/_wiki/wikis/OneITVSO.wiki/14521/Custom-Azure-RBAC-Role-for-Engineers-CSEO-DevOps-Role?anchor=what-if-i-can%27t-still-perform-the-azure-action-desired%3F)

## To Validate resource provider actions

You can check if the DevOps role has the action with the below powerbi link
[PTA Allow Action List](https://msit.powerbi.com/groups/09c37f98-111c-43fa-9367-17bcb71010cd/reports/1c574892-f06f-4ca3-a8b3-11e07985ae21/ReportSection435e12a20a5c3521b8db)
>Every out of box role definition in Azure was evaluated down to the Allow Action level. This custom role definition is an aggregate of my Allow Actions that are specific to Azure resources tailored to developer needs. Follow the PBI link to get a list of all included Allow Actions for the CSEO DevOps custom role.


You can also validate resource provider actions available using powershell
```powershell
#$Provider = "Microsoft.Web"
$Provider = "Replace Me"
(Get-AzRoleDefinition -Name "Tnr Devops Role").actions | select-string $Provider
```

You can see the TnR DevOps role definition we have deployed here:
- https://dev.azure.com/msresearch/MSR%20Engineering/_git/Governance-TnRDevOps?path=/Definitions/TnRDevOpsRole%20-%20TNR%20Management%20Group%20Config.json&version=GBmain

The TnR DevOps Role should be a replica of the actions listed in the CSEO DevOps role:
- https://microsoftit.visualstudio.com/OneITVSO/_git/IES-HCC-CLDGOV-CloudGovService?path=/Microsoft.CloudGov.DevOpsRole/DevOpsRole.json

###What does this role allow me to do?
Every out of box role definition in Azure was evaluated down to the Allow Action level. This custom role definition is an aggregate of my Allow Actions that are specific to Azure resources tailored to developer needs. Follow the PBI link to get a list of all included Allow Actions for the CSEO DevOps custom role. [PTA Allow Action List](https://msit.powerbi.com/groups/09c37f98-111c-43fa-9367-17bcb71010cd/reports/1c574892-f06f-4ca3-a8b3-11e07985ae21/ReportSection435e12a20a5c3521b8db). You can also see the current role definition deployed in production [here](https://microsoftit.visualstudio.com/OneITVSO/_git/E36-MWS-CLDGOV-CloudGovService?path=/Microsoft.CloudGov.DevOpsRole/DevOpsRole.json). 

###Why was the CSEO DevOps Role created?
Prior to the creation of this role, more daily engineering actions were taking place under admin-level role assignments. As we listened to our engineering community and evaluated the developer experience, we realized that SAW devices were very restrictive for many engineering use cases. As more out of box role definitions move to PTA, we wanted to protect the developer experience. The CSEO DevOps Role was created in recognition that engineers do take up certain roles such as DRI that could benefit from having certain permissions with the least amount of friction points. This role has been vetted and approved by the DSRE pre-CISO forum on Dec 2, 2020.

# Work In Progress

## SLO

> Research Development and Engineering teams can seamlessly operate and maintain their projects and services in compliant ways.

This is a #OneMSFT priority and we inherit our requirements from http://aka.ms/ProtectAdmin in coordination with T+R Security and Security Champions.

Over provisioned administrative access puts our resources and company at unacceptable risk. However, draconian security policies decelerate R&D efforts in ways that do not thoughtfully account for how we mitigate risk to the company.

We believe there is a path to a thoughtfully aligned working environment that is both compliant and productive.

## SLI
Additional feedback is welcome. 
These are just examples that could/should be iterated on with data we review.
- 95% of user identities in T+R on subscriptions that are persistent, are setup with T+R DevOps Role
- 100% Compliance on 0 persistent administrators (Owner/Contributor/UAA) on subscription scope

The SEF OKRs are something we could inherit audit results from their key results.

## KPI
- TODO: Validation of our PowerBI report of permissions over time that reflect our SLIs

I believe our collaborators in T+R Security have a dashboard they use to report offenders to us.

We also have a logic app setup however it doesn't appear to be working as expected.