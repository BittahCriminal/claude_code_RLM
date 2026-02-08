[Update January 2021] See this page for how to gain access to [CloudMine](https://aka.ms/cloudmine) :
https://1esdocs.azurewebsites.net/datainsights/cloudmine/howto/get-access.html


If you need to query Azure DevOps data, your best bet is to do so via Kusto. To get access, join the [CloudMine-Data](https://myaccess/identityiq/ui/rest/redirect?rp1=/accessRequest/accessRequest.jsf&rp2=accessRequest/review?role=CloudMine-Data&autoSubmit=true) project in MyAccess (Non-FTE requires Level 65+ to approve). Once you're approved (probably by Trevor), you'll be able to connect to `1es.kusto.windows.net` using your Kusto client of choice.

If you don't have Kusto Explorer installed, you can try out [this sample Kusto query](https://dataexplorer.azure.com/clusters/1es.kusto.windows.net/databases/AzureDevOps?query=H4sIAAAAAAAEAEWPy0rEQBBF94L%2f0GSTBDLBWbhwEWFE3OngA1yX6Uu6MKke%2bpFI8OPtRDPuinsOt6raPvoAV%2bR7%2bPozzbaeWLSdfC0IeVlrCvRBHkV%2bmKPDPcbjyaf8LnKvLy%2b%2b1WTgoJ4jIt54gLptlNip2N3sdfnPj64j4ZkCW3mipDWNygbv4EGuNZki0b8lKzXkVWZsOk1nSwm%2bApLwThyWJc1rILdOu%2fPiSr1EWeEDC3uz0rO3lPg4DOR4hnqEZpLNP8G1kMA9ir%2bour4qK3UY4ajDptHYbTw99gNyzo4BOQEAAA%3d%3d).

Below is a query that attempts to find the projects and builds that are using the most runtime in our Azure DevOps organization:
Run it in your browser by going [here](https://dataexplorer.azure.com/clusters/1es.kusto.windows.net/databases/AzureDevOps?query=H4sIAAAAAAAEAKVTS2%2fTQBC%2b51eMfIlNnYQI9YSMBK2qSggKTSWO0diexEvsXWsfTVPx45ld20lcQCBxcXY9k5nv5cViRQRWWazBGdwSoCzBioZm9NSSNOKRIHeiLg3kB2i1%2bk6FndRkoVZql2OxW5d4MJBB%2fOY1XMAyeQuwWFwsIacCneHhFWmaGkBYzrgVatxOitoZSzqeLsnMd3xW872QpdqbuSQ7TeYlWszRUDx9%2f%2bw0XdPjXWv4%2fQcPBWDyA%2fZ%2bLHx15OiB4cK7DKTax2NUr2C2LBPwiD7xFjCWAWyE5mPpPG%2f46JczOtUyafGMVihpjuPv9BZl%2f%2fYz8pYsg6gxmgyhLqooqBUwhGqFBqJKMbUy4hn0ZInr31BYDzFbWdThNDvCTuHeyVC8EVKYKlSPfQH4FdaFq9EGJVnPQdc9QYGMsVH8wFw5z0l3BLgVZbCRGTetJ2Rc06AWz%2bRHauJ53pJasBRq0yeggx7%2bx2ng08nywDQEYcKoIPhwpZy0WeGfcZKG9wMb3hb3575yVMGXhksSSrzlmjbMf5A5hS%2fdVn85mtHP806%2fdPmy8UrdiJpDBV4JlIcOrVfCejIGajK9MJfQCOm8Ai338wzeoXTJZ4YyrCnJFMGAVaUcD%2bpU74Z2skmQbDFfZIhSTt2QTreGtfzlGzqF4sELzqtuXYMyM1YXaOON0g3adfCtRTkomEZllKQQeaSGf1P4Y2PVNTJibaLk%2f21%2fabY373Ttrf0nLqNE%2fJXQuHvMarzU%2fj5uoexjNs5bCqF6GxgHIqYHvEat8RA3uKO1lyceR5JRMIQEhsCeBRTO03MOK0RoMvkJpxHEp2QFAAA%3d).
```js
//See total usage and time-expensive builds by project
let lookback_days = (30 + 1);  //+1 because there's a 1-day lag
cluster('1es.kusto.windows.net').database('AzureDevOps').Build  
| where QueueTime >= now(lookback_days * -1d)   //Must stay first due to Kusto's optimizations
| where OrganizationName == "msresearch" and QueueName has "hosted"
| extend WaitTime=StartTime-QueueTime, RunTime=FinishTime-StartTime   //Calculate these because we care more about durations than timestamps
| summarize //Creates a list of total hosted time used by project and build
    BuildCount=count(),
    RunTime=sum(RunTime),
    WaitTime=sum(WaitTime)
    by DefinitionName, ProjectName
| where RunTime >= lookback_days * 5m  //Filter out any build that uses less than 5 minutes per day
| order by RunTime desc   //Should cause build list on next line to be ordered by most-expensive builds
| extend TotalRunHuman=strcat(format_timespan(RunTime,"d"), " days, ", format_timespan(RunTime,"h"), " hours")
| summarize //Creates a list of total hosted time used by project
    BuildCount=sum(BuildCount),
    TotalRunHuman=strcat(format_timespan(sum(RunTime),"d"), " days, ", format_timespan(sum(RunTime),"h"), " hours"),
    TotalRuntime=sum(RunTime),
    TotalWait=sum(WaitTime), 
    HostedBuilds=strcat_array(make_list(DefinitionName),", ") 
    by ProjectName 
| order by TotalRuntime desc
```