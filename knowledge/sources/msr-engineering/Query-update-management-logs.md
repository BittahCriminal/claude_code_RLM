In addition to the details that are provided during Update Management deployment, you can search the logs stored in your Log Analytics workspace.

To search the logs from GCR-patching automation account, select update management and open the log analytics [workspace](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/40641f8d-33f8-4948-b0ae-3df7e85e94e9/resourcegroups/gcr-patching/providers/microsoft.operationalinsights/workspaces/gcr-patching/Overview) associated with our automation account and click on Logs.

Example of some of the useful Azure patch management query

- query that lists all available nodes within our GCR-patching automation account:

`Heartbeat
| summarize arg_max(TimeGenerated, *) by Computer`

![image.png](/.attachments/image-e0658c7d-d775-4865-bf82-cf545fa41fb0.png)

- List of missing updates in a specific node in this example ( GCRAZGDW102) in last 24 hours:

`Update
| where TimeGenerated > ago(14h) and OSType != "Linux" and (Optional == false or Classification has "Critical" or Classification has "Security") and SourceComputerId in ((Heartbeat
    | where TimeGenerated > ago(12h) and OSType =~ "Windows" and notempty(Computer)
    | summarize arg_max(TimeGenerated, Solutions) by SourceComputerId
    | where Solutions has "updates"
    | distinct SourceComputerId))
| summarize hint.strategy=partitioned arg_max(TimeGenerated, *) by Computer, SourceComputerId, UpdateID
| where UpdateState =~ "Needed" and Approved != false and Computer == "GCRAZGDW102.redmond.corp.microsoft.com"
| render table`

![image.png](/.attachments/image-c584d987-d085-4113-908d-9b6156e6cefc.png)

- Query for list of onboarded and available Linux Onprem nodes to our azure patch solution

`Heartbeat | where Computer contains "GCRSANDBOX" | distinct Computer`

![image.png](/.attachments/image-0a7197dd-5a96-4413-9036-6ce6263f3ea3.png)


- All nodes with missing updates in last one hour

`Update
|where OSType != "Linux" and UpdateState == "Needed" and Optional == "false" 
| project TimeGenerated, Computer, Title, KBID, Classification, MSRCSeverity, PublishedDate, _ResourceId
| sort by TimeGenerated desc`
![image.png](/.attachments/image-21cd5675-903e-4f55-941a-7386e5eef9e2.png)

**how to get query for specific Packages in this example "OMI" package** 

`Update
| where TimeGenerated > ago(5h) and OSType == "Linux" and SourceComputerId in ((Heartbeat
    | where TimeGenerated > ago(12h) and OSType == "Linux" and notempty(Computer)
    | summarize arg_max(TimeGenerated, Solutions) by SourceComputerId
    | where Solutions has "updates"
    | distinct SourceComputerId))
| summarize hint.strategy=partitioned arg_max(TimeGenerated, *) by Computer, SourceComputerId, Product, ProductArch
| where Product == "omi"
| render table`