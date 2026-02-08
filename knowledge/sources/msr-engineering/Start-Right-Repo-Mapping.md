Msresearch will be onboarding the Start Right 1ES extension to enforce inventory compliance during repository creation. This extension introduces a structured approach to repository creation, enabling us to categorize repositories as “production” or “non-production” and associate them with the appropriate ownership model: either a service tree or at least two accountable owners. 

The purpose of this document is to provide clarity on when to choose a Service Tree Service or opt for direct mapping during the repository creation process under the Start Right 1ES extension.


## **Repo Creation under Start Right** 

- Provide information for your new repository 

- Provide a name for your repository 

- Choose to add a README and .gitignore files 

- Select the classification for your repository - Production or Non-production. 

- Assign your repository to service(s) or direct owners. 

  * Production repositories are required to specify a Service Tree that your repository is associated with.

  * Non-production repositories can specify a service tree OR two or more "direct owners".




| **Note:** If your project is classified as “production”, it is mandatory to associate your repo with a service tree. For one-off projects that do not require extensive governance, we recommend utilizing direct mapping. |
---

## **Service Tree Service**: 

- A Service Tree Service represents a specific service or component within our organization’s infrastructure. 

- Targeting a Service Tree Service for repository ownership is recommended when: 

  - The repo closely aligns with a particular service’s scope and functionality. 

  - Multiple teams or individuals contribute to the service and need access to the repository. 

## **Direct Mapping:** 

- Direct mapping refers to assigning repository ownership and access to specific individuals or teams. 

- Direct mapping should be a suitable approach when: 

  - The repository’s purpose is independent of any particular service or component. 

  - Ownership and access is restricted to a specific team or individuals. 

  - Ownership is expected to remain stable or the repository serves a unique purpose that requires a dedicated ownership. 


---


For additional information on Start Right and its documentation, please refer to the following link:

[Start Right for Azure DevOps Repo Creation | 1ES On EngHub](https://eng.ms/docs/cloud-ai-platform/devdiv/one-engineering-system-1es/1es-docs/startright/repo)


