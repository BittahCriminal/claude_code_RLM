[[_TOC_]]
# Preamble
These services are built and maintained by the SES team and v-team members. This list is meant give people an idea of whom to go to for support or context of our existing services. We welcome people wanting to cross train and broaden their experience. If you're new to contributing, just let us know by giving a shout-out on teams.

# Terminology

- **Service Isolation** This is our ideal state where each component is dedicated to the service. I.E. not shared. The alternative is to share one or more component. A good example of this is our LLM Proxy. 
- **Shared Service** This is a service that shares one or more components with another. An example of this could be a dev/test service that has testing across many projects or services. 
- **Service Tree** This is Microsoft's standard for service/product ownership and accountability. [Docs](https://eng.ms/docs/cloud-ai-platform/azure-edge-platform-aep/aep-engineering-systems/engineering-intelligence-standards/service-tree/service-trees-team-doc/stbasics)
  - **Common Structure**: Division, Organization, Service Group, Team Group, Service, Subscription
  - SES is bucketing in a Team Group called: [Shared Engineering Services](https://microsoftservicetree.com/organizations/4cc1ba9e-5c68-4624-b65f-add9fae85866)


# Service Standard

A fully mature service has the capability to understand and manage inventory across several systems. These systems are required by Microsoft to ensure awareness and accountability. Our management of these systems are critical to the reducing our technical debt. When deciding how to approach these systems we must take into account the overhead of management. For example, a single repository may not be a good target for its own Service Tree service. It might make more sense to group similar efforts under a general service or subscription. 

Another challenge is that some services (like code repos) don't have 

Ideal state is **Service Isolation**:
- One service per Service Tree service
- One Subscription per service
- One or more security groups for management.
  - We should follow Least Privileged Access (LPA) designs
  - If multiple services are managed by similar people you are empowered to simplify our operations by using a single group
  - We should avoid communications and permissions being the same group as many like to be informed but not participate in service management.

The ideal state might be a bit of overhead when creating but it greatly reduces it when managing your accountability as a service owner. For example, if you isolate your service you will get:

- A scoped report of costs from Azure Spend
- A scope area of cost savings from Azure Spend
- Better budget tracking for business managers
- A clear owner from Service Tree
- The ability to define metadata without negativity impacting other services (prod/non-prod)
- A stronger security boundary (shared subs can allow lateral movement)

Each Service should consider:
- The Service Tree service that it should belong to
- The subscription it should belong to (if needed)
- The Resource Group for the service
- The tagging structure (Rings, Service labels, etc)
- The security boundary (edge, group permissions)
- The Release and Compliance requirements

If you're not sure if you should target a isolated or shared approach, please reach out to [Trevor](mailto:trevor@microsoft.com) for review. 

# How to create Service Tree services and Subscriptions

These processes are managed by our RTE PM team.

To engage please use the following forms:
- [Service Tree service creation](https://msresearch.visualstudio.com/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4608/Service-Tree)
- [Azure Subscription Creation](https://microsoft.sharepoint.com/teams/AIRDEPOT/SitePages/azadmin.aspx)

# Service Documentation
Documentation is a critical component of any service. It enables a shared understanding and provides a single source of truth of what owners/customer should expect. Not keeping your service documentation current provides risk to our team's creditability. 

Service Documentation should include:
  - A description of the service, what its purpose is, and who the users are.
  - A scope of production or non-production
  - SLOs, SLIs and KVIs 
  - A description of all collateral needed for management (Subscription, Service Tree service, secure groups, etc)
  - A link back to the project statement used to create the service if it exists
  - If not in the project statement, any market analysis that justifies the existence of this service from other Azure Native offerings.
  - If needed, user documentation, either here or in another appropriate discoverable location.
  - What alert monitoring is provided
  - Any service limitations
  - Any git repositories that hold code relevant to the service
  - Hints in supporting the service, including any common troubleshooting measures

# SLOs SLIs and KVIs
When managing a service, it's important to measure its reliability and the value it provides to users. To do this, we use several key metrics: SLO, SLI, and KVI.

- **SLO** is the **Service Level Objective**. This is a threshold that measures the end user's expectation of reliability. This can be service availability or uptime, service responsiveness such as the time it takes to download a file or web page.
- **SLI** is the **Service Level Indicator**. This is a measurement that shows if we are within the defined SLO
- **KVI** is the **Key Value Indicator**. It is a quantitative measurement showing the value the service is providing. Utilization is a common KVI, while other good indicators include quantitative measurements that demonstrate the value the service provides, such as time saved or how widely the service is used.

Additionally, the methodology or methodologies used to establish these values should be described alongside the objectives and indicators.


# Alert Monitoring

  - Each service should have alert monitoring in order to track service degradations or downtime.

# Supporting Metrics

  - Each service should have supporting metrics used to help troubleshoot service if there is service degradation, either reported by monitoring (ideal) or users. Often this comes "for free" with many Azure services.
  - Each service should also have, where possible, metrics to track utilization to ensure the validity and impact of the service.


# Resources and Further Reading
[Google SRE Book](https://sre.google/sre-book/table-of-contents/)
[Implementing Service Level Objectives](https://www.oreilly.com/library/view/implementing-service-level/9781492076803/)
https://learn.microsoft.com/en-us/azure/site-reliability-engineering/
- FTEs can read O'Reilly books at https://aka.ms/oreilly