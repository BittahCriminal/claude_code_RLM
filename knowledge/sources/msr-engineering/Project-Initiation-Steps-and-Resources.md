      
**Preparation**
·       If needed, create a new **Project Name** and **Project ID**: [GPU Reporting Power App](https://apps.powerapps.com/play/e/cb9644d8-619b-e29c-ad57-d79cc76bc51e/a/32ea0b35-32c7-40d8-ab4c-6b2e58108328?tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47&amp;hint=26cf37d7-f57e-4965-bc5a-8f58e1d2d310&amp;sourcetime=1712698496537)
o   [Project Portal ID and Experiment ID Creation - Overview](https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/9044/Project-Portal-ID-and-Experiment-ID-Creation)
·       If needed, create new Research Project Portal Page (Julia and Mike)
·       Sample Teams OneNote location for project notes: (onenote:https://microsoft.sharepoint.com/teams/GCRMemberOutreach/Shared%20Documents/General/Hardware%20Testing%20Project%20Information/Hardware%20Testing%20Notebook/GH200%20and%20Maia100.one#&section-id=f48b0156-dd4a-461a-a020-74e89170a547&end)  ([Web view](https://microsoft.sharepoint.com/teams/GCRMemberOutreach/_layouts/15/Doc.aspx?sourcedoc={a90c3a94-c117-4e34-bb5c-97c806768ca6}&action=edit&wd=target%28GH200%20and%20Maia100.one%7Cf48b0156-dd4a-461a-a020-74e89170a547%2F%29&wdorigin=717&wdpreservelink=1))
·       Sample email comms for MI300 and GH200 can be found here: 
[GPU Hardware Trials and Testing](https://microsoft.sharepoint.com/:f:/t/TnREng7/EohoNAzR58JFjYUPhpQlzpIBODP4sojw36dDvJeqjH-QZA?e=8DqGuB)
·       Gather names for v-team
·       Create email enabled SG and add all v-team members
·       Create Teams chat for the v-team (ie: “GH200 V-Team”)
·       Schedule a kickoff meeting
·       Schedule weekly check-in meetings for v-team
·       Schedule bi-weekly Ops Team meetings for internal syncs
·       Gather contacts for hardware owner (lambda, AMD, etc) who will be involved in issue triages, getting access, answering questions, issue tracking (Jira, etc)
·       Schedule weekly meeting with supplier (AMD, Lambda, etc)

**Test Planning**
Work with Ops team create a test plan. Lifeng typically creates plans and tracking in OneNote.
Work with team to document plan – tests and evaluations, action items/tasks, ownership of tasks, etc. Create ADO tickets.
Sample backlog: [GCR - MI300 Testing Project - Boards](https://dev.azure.com/msresearch/MSR%20Engineering/_queries/query-edit/48eb8bfe-7606-4f69-89ed-a2a119e6dc49/)
OneNote for Lifeng and Ops team: [GPU Efficiencies](onenote:https://microsoft.sharepoint.com/teams/supwhine/Shared%20Documents/OneNote%20Notebooks/TnR%20Meeting%20Minutes/GPU%20Efficiencies.one#&section-id=575b249a-314e-4361-84a2-2f85d03efcc4&end)  ([Web view](https://microsoft.sharepoint.com/teams/supwhine/_layouts/15/Doc.aspx?sourcedoc=%7bc188b4a9-7067-493a-b272-75af5bc230d7%7d&action=edit&wd=target%28GPU%20Efficiencies.one%7C575b249a-314e-4361-84a2-2f85d03efcc4%2F%29&wdorigin=717&wdpreservelink=1))
Example work breakdown for planning: [10/17/2024](onenote:https://microsoft.sharepoint.com/teams/supwhine/Shared%20Documents/OneNote%20Notebooks/TnR%20Meeting%20Minutes/GPU%20Efficiencies.one#10%2F17%2F2024&section-id=575b249a-314e-4361-84a2-2f85d03efcc4&page-id=d25d79b7-899d-43df-88e8-b94e1e51240c&end)  ([Web view](https://microsoft.sharepoint.com/teams/supwhine/_layouts/15/Doc.aspx?sourcedoc=%7bc188b4a9-7067-493a-b272-75af5bc230d7%7d&action=edit&wd=target%28GPU%20Efficiencies.one%7C575b249a-314e-4361-84a2-2f85d03efcc4%2F10%5C%2F17%5C%2F2024%7Cd25d79b7-899d-43df-88e8-b94e1e51240c%2F%29&wdorigin=703&wdpreservelink=1))
Example Test Coverage Plan: [Test coverage 11-18-2024](onenote:https://microsoft.sharepoint.com/teams/supwhine/Shared%20Documents/OneNote%20Notebooks/TnR%20Meeting%20Minutes/GPU%20Efficiencies.one#Test%20coverage%2011-18-2024&section-id=575b249a-314e-4361-84a2-2f85d03efcc4&page-id=542e74fa-7bd9-4faf-934f-0f6a8ee3562e&end)  ([Web view](https://microsoft.sharepoint.com/teams/supwhine/_layouts/15/Doc.aspx?sourcedoc=%7bc188b4a9-7067-493a-b272-75af5bc230d7%7d&action=edit&wd=target%28GPU%20Efficiencies.one%7C575b249a-314e-4361-84a2-2f85d03efcc4%2FTest%20coverage%2011-18-2024%7C542e74fa-7bd9-4faf-934f-0f6a8ee3562e%2F%29&wdorigin=703&wdpreservelink=1))

**V-Team Resources:** (check links and pin these to the team chat)
*   Wiki for getting started guide, examples, known issues, expectations (Lifeng is owner. Typically on our GCR wiki page)
    *   [Job submission on AMD ecosystem - Overview](https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/13674/Job-submission-on-AMD-ecosystem)
*   Form for logging your Experiment details: [Experiment Tracker](https://apps.powerapps.com/play/e/cb9644d8-619b-e29c-ad57-d79cc76bc51e/a/32ea0b35-32c7-40d8-ab4c-6b2e58108328?projectId=PRJ-0502-A18&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47) (this is where you get your experiment name for tagging – see below)
*   SharePoint location for documentation and OneNote for v-team: [GH200 Testing Project](https://microsoft.sharepoint.com/:f:/t/GCRMemberOutreach/ElrWrbTRWCtHgcn0ew5oMZoBvUh0n7tPrUJWlDic8ZDy0w?e=1EUa93) 
*   If **tagging jobs** is required, ensure v-team knows this and have them tag their jobs properly
    *   [Custom Tagging Jobs - Overview](https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/8028/Custom-Tagging-Jobs)
    *   Example of proper tagging: [**Project_Name:Lambda_GH200_Testing,ProjectID:**PRJ-0428-A46**,Experiment:**Lambda_GH200_rccl-tests] 
*   SharePoint Issue Entry Form: The list was migrated. [GPU Issue Tracker](https://aka.ms/gpuissues) 
    *   SharePoint Issue List: [https://aka.ms/gpuissueslist](https://aka.ms/gpuissueslist) 
*   ICM Tickets: [https://aka.ms/ITP/IcMfor1P](https://aka.ms/ITP/IcMfor1P)
*   Jira for AMAD
    *   [How to get access to AMD's JIRA backlog - Overview](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/14014/How-to-get-access-to-AMD's-JIRA-backlog)
    *   [Issue Navigator - External JIRA](https://ontrack.amd.com/issues/?jql=project%20%3D%20MSRCHA%20AND%20resolution%20%3D%20Unresolved%20ORDER%20BY%20created%20DESC%2C%20priority%20DESC%2C%20updated%20DESC)

**Reporting:**
Project templates and resources: [GPU Hardware Trials and Testing](https://microsoft.sharepoint.com/:f:/t/TnREng7/EohoNAzR58JFjYUPhpQlzpIBODP4sojw36dDvJeqjH-QZA?e=8DqGuB)
·       V-Team questionnaire example:
o   [GH200 Questionnaire - Summary.docx](https://microsoft.sharepoint.com/:w:/t/TnREng7/Ed5WJGHZahdIn9V-Lqge1IoBfuucynQek8KSJMsKL2DEkw?e=lXbGao)
·       LT Weekly Report: [AMD, Singularity, and AOAI Status Report12-19-24.pptx](https://microsoft.sharepoint.com/:p:/t/TnREng7/EZw96Wjf3QVBp8lUkCn99KwBC0fqzNjYY4MbCtIQo4emhw?e=LsfEbI)
·       Consolidated Issue Tracker (AMD, Singularity, ICM, etc): [Singularity-AMD-IssuesTracking.xlsx](https://microsoft.sharepoint.com/:x:/t/TnREng7/EUgosk5_YNZAh-dekrRWBy0B40bXFDmJCc580MmpMAR6Zg?e=cYcYus)