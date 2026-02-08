To ensure the proper archiving and the preservation of all necessary information for MSResearch, we recommend using the git bundle feature.  

Git bundle allows you to pack the references of your repository into a single file, which can then be treated as a recognized git source. You can perform fetch, pull, and clone operations from the bundle file.

# **Archiving Repositories using git bundle**

To create a bundle file containing the desired references, use the following command: 

`$ git bundle create /path/to/mybundle master branch2 branch3 `

To include all references (branches, tags, etc.) in the bundle, use the `--all` flag: 

`$ git bundle create /path/to/mybundle --all `

Once you have created the bundle file, please follow your team’s guidelines or any established procedures for storing and archiving project repositories. 

# **Reviving an Archived Repository** 

If you need to revive the project at a later date, you can download the bundle file and use git clone to extract the repository. 

`$ git clone /path/to/mybundle newrepo `

This will restore the repository on your local machine. Now, you can proceed with creating a new project and importing the repository into Azure DevOps.

1. Request a new project from MSR-ADO if necessary. 

1. Create a new repository: 

   - Select the project for which you wish to create the repository. 

   - Click on “Azure Repos” then choose “Default Repository”  

   - On the right-hand side, click “New Repository” 

   - Enter the desired repository name, and you can optionally choose to add a README file to the repository. 

   - Click “Create” to create the repository. 

Once the repository is created, you can proceed to restore your repository and its complete history. Use the following command to push the contents of the bundle file to the new repository: 

`$ git push --mirror https://dev.azure.com/contoso-ltd/MyFirstProject/_git/new-contoso-repo `

**Note:** Using the `--mirror` command will overwrite all branches in the target repository, including the deletion of any branches that are not present in the source repository.
--
## **classification for Project Catalog** ##

Please complete one of the following actions to complete repository classification:

Option 1: Classify the repository as Production or Non-production by visiting the repository link(s) in the list below. Clicking the Classify button will redirect you to Product Catalog where you can provide the appropriate classification.

[Repo Disabling](https://eng.ms/docs/cloud-ai-platform/devdiv/one-engineering-system-1es/1es-docs/product-catalog/inventory-program/repository-disabling-campaign#repository-no-longer-needed)

Option 2: Archive/delete the repository if it is no longer needed. Learn more how to archive/delete in a compliant manner.

To see a comprehensive view of your ADO repositories that are missing inventory, please visit this dashboard (only FTEs can access this dashboard)

 [dashboard](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2f%2fmsit.powerbi.com%2fgroups%2fme%2fapps%2f44b2d336-ddac-4afa-ac62-c0a4ecc3b202%2freports%2ff805b58b-e8f1-4bc2-bd73-dae519773304%2fReportSection%3Fctid%3D72f988bf-86f1-41af-91ab-2d7cd011db47%26experience%3Dpower-bi&data=05%7c01%7cv-ahuetson%40microsoft.com%7c0b9e600c0d95432f913908dbcf13dbde%7c72f988bf86f141af91ab2d7cd011db47%7c1%7c0%7c638331456480785495%7cUnknown%7cTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7c3000%7c%7c%7c&sdata=C3jjpzGvytDIeYlme5iYFYhhScgr41Fu43PZC8W1QM8%3D&reserved=0).

---
## **Additional Resources:** 

Please reference Microsoft documentation under the [Manually import a repo using git CLI](https://learn.microsoft.com/en-us/azure/devops/repos/git/import-git-repository?view=azure-devops#manually-import-a-repo-using-git-cli).

For more reference on git bundle please visit the git bundle resource [Git - git-bundle Documentation (git-scm.com)](https://git-scm.com/docs/git-bundle).

Another great reference for Git bundle is [Repository Backup — Git Memo v1.1 documentation (git-memo.readthedocs.io)](https://git-memo.readthedocs.io/en/latest/repository_backup.html)

[Location of the SES code archive](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/0d83bec5-5c98-45a6-a26a-a754a03afcae/resourceGroups/codearchive/providers/Microsoft.Storage/storageAccounts/sesamecodearchive/overview)