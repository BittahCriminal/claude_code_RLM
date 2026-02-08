# Team goals

In our efforts to track code we adopt standards in the 1ES program where the overhead of the processes align with the visibility of the service.  That is to say if you're building a service that can cause a customer outage you will be required to do more than if only the engineering team depends on it.

## ADO Projects

Our source control system is Azure DevOps (ADO).

|Project|Description|
|-----|--------|
|[MSR Engineering](https://dev.azure.com/msresearch/MSR%20Engineering)| This is our main project with our internal repositories.  This should be the place most of your code lives.  This also contains all engineering work items.|
|[GCR](https://dev.azure.com/msresearch/GCR)|This is where you'll save customer code that is specific to our GCR service|

## Repositories

Any code you create should be saved in a repository.  This ensures the unexpected (system crash) does not result in lost work.  Most repositories should have projects associated and thusly have gone through the project intake process.  Please contact the [engineering managers](mailto:jim@microsoft.com;trevor@microsoft.com;krisz@microsoft.com) if you think you have a case where you need a repo for something that isn't an approved project.
|Repo|Description|Service|Branch Policy enabled?|Self approval|
|-----|----------|-------|---------|-----|
|[gcr-ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible)|This is our GCR-specific Ansible codebase|GCR|Yes|Yes|
|[GCR](https://dev.azure.com/msresearch/_git/GCR)| Onboarding scripts for customers|GCR|No|Yes|
|[winbind](https://dev.azure.com/msresearch/GCR/_git/winbind)|Scripts to help others configure WinBind|Operations|No|Yes|
|[AZSecPack_Orchestration](https://dev.azure.com/msresearch/MSR%20Engineering/_git/AzSecPack_Orchestration)| This contains our contributions to the AZSecPack project|Security|Yes|Yes|
|[ADO Migration tool](https://dev.azure.com/msresearch/MSR%20Engineering/_git/AdoMigration)|This tool provides migration services for ADO.| ADO Management| Yes|Yes|
|[MSR Engineering Tools](https://dev.azure.com/msresearch/MSR%20Engineering/_git/MSR%20Engineering?path=%2FResearchEngineeringTools&version=GBmaster)|This should not generally be used to store new code, but is a great place to find many legacy tools and scripts|Engineering|No|Yes|

## Branching

Branches are required in any project that has a policy enabled.  Our preferred format is 'alias/feature_description' as in 'trevor/adding_version_X'.

## Pull requests and reviews

Pull requests should:

- Link to work item (Bug or Task)
- At least one team member other than yourself has approved.  This is defined in the table above and might be relaxed due to SME availability.
- Squash and merge (should be default, update repo if not)
- If the fix is a bug ensure the description covers the why/how
- When submitting a PR make sure the message has enough detail for the approvers to execute
- Delete branch when PR is complete
- If the PR is large you might want to review it with [CodeFlow](https://www.1eswiki.com/wiki/CodeFlow)

### Reviews
We strive to always review pull requests with on code bases that directly affect our researchers such as Ansible. Having others review your code spreads the awareness of what you've done to others. Some things to keep in mind With Pull Requests:

- If the PR is extremely urgent, that usually means it is to fix something that has broken.  Stress will be high, as will the chances to make a mistake (even a small one).  Usually you're working on a problem with other people, so it shouldn't take very long to get someone else to review it, and the safety that provides is extremely valuable to make sure the problem doesn't get worse.
 
- If the PR is extremely minor/trivial, then it won't take someone very long to review it.
 
- If the PR is not urgent nor small - this fits into the exact case why we're doing Pull Requests

### Helpful guides:

- [Code review Training](https://www.1eswiki.com/wiki/Code_Review_Training)

# Code Subject Matter Experts

Please use the list below for approvers.  We may create ADO teams to better manage this.

|Lang|Users|
|----|----|
|C#|-|
|Chef| KrisZ; BenH|
|Kusto|-|
|Powershell|Trevor; KrisZ; JordanB|
|Ruby|KrisZ; BenH|
|Shell (Bash)|KrisZ; BenH; Trevor; JordanB|
|SQL|GeoffryN|
|Python|KrisZ; BenH; Trevor; JordanB|
|Ansible|KrisZ; Omid; JordanB|
|Go|KrisZ; JordanB|





