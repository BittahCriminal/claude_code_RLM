**_If you are on this page, that means either you have a question on when to create a new project or MSR-ADO team sent this link_**

[[_TOC_]]

## MS-Research ADO Terminology <a name="Terminology"></a>

_If a Orchestra is Team (_ADO Project_). Strings, Woodwinds, Brass and Percussion groups are Smaller Teams (_Teams in ADO Project_). Each Symphony (_Project_) is a Repo._
Each ADO Project is considered as a Team. 
::: mermaid
 graph LR;
 A[ADO Project] --> B[MS Research Team];
:::
Each Repo is considered as a individual project. 
::: mermaid
 graph LR;
 A[ Git Repo] --> B[Application];
:::
If your Application is big, you can link multiple Repos of code to a Single Application
::: mermaid
 graph LR;
 A[Git Repo 1] --> B[Application];
 C[Git Repo 2] --> B[Application];
 D[Git Repo 3] --> B[Application];
:::


## Default settings of a ADO project
When MSR_ADO team is creating a ADO project, These are the settings that will apply to each project.
1. Each new Project created will be set Enterprise Visibility unless there is a business justification to be private visible, This means that all the users of the Organization will have read access to your project.
2. [Process](https://go.microsoft.com/fwlink/?LinkID=825) Agile-SDL is set for all the projects. Read more about Agile [here](https://docs.microsoft.com/en-us/devops/plan/what-is-agile))
3. Version control is set to [Git](https://docs.microsoft.com/en-us/devops/develop/git/what-is-git))


---
**Fun Fact**:
There are Organizations outside Microsoft running on single ADO project with 500+ area paths, Teams and up to 10 Area Path Depth. To give a glimpse of this scale in our Organizational chart view, from Microsoft CEO to me it's 8 Area Paths Deep. 
::: mermaid
graph TD;
    1.CEO-->2.CTO;
    2.CTO-->3.CVP;
    3.CVP-->4.Director;
    4.Director-->5.Deputy-Director;
    5.Deputy-Director-->6.Partner-Services-Engineer;
    6.Partner-Services-Engineer-->7.Principle-Service-Engineer;
    7.Principle-Service-Engineer-->8.Me;
:::


Learn more about ADO work Object limits [here](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/work/object-limits?view=azure-devops).

---



## When to add a new Project?
In general, we recommend that you use a single project to support your Team. A single project minimizes the maintenance of administrative tasks and supports the most optimized / full-flexibility [cross-link object](https://docs.microsoft.com/en-us/azure/devops/boards/queries/link-work-items-support-traceability?view=azure-devops) experience.

Even if you have many teams working on hundreds of different applications and software projects, you can most easily manage them within a single project. A project serves to isolate data stored within it. You can't easily move data from one project to another. When you move data from one project to another, you typically lose the history associated with that data


## Frequent Requests to add a ADO project

These frequent requests from research teams to MSR-ADO to add new projects:

-   To prohibit or manage access to the information contained within a project to select groups. 
	-   With defaults set to Enterprise Visibility this requirement won't work in most cases unless the project is set to private visibility. 
-   To support custom work tracking processes or custom workflow process for specific business units within your Team
	-   Agile-SDL is a excellent process to follow for Software Development life cycles and it's a default process too. But we will can always include custom workflow process and custom issue types in the same project.
-   To support entirely new and separate Software units that have their own Developers and Teams.
	-   If the new Team is mix and match in your own team internally, It is suggested to keep everything under same ADO project
-   To support testing customization activities or adding extensions before rolling out changes to the working project.
	-   This can be incorporated into a single project to have multiple testing customization activities.
-   To support an Open Source Software (OSS) project.
	-   MSR-ADO is not the place for OSS projects. But you can have a project here for sometime before moving completely to Microsoft GitHub. 

## Structure your project

When you add a project, look at using the following elements to structure it to support your business needs:

-   [Create a Git repository](https://docs.microsoft.com/en-us/azure/devops/repos/git/creatingrepo?view=azure-devops) for each subproject or application, or [create root folders within a TFVC repository](https://docs.microsoft.com/en-us/azure/devops/repos/tfvc/branch-folders-files?view=azure-devops) for each subproject. If you're using TFVC and heading toward a combined project model, create root folders for different teams and projects, just as you would create separate repos in Git. Folders can be secured as needed and workspace mappings can control what segments of the repo you're actively using.
-   [Define area paths](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/set-area-paths?view=azure-devops) to support different subprojects, products, features, or teams.
-   [Define iteration paths (also known as sprints)](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/set-iteration-paths-sprints?view=azure-devops) that can be shared across teams.
-   [Add a team](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/add-teams?view=azure-devops) for each product team that develops a set of features for a product. Each team you create automatically creates a security group for that team, which you can use to manage permissions for a team. See also, [Portfolio management](https://docs.microsoft.com/en-us/azure/devops/boards/plans/portfolio-management?view=azure-devops).
-   [Grant or restrict access to select features and functions](https://docs.microsoft.com/en-us/azure/devops/organizations/security/restrict-access?view=azure-devops) using custom security groups.
-   [Create query folders](https://docs.microsoft.com/en-us/azure/devops/boards/queries/organize-queries?view=azure-devops) to organize queries for teams or product areas into folders.
-   [Define or modify notifications](https://docs.microsoft.com/en-us/azure/devops/notifications/about-notifications?view=azure-devops) set at the project level.

## When to add a team, scaling Agile tools across the project.
As your Team grows, start using _teams_ option in ADO to provide them Agile tools that each team can configure to meet their workflow.
-   [Scale Agile to large teams](https://docs.microsoft.com/en-us/devops/plan/scaling-agile)
-   [About teams and Agile tools](https://docs.microsoft.com/en-us/azure/devops/organizations/settings/about-teams-and-settings?view=azure-devops)
-   Manage a [portfolio of backlogs](https://docs.microsoft.com/en-us/azure/devops/boards/plans/portfolio-management?view=azure-devops) and gain insight into each team's progress and the progress of all programs.
-   Use [Delivery plans](https://docs.microsoft.com/en-us/azure/devops/boards/plans/review-team-plans?view=azure-devops) to review the schedule of stories or features your teams plan to deliver. Delivery plans show the scheduled work items by sprint (iteration path) of selected teams against a calendar view.
-   Incrementally adopt [practices that scale](https://docs.microsoft.com/en-us/azure/devops/boards/plans/practices-that-scale?view=azure-devops) to create greater rhythm and flow within your organization, engage customers, improve project visibility, and develop a productive workforce.
-   Structure projects to gain [visibility across teams](https://docs.microsoft.com/en-us/azure/devops/boards/plans/visibility-across-teams?view=azure-devops) or to support [epics, release trains, and multiple backlogs to support the Scaled Agile Framework](https://docs.microsoft.com/en-us/azure/devops/boards/plans/scaled-agile-framework?view=azure-devops).

To see recommendation on a complex project and team management visit [ADO-Project-Management-Recommended-Practices Page](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4563/ADO-Project-Management-Recommended-Practices).

**Cheers :beers:**