# RTE Data Services Components
The service's components are deployed and managed by the by the group [RTE Data Warehouse Core Team (rtedwcore@microsoft.com)](mailto:rtedwcore@microsoft.com). Please reach out to this group with your questions via email.

## Azure Synapse Workspace
This forms the core of the RTE Data Services and hosts our service's
 - Data collection pipelines: Managed by source control repository [RTEDataServices-Synapse](https://dev.azure.com/msresearch/MSR%20Engineering/_git/RTEDataServices-Synapse)
 - Dedicated SQL pools: Access to the SQL data is managed and limited to those that need it. To connect you have to use an SC-ALT identity.
 - Ondemmand SQL pools: As with the dedicated SQL end point access is managed and only granted to SC-ALT identities.
 - Spark pool: Is used by service data flows for more advanced data manipulation.

## Azure Data Lake Storage (ADLS)
We use ADLS for storing our long-term data. Data is typically partitioned by date, and accessed via the on-demmand SQL pool hosted in the Synapse workspace.

## Azure Blob Storage
Typically used to stage data before being processed and written to ADLS and SQL tables. We use LifeCycle policies to move older data to cool storage tiers and then delete it in line with our service's SLA.

## Azure Data Explorer (ADX) Cluster
Used for collecting streamed telemetry and utilization data from AML and other services required for our reporting. We have our own ADX cluster, but also utilize other groups ADX clusters. For example AzureSpend publish all the data we use for our Consumption Reporting in their ADX cluster.

## Azure Log Analytics Workspace
Similar to Azure Data Explorer, this is used to collect streamed and custom service telemetry data for our reporting. With a leaner implementation of KQL than ADX it is sometimes used as a intermediary service for some of our Azure Data Explorer tables.

## Azure User Assigned Managed Identities
We use the following User Assigned Managed Identities to access and collect upstream data.

- RTE-DataServices-MetaDatareader (7065496d-2298-4edb-bdf8-a0ff6107465b): Used for connecting with other data owners.
- RTE_AML_Diagnostics_Remediation (b75de4c4-a398-4061-957d-e06b4f8e5bcd): Used by Azure Policy's remediation task to apply missing AML Workspace Diagnostics settings.
- RTE-AzLifeCycle-mgmt (d71dbb76-cdae-4c13-9bc1-aee3ac5bcb22): Has User and Group reader access to Microsoft Graph for lifecycle management processes.


## Further service information

For further detailed information please see go to our services ADO repo [RTEDataServices](https://dev.azure.com/msresearch/MSR%20Engineering/_git/RTEDataServices)

