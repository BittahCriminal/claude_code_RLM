## Mission statement
The mission of RTE Data Services is to lower the cost of reporting across RTE's services by automating the collection and preparation of all the data required by the RTE team. Enabling RTE as a team to make more data driven business decisions.

## Operational Principals
The service uses the following basic principles to ensure we collect and report on only the data we need.

::: mermaid

flowchart LR
    getRaw["Get the RAW data.
    Write it to storage"]
    cleanupData["Clean the RAW data. Write to storage.
    Ready for ingestion in to structured tables"]
    import["Import data into structured tables
    ready to start reporting"]
    SQLviews["Create report specific views that we then grant users/groups access to."]
    aggregate["Aggregate and enritch data to extend reporting"]
    getRaw --> cleanupData -->  import <-->|optionally iterate| aggregate
    import --> SQLviews

:::

## Data Retention Periods
The *default* data retention provided by the service are
- Detailed data is available for 2 years.
- Aggregated data is available for 5 years.  

## Service Team
The service is managed by the group [RTE Data Warehouse Core Team (rtedwcore@microsoft.com)](mailto:rtedwcore@microsoft.com). Please reach out to this group with your questions via email. The service lead is [Ian Kelly](mailto:iankelly@microsoft.com).

## Making use of RTE Data Services
As stated above, this service is here to automate the collection and processing of the data needed to enable data driven business decisions. For us to help you, you need to understand at some level the data you need.

Recommended preparation
1. Define who your customers are and the business decision the data is going to inform. 
2. Try to build a test report in Power BI Desktop to validate that you can produce the metrics you need. Power BI Desktop can connect to many different data sources to enable the development of a concept report.
   - [Power BI Desktop Data Sources](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources)
   - An Excel spreadsheet is a great way to create static tables that can be connected to your report as a data sources.
3. Once you have your initial static concept report created, reach out to the [RTE Data Service Core Team](mailto://rtedwcore@microsoft.com) with the above information and a link to your report. One of the team will respond within 3 working days.

If you are interested in learning more about the service's components then [continue reading....](./RTE-Data-Services/Service-Components.md)