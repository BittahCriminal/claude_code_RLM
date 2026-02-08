[[_TOC_]]

# Why
This page is intended to capture the details on how T&R is adopting Github. The goal will be to share resources and frame an approach for adoption. There are some hard corporate rules (external user access, open source) and other areas where we have recommendations. We will highlight 

#Flavors of Github
There are three (really two) flavors of Github in Microsoft. You can review [this page](https://eng.ms/docs/more/github-inside-microsoft/overview) for more details but a summary is below. 
- [Github Enterprise Cloud](https://repos.opensource.microsoft.com/). This is any project hosted under github.com and should only be used for projects that intend to be released externally or when partnering with externals. You should not create your own organization and should use one listed [here](https://docs.opensource.microsoft.com/github/opensource/orgs/)
- [Github Enterprise Managed User (EMU)](https://eng.ms/docs/more/github-inside-microsoft/overview/emu). This is for any internal projects not intended for public release. This should only be used by internal employees.

GithubAE:
- [Github AE](https://eng.ms/docs/more/github-inside-microsoft/overview/ghae). This is an older deployment and no longer an option.

# TnR Strategy

### Planning
Setting your strategy should be done in the beginning of your project. If you know your intent is to open source the project it probably makes sense to start in GH Enterprise Cloud. If you know the project is internal, GC EMU is the right place to start. Moving repos can be done but the complexity depends on the feature set. 

### Feature areas of interest

|Feature|ADO|EMU|Notes|
|--|--|--|--|
|PR Experience | X |  |  |
|Build & Release Pipelines  | X |  |  |
|Project Management  | X |  |  |
|Researcher Familiarity |  | X |Most researchers already used to github.com  |
|Planned 1ES investments  |  |X  | Long term strategy is Github ; most new features going to EMU |
|Ease of Opensourcing  |  | X |Need to move to github.com/microsoft anyway |



### Scenarios

- Open source (**Requirement**)
  - Github Enterprise
- External Collaboration (**Requirement**)
  - Github Enterprise
- Internal Org Project (**Recommendation**)
  - Github EMU
  - Azure Dev Ops
- Internal company project (**Recommendation**)
  - Github EMU 

## EMU Organizations

Current EMU Organizations as of 9/9/24:

![image.png](/.attachments/image-d049d1de-c73d-437c-98fb-855e0f3f8544.png)

### EMU Reporting
The Github inside Microsoft (GiM) team manages a PowerBI report that can help understand a verity of information. One helpful datapoint is which EMU orgnizations exist in T&R. 

- [Report](https://msit.powerbi.com/groups/me/apps/045d9317-f500-496c-b540-e8831024bee3/reports/7f9a5ecc-dfb6-4c4a-bca3-87a4b6616041/ReportSection82b4a9aeb65401e72bd6?ctid=72f988bf-86f1-41af-91ab-2d7cd011db47&experience=power-bi)
- Make sure to set the following filters

![image.png](/.attachments/image-9cd128af-a3ee-4d9c-bb08-588a2858ccc0.png)

## Access


#RTE Onboarding

Group: [One click join TnR-GHEMU](https://idwebelements.microsoft.com/GroupManagement.aspx?Group=TnR-GHEMU&Operation=join)

# References
[Opensource @ MS](http://aka.ms/opensource)
[Github EC Orgs](https://docs.opensource.microsoft.com/github/opensource/orgs/)
[GH EMU Organizations](https://eng.ms/docs/more/github-inside-microsoft/repos/organizations)
[Github inside Microsoft](http://aka.ms/gim)
[Github inside Microsoft Support (Teams Preffered)](https://eng.ms/docs/more/github-inside-microsoft/overview/questions)
[Github Feature Matrix](https://eng.ms/docs/more/github-inside-microsoft/overview/features)
[Customer Collaboration](https://docs.opensource.microsoft.com/github/opensource/customer-collaboration/)
