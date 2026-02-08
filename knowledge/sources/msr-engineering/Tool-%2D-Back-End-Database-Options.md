# Introduction
This is a survey of database options, with a lens of a long term metrics project where the metrics were going to be entered manually at first into something that could also be treated as a sort of database. This may be useful for future projects.

## Guiding principals
Below is base list of what I consider principals for the selection process. 
- **Accessible** - PMs will be indirect, and possibly direct users of this solution. To ensure I'm not a technical gatekeeper, this solution should be accessible to those who are not SQL experts.
  - **Inserts** - There should be a method to insert metrics that is as easy as excel since we will be starting by manually inserting data, and working towards automation.
  - **Queries** - Querying the data using standard Microsoft tools should be easy
- **Performance** - High performance is not needed
- **Low Maintenance** - Since I don't need high performance, the solution should also not require a DBA to maintain it.
- **Cost Competitive** - This solution shouldn't cost many times more than the competing solutions.
- **Azure Native** - The service must be Azure Native. I don't wish to have a VM to patch and perform upkeep on where possible.


From: [List of all Power Query connectors - Power Query | Microsoft Learn](https://learn.microsoft.com/en-us/power-query/connectors/)

All below solutions are supported by [Azure Data Factory connectors](https://learn.microsoft.com/en-us/azure/data-factory/connector-overview).

### Sharepoint Online Lists

A highly accessible solution. There's an extremely similar, but not quite the same solution called Microsoft Lists.

- UI - Sharepoint. Easier to use than Excel.
- Cost: Free (part of sharepoint, which we don't get billed for)
- Serverless - No server management overhead
- Language Support:
    - REST - Has a [REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest)
    - Python - Via [shareplum](https://github.com/jasonrollins/shareplum), though the project was recently archived
    - Go - Via [Gosip](https://go.spflow.com/) library. [CRUD examples](https://go.spflow.com/samples/basic-crud)
    - Powershell - via [PnP Powershell module](https://learn.microsoft.com/en-us/shows/mvp-azure/work-sharepoint-online-lists-pnp-powershell).
- Comes with a number of columns that you can hide, but not delete (such as Title)
- Native functionality for Power Automate and Power BI (options are in-menu)
- Query Language - Nothing very advanced. However it's easily exported to Excel, or CSV for further analysis. It's also supported by [Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/connector-sharepoint-online-list?tabs=data-factory), so it could be used with Azure Data Explorer, or another db analysis solution.
- [Power Query Supports Nearly All Features](https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-online-list)

  

### Azure Table Storage

- Query Capabilities: Limited. Data can be exported as CSV to query platforms like ADX
    - ADX doesn't have a native Azure Table importer, it would need to be done multi step with something like ADF, or some other tooling.
- Cost: Inexpensive
- Language Support: Works with Golang, Python and Powershell
- UI - [Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer/)
- Inserts
    - Via the GUI in Storage Explorer
    - Via az cli:
        - az storage entity insert --entity "{\"PartitionKey\": \"P1\", \"RowKey\": \"R1\", \"Name\": \"Alice\"}" --table-name MyTable --account-name mystorageaccount --account-key myaccountkey
    - Via powershell:
        - Add-AzTableRow -table "MyTable" -partitionKey "P1" -rowKey "R1" -property @{"Name"="Alice"} -accountName "mystorageaccount" -accountKey "myaccountkey"
    - Go and python are also well supported
- Grafana Support: No
- Serverless - No server management overhead
- Can be used with ADX for Kusto style quries
- References
    - [Introduction to Table storage - Object storage in Azure | Microsoft Learn](https://learn.microsoft.com/en-us/azure/storage/tables/table-storage-overview)
    - [Azure Table vs Azure Cosmos DB for Table](https://learn.microsoft.com/en-us/azure/cosmos-db/table/support?toc=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fstorage%2Ftables%2Ftoc.json&bc=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fbread%2Ftoc.json)
    - [Design a Scalable Partition Strategy for Azure Table](https://design%20a%20scalable%20partitioning%20strategy%20for%20azure%20table%20storage/)

  
  

### Azure Blob Storage + Parquet (or CSV)

Parquet is a popular big data storage format natively supported by many platforms. However, it's likely overkill for our purposes.

- Fairly unlimited in terms of data storage. File based.
- Cost: Inexpensive
- Serverless - No server management overhead
- Grafana Support: No
- UI - 3rd party file viewers, may work with Excel?
- Add Hoc User Friendly Writes - Requires converting to a format that supports writing to it
- Querying: Need to import it into something like ADX or XLS
- File Management: Would need to create a file sorting method for services and timespans. Many of our Big Data platforms like ADLA support Parquet natively.
- References
    - [Parquet format - Azure Data Factory & Azure Synapse | Microsoft Learn](https://learn.microsoft.com/en-us/azure/data-factory/format-parquet)
    

  

### Azure Blob Storage + Excel

Summary: Excel is by far the easiest to use, and would likely be the best solution if we were only manually entering data with no automation.

- Difficult to act on it programmatically
- Query Capabilities: Native Excel, or it can be exported to query platforms like ADX
- [Power Query supports all features](https://learn.microsoft.com/en-us/power-query/connectors/excel)
- Single file based access, limited concurrency
- Very easy to use
- No compat with Grafana
- Serverless

  

### MySQL

Summary: MySQL is a very popular open source database solution with origins in serving simple websites. It still requires some light DBA knowledge to administrate and maintain.

- Can provision up to 16TB, with 3 IOPS
- SQL language
- Go, python, and powershell support
- [Power Query Supports all features](https://learn.microsoft.com/en-us/power-query/connectors/mysql-database)
- May not be the best fit since it's meant more for performance.
- Can stop the cluster to save on costs

  

### Azure SQL Server

Summary: SQL Server is a very popular Windows database solution with a wide range of applications. It requires DBA knowledge to administrate and maintain.

- SQL language
- Go, python, and powershell support
- [Power Query supports all features](https://learn.microsoft.com/en-us/power-query/connectors/sql-server)
- [Can attach to Grafana](https://grafana.com/docs/grafana/latest/datasources/mssql/)
- May not be the best fit since it's meant more for performance.
- Team knowledge with SQL server administration is variable.
- Can stop the cluster to save on costs

  

### PostgreSQL

Summary: Similar to MySQL, PostgreSQL is a very popular open source database solution. It still requires some light DBA knowledge to administrate and maintain. The Azure implementation has some limitations.

  

- 1TiB storage limit
- UI though Azure Data Studio
- Go, python, and powershell support
- Can attach to Grafana
- [Power Query support is Limited](https://learn.microsoft.com/en-us/power-query/connectors/postgresql) though it's probably enough
- Uses SQL for queries
- May not be the best fit since it's meant more for performance.
- Can't stop the cluster to save on costs

  

### Azure Data Explorer (Kusto)

Summary: This platform is meant to do ad-hoc analytics on big data, from disparate sources.

- [What is Azure Data Explorer? - Azure Data Explorer | Microsoft Learn](https://learn.microsoft.com/en-us/azure/data-explorer/data-explorer-overview)
- [Power Query support is very good](https://learn.microsoft.com/en-us/power-query/connectors/azure-data-explorer)
- [Can attach to Grafana](https://grafana.com/grafana/plugins/grafana-azure-data-explorer-datasource/)
- UI - Has a portal UI that can used for reads, not writes
- Query Capabilities: Uses Kusto for querying
- ADX is a distributed, cloud-based, columnar storage database. It uses a proprietary query language known as Kusto Query Language (KQL) to run queries against the data. The underlying architecture is designed to handle large volumes of diverse data, making it an excellent choice for tasks like log and telemetry data analysis.
- Can reuse some of our KQL queries and methods we use with Log Analytics Workstation
- [Works with Golang](https://learn.microsoft.com/en-us/azure/data-explorer/go-ingest-data)(API is in preview) and [Python](https://learn.microsoft.com/en-us/azure/data-explorer/python-ingest-data)
- Technically possible with Powershell using .NET
- Storage limited based on VMs involved. 4TB for 1VM and beyond.
- Easy to scale up or down as needed
- [Cost](https://azure.microsoft.com/en-us/pricing/details/data-explorer/https://azure.microsoft.com/en-us/pricing/details/data-explorer/) - Basic 2 core system no discount is $256/month. A bit higher than what a pgsql server would cost.
- Can manage with [az cli commands](https://learn.microsoft.com/en-us/cli/azure/kusto/cluster?view=azure-cli-latest)
- Can query with [kusto.cli](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/tools/kusto-cli)
- Can stop the cluster to save on costs, has automated stop option

  

## Others not reviewed, because they're for far higher scale, complexity, and expense.

[Azure Cosmos DB for Table](https://learn.microsoft.com/en-us/azure/cosmos-db/table/introduction)

- This is a supercharged version of Azure Tables

[Azure Data Lake Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)

- This is a supercharged blob storage with query capabilities

[Azure Data Lakehouse](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/)

- It's a data lake, it's data warehouse, it's where you're going to retire once you go mad from dealing with data all day long.