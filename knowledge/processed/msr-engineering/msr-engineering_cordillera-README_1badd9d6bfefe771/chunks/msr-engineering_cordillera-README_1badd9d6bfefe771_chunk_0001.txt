 area and the rules that are appropriate to maintain the stability and performance of the cluster.

### Approval Gates
Area leads may specify themselves as: 
* **Mandatory approvers**: Their approval is required for any change to their area.  
  * Leads designating themselves as mandatory approvers must also provide at least one additional approver to avoid blocking merges.  The list of approved reviewers will be added to a group specific to that code area to facilitate easier administration of future privilege and messaging assignments. 
* **Optional approvers**: They are notified of relevant changes, but their approval is not required for merge. 

### Technical Gates
Area leads may also define technical validation requirements for their code area.  These may include: 

* Build validation 
* Formatting / linting checks 
* Static analysis or status checks 
* Area-specific test suites 
* Any additional verification mechanisms appropriate for the asset type (e.g., YAML, Bash, C#, etc.) 
