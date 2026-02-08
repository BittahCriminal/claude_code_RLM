
# Cordillera: Introduction 🌄
Welcome to Cordillera! The home of configuration, tooling, and utilities for all current and future GCR‑operated training clusters: not just the Bonete B200 cluster.

We chose the name Cordillera ([which is a large, complex chain of mountain ranges](https://en.wikipedia.org/wiki/Cordillera)) intentionally:
* A range made of many peaks, symbolizing Bonete today plus future clusters
* A unified operational foundation, spanning multiple environments
* A scalable structure, designed to evolve as GCR grows
* Such mountain systems have a complex structure, just as our repository will have many interrelated components which contribute to the success of this and future clusters.

Cordillera provides clear documentation, centralized configuration, and community‑driven tooling to empower collaboration across the GCR AI Infrastructure and you, our Research partners.

# Repository Contents

At this time, the Cordillera repository is intended for the following types of contributions: 
* Cluster configuration (e.g. Kubernetes manifests, Volcano configurations). 
* Operational tooling used by cluster users or operators. 
* Documentation supporting cluster usage, administration, or operations. 
* Utilities that assist with interacting with clusters, submitting jobs, or improving operational workflows. 
* Code ownership metadata: Each project or code area must maintain an es-metadata.yml file defining ownership, approvers, and other metadata. Some areas may inherit defaults from the root-level es-metadata.yml; area leads should review and update settings as needed.

The Cordillera repository is not intended for hosting research code, experiments, model training pipelines, or any job-specific or user-specific scripts. These instead should be hosted in the contributor’s own project repositories.

It may help to think of research code as "data-plane" resources for the cluster, and that the Cordillera repository is used to host "management-plane" cluster resources.

# Code & Configuration Governance
We want to encourage contributions from the research community, so our default review model is lightweight:

* Each pull request must be reviewed and approved by a member of the MSR AI Infrastructure V-Team, or the MSR AI Infrastructure core team.
  * Considering that the PR submitter is considered to implicitly approve their own code submission, this results in a 2-person approval for each PR in the repository.

Additionally, each code area must create and maintain an [es-metadata.yml file](https://eng.ms/docs/coreai/devdiv/one-engineering-system-1es/1es-docs/product-catalog/inventory-as-code/manage-inventory), if the code area needs to override the defaults specified in the repository root.  For most code areas, there will be minimal (if any) data elements which must be overridden:  the most likely is identifying the responsible owners.

Finally, each code area is encouraged to create and maintain a README.md file in the root of their area folder, and subsequent README.md files as appropriate for submodules that may be created.  The exact best practice for this will vary from project to project.

## Area-Specific Approval and Technical Gates
Beyond the minimal requirement for general repository contributions, each code area lead can specify additional approval or technical gates that are applicable to their part of the project.  Each of these will vary based on the code area and the rules that are appropriate to maintain the stability and performance of the cluster.

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
