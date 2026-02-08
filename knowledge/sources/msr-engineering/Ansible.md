# How Ansible is used in GCR
Ansible is being used on Linux hosts running Ubuntu 20.04 and above only. For Windows hosts in GCR, we use [Azure Automation](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/3428) which utilizes [DSC](https://docs.microsoft.com/en-us/powershell/scripting/dsc/overview).

## SLO/SLI/KVI

The following are definitions of SLO/SLI and KVI. No actual metrics are available for this service currently.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal;">Ensure a failure rate of no more than 1% of deployed hosts</span>|
| --- | --- |
| SLI | Use the reported metrics of failures to generate a table that shows fails vs successes |
| KVI | Number of hosts using this service |

### Methodology:
None of the above have been implemented, but here are some proposals and explanations:

**SLO** - May need to be adjusted but is a swag of how many ansible runs should be successful.
**SLI** - Would need to either query our existing Azure Table for a dashboard
**KVI** - Could get this table from the proposed SLI. Could also gather how many playbooks are being executed per host to show automation vs potential toil.


## Installation and execution
* We have a custom Ansible package in a custom debian repository.
* [Azure] The ansible package is installed as a [custom script extension](https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-linux).
* Once the package is installed, it creates a crontab which will cause it to run ever half hour.
* During the Ansible run, the package downloads the current code from the [gcr-ansible-master container](https://ms.portal.azure.com/#blade/Microsoft_Azure_Storage/ContainerMenuBlade/overview/storageAccountId/%2Fsubscriptions%2F7ccdb8ae-4daf-4f0f-8019-e80665eb00d2%2FresourceGroups%2Fgcr-ansible%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Fgcransible/path/gcr-ansible-master/etag/%220x8D79940707C7B41%22/defaultEncryptionScope/%24account-encryption-key/denyEncryptionScopeOverride//defaultId//publicAccessVal/None) in our [gcransible](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-ansible/providers/Microsoft.Storage/storageAccounts/gcransible/containersList) storage account.
   * Code in this container is sync'd from our [gcr-ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible) ADO codebase via the [gcr-ansible CI pipeline](https://dev.azure.com/msresearch/MSR%20Engineering/_build?definitionId=2053). Every code commit activates this pipeline.
* After the code is downloaded, ansible runs the code directly on the VM.


::: mermaid
sequenceDiagram
    participant A as VM
    participant B as Ansible Package
    participant C as Storage Acct with Code
    participant D as Ansible Git Repository
    B->>A: [Initial Install] Downloads via Custom Script Extension
    A->>A: [Initial Install] Install Ansible Package
    C->>A: [Every 30 minutes] VM Downloads Code
    A->>A: [Every 30 minutes] Execute Ansible Code
    D->>C: [On code commit] Code push via pipeline
:::



# Ansible Information Resources



[Latest Main Ansible Documentation](https://docs.ansible.com/ansible/latest/)
[MyDailyTutorials - Decent Ansible Tutorials Site](https://www.mydailytutorials.com/)
[Ansible Subreddit](https://www.reddit.com/r/ansible/)
[Ansible video libarary](https://www.ansible.com/resources/videos)
[Infrastructure testing with Molecule by Elana Hashman](https://www.ansible.com/infrastructure-testing-with-molecule)

## Azure
[Ansible on Azure Documentation](https://docs.microsoft.com/en-us/azure/ansible/)
[Azure Ansible Module and Version Matrix](https://docs.microsoft.com/en-us/azure/ansible/ansible-matrix)
[Ansible Documentation - Microsoft Azure Guide](https://docs.ansible.com/ansible/latest/scenario_guides/guide_azure.html)
