## This guidance is scoped at the internal Microsoft resources (Microsoft AAD tenant, Azure DevOps internal organizations).

### Legal Compliance Privacy Approval
TODO: Add note on what the CELA/compliance/Privacy* process is + contacts.

- AI+R Legal: [Collaboration Guidance Document](https://microsoft.sharepoint.com/:w:/r/teams/TnRInternal/_layouts/15/Doc.aspx?sourcedoc=%7B290A96D4-7715-4544-A815-43DCBD023A95%7D&file=Collaborations.docx&action=default&mobileredirect=true) 

1. Azure Portal Guidance
    1.  Microsoft Account (MSA - Outlook/Hotmail/Live/MSN/Gmail/etc) access works. You can add an MSA as an Owner on your subscription to grant external collaborators access to internal subscriptions in the MS AAD Tenant. _(Accurate as of 12/17/2019)_
    2. PIM tested with MSA and works (Owner RBAC tested + new RG/VM creation and deletion of resources worked)

2. Azure Resource Guidance
    1. TODO: Virtual Machine Access guidance + scenarios
    2. TODO: Storage Account Access
    3. TODO: <Add other common scenarios>
        1. Visual Studio / VS Code Deployments / ADO Pipelines / Cosmos/Project VC other internal resources that are supported vs. not for external collaborators.
    4. Accessing your personal Azure Portal instance tied to your MSA (works but make sure you accept the invite in email)

3. Azure DevOps Guidance
    1. Refer to [Adding External Users to ADO + AAD](/Research-Technology-Engineering-Services/Azure-DevOps-Service/Adding-External-Users-to-ADO-+-AAD)


Additional Resources:

1. [AI+R Privacy Team SharePoint Site](https://microsoft.sharepoint.com/teams/RIInternal)
2. [AI+R Security Team SharePoint Site](https://microsoft.sharepoint.com/teams/RIInternal/SitePages/Security.aspx)
3. [AI+R Legal Team SharePoint Site](https://microsoft.sharepoint.com/teams/TnRInternal/Pages/legal/legal.aspx?web=1)