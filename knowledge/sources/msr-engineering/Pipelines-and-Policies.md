# Policies

We use branch policies as part of our effort to adhere to best practices, improve code/configuration quality and ensure future maintainability.  Commits to the master branch are restricted:  if you have correctly configured pre-commit, you will get an early warning when you commit locally to master.  (Do not fear: you can easily create a new branch from your changes instantaneously without losing any work).

Code must be promoted to master via a pull request (PR).  The PR will limit your merge to a squash, and will not be completed until:

* The PR is reviewed and approved by at least one team member, and
* The commit passes the automated checks in the build pipeline (See below)

# Pipelines

## Build Pipeline
There are two pipelines used in the GCR-ansible repository.  The first is a "build pipeline", but this project doesn't (currently) have any "builds".  Once automated tests are devised, we may implement them as part of this pipeline.  For now, the build pipeline checks the commit for adherence to our automated linting and policy checks.  For more information on the checks, review the ".pre-commit-config.yaml" file in the repository root (or observe the output of ```pre-commit run --all-files``` on your workstation.

## Deployment Pipeline
The deployment pipeline triggers on the successful completion of a merge onto the 'master' branch.  It copies the repository to the storage account for retrieval by the managed instances.  If it ever becomes necessary, the deployment pipeline can be run on-demand to freshen the storage account.  The deployment pipeline does not include any quality checks as those are assumed to have been completed previously by the build pipeline.  In this way, it can be a useful escape hatch if an emergency deployment must be made which bypasses the build pipeline checks:  disable the build validation temporarily in the branch policies and then complete a PR as normal.  Once the code hits master, it will be deployed, and then the build validation can be re-enabled.  **note**: if you disable the policy checks in this way, you will still eventually need to solve the problem, either by addressing the underlying deficiency or by disabling the failing checks for the offending markup stanza(s).  The build pipeline checks run against all files in the repository, not exclusively against files changed in any particular commit.