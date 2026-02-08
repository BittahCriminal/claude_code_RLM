https://microsoft.sharepoint.com/teams/RIInternal/SitePages/Migrating-VSO-Projects-across-Accounts.aspx

# Introduction
This article describes the Security Guidance and the available Support for Azure DevOps (formerly Visual Studio Online) within MS Research. It also describes the proper procedures for getting an Azure DevOps project created and configured correctly, as well as how to prepare a project for release during a Security Review.

#  Security Guidance
**All** MSR projects not releasing as open-source (GitHub) must be created under one of the following approved accounts:
* msresearch (Recommended)
* msrasia
* msrcambridge
* microsofthealth
* malibu00
* tnrdev

If you have an existing project that is not under one of these accounts you must migrate to an approved ADO account. 

# Support
For support with Azure DevOps (msresearch only), please contact [MSR-ADO](mailto:msr-ado@microsoft.com). The following services are provided:

- Process template modifications 
- Access control instantiation  
- Extension deployments 
- Project creation in accordance with security requirements

The following policies are enforced:
- No 3rd party extensions to be deployed  
- All extensions will require engineering review  
- Custom Process templates only with business justification

# Instructions for New Projects

## Create the Project

If you haven't already, these steps will help you create a project in ADO:
Navigate to the website for the account most appropriate for your release (based on the above criteria).
1. Click the **Create Project** button.
1. Enter a Project name and short description.
1. Decide on the visibility of your project.
-   This can be changed later.
1. Choose the appropriate Work item process for your project.
-  This is at the discretion of your team. In most cases teams choose 'Agile'.
-  You **must** use the 'SDL' variant of your selected process (e.g. 'Agile-SDL' is the appropriate option for Agile projects).
1. Click **Create**.

# Set Permissions

1. These steps will help you set the correct permissions to allow team members to access your new project.
1. On the project page in Azure DevOps, click on **Project settings**.
Under General, go to **Security**.

This is the page that allows you to assign permissions. Typically, any member of your immediate team who requires access to the project should go under the default project team (which shares the name of the project itself). To add team members:
1. Under **Teams**, click on the project team.
-   This is the team that shares the project's name.
1. Click on the **Members** tab.
1. Click **Add**…
1. Enter the alias of the team member to add OR the alias of your team's Security Group.
1. Click **Save Changes**.

# Automatic Security Scans
Save time when completing your Security Review by scanning source code for security vulnerabilities as you write code! A detailed guide describing how to instrument your project for these scans can be found [here](https://microsoft.sharepoint.com/teams/RIInternal/SitePages/Self-Service-Build-Scans.aspx).


# Preparing for a Security Review
Additional permissions need to be assigned to any project that will need a Security Review prior to releasing.

# Grant Access to AIRSecCompliance

AIRSecCompliance must be granted read access to the repository for security analysis.
1. Navigate to the project on Azure DevOps and click **Project settings**.
1. Under **General**, click on **Security**.
1. Under **VSTS Groups**, select **Readers**.
1. Under the **Members** tab, click the **Add**... button.
1. Enter _AIRSecCompliance@microsoft.com_ and click **Save changes**.

#Grant SDL Access

The SDL team gathers metrics on open security bugs in all code released by Microsoft. Their Service Account needs read access to work items in order to collect this data from your project.
1. Navigate to the project on Azure DevOps and click **Project settings**.
1. Under **Work**, click on **Project Configuration**.
1. Click on the **Areas** tab.
1. Find the highest-level Area in the list. Right-click it and choose **Security**.
1. Click **Add**....
1. Enter _SDL Work Item Readers_ and click **Save changes**.
1. Select _SDL Work Item Readers_ in the list. Set the value for _View work items in this node_ to **Allow**.
1. Click **Save changes**.

#Code signing injection
If your pipeline includes a task that _must_ be run last, you may need to set the variable `runCodesignValidationInjectionBG` to `false`. This is a "break glass" variable, so we probably shouldn't use it unless we have to.
This is not officially documented, but an email conversation with Sridhar Poduri and Praveen Pendyala (in November/December of 2019, subject "Codesign Validation Task Injection") led to this being mentioned and confirmed.