# Introduction
One of the major costs for our Azure DevOps environment is the number of parallel build job slots we pay for. In late 2018, we were getting by with three, but as the number and size of projects in our organization has ballooned, we are (in mid-2020) occasionally seeing contention (where no build slots are available and users must wait for something to finish) with even 10 parallel build slots. Most of this usage is by a couple of projects, which is one of the things we need to check on every so often.

# Metrics
The objective for this aspect of our ADO administration is simply to allow most teams to work with minimal need to pay close attention to their pipelines. As such, our key results of success are as follows:
- Low (preferably <1m) wait times, which are caused only when there is contention.
- Rapid turnaround (same-day) of support requests.
- High cost efficiency

# Monitoring contention and usage
High usage is generally a good sign, but if usage is too high, users will have to wait for builds. As of July 2020, our [median run time](https://dataexplorer.azure.com/clusters/1es.kusto.windows.net/databases/AzureDevOps?query=H4sIAAAAAAAEAEWPy0rEQBBF94L%2f0GSTBDLBWbhwEWFE3OngA1yX6Uu6MKke%2bpFI8OPtRDPuinsOt6raPvoAV%2bR7%2bPozzbaeWLSdfC0IeVlrCvRBHkV%2bmKPDPcbjyaf8LnKvLy%2b%2b1WTgoJ4jIt54gLptlNip2N3sdfnPj64j4ZkCW3mipDWNygbv4EGuNZki0b8lKzXkVWZsOk1nSwm%2bApLwThyWJc1rILdOu%2fPiSr1EWeEDC3uz0rO3lPg4DOR4hnqEZpLNP8G1kMA9ir%2bour4qK3UY4ajDptHYbTw99gNyzo4BOQEAAA%3d%3d) is  6.5 minutes, and a wait time in excess of half that is going to stand out to the user. Lower is better here, and we can reduce wait times by paying for more parallel build slots, but that directly worsens our cost efficiency, so a balance must be found.

# Cost efficiency
As of 2020, each parallel job slot costs $40 per month, so our 20 parallel builds costs (40 * 20 * 12) $9,600 per year. We should be able to get by with 10, but some projects have been very bursty; one OneFuzz build runs in 9 slots concurrently, and each takes over 20 minutes to fail.

The documentation for Azure DevOps encourages a 1:5 job-slot-to-user ratio, which given our roughly 1200 active users, would result in over 240 job slots and a cost of nearly $10,000 per month. However, with ~60 [active users of _pipelines_](https://dataexplorer.azure.com/clusters/1es.kusto.windows.net/databases/AzureDevOps?query=H4sIAAAAAAAEAE3MsQrCMBAG4F3oOxyZ2sHB0SEOKo6K4guczWECTaJ3CaXFh9dUKi7Hz%2f0%2f3za7zixe0FtignOmTFfnCTYaQuzr5XplmurXn%2fiOwY2YXAxH%2fMy0BuWFSQi5tQowmC8ytRYFlI2SyKiCSPYe2Y0EF3pmkrSLOSTdlls3cBvmP7GekzlE3jt5dDgUszCRDfHfelLAkLTV4g1U5i1W0AAAAA%3d%3d) as of July 2020, 12 slots actually lines up nicely with the guidance.

# Adjusting parallel build slots
To adjust parallel build slots, go to the [Organization Billing settings page](https://dev.azure.com/msresearch/_settings/billing) and change the number in the textbox to the right of **MS Hosted CI/CI** as seen in the screenshot below, and then click the blue **Save** button at the bottom of the page.
![image.png](/.attachments/image-28f5a0fe-f4bd-42b3-a3a8-ac8a1d4a8afb.png)
Note that if you are a vendor, you will likely be unable to change this field without Trevor doing some configuration magicks on your behalf.