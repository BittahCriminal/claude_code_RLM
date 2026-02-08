Source: Aaron Wiley 
To be used by: Ravi Togoda , Trevor Eberl

Host Compliance:
There are two components to this metric:
1.	On-prem asset compliance
2.	Azure compliance consisting of Windows_IaaS assets

For on-prem assets, I leverage the powerBI dashboard (https://msit.powerbi.com/groups/me/reports/67c9cc1d-777a-425d-b69e-4caf99e77c9c/ReportSection) and filter down the Computer OS to just 2008R2/2012/2012R2/2016.  This shows the complete scope for server assets in our lab space.
For Azure assets we have been waiting for our AzSecPack deployment to be complete so we start seeing host compliance data in Geneva.  I believe that we should start seeing this data now and once I’ve got the query I’ll share it with you.  In the interim, I’ve been just counting Windows_IaaS assets in our Azure subscriptions and assuming non-compliant.

How numerator and denominator are calculated
Numerator: All assets that are patched
Denominator: All assets in scope (on-prem from PBI report) + all Azure assets that are Windows_IaaS

Persistent Admins:
There are two components to this metric:
1.	Domain accounts that are in the admin groups for our on-prem assets
2.	Accounts that are listed as admins on our Azure subscriptions

For on-prem assets, I leverage the admin list that is published daily in the file share \\airscan\ess.  Currently, we’re filtering out local admins and only including domain accounts that exist on server assets (Server 2008R2, 2012, 2012R2, 2016).  We then dedupe that list to get a distinct list of admins and that’s our on-prem count.
For Azure assets, I’m running the following queries:
cluster("Azureslam").database("ASMSearchDB").Kusto_AIRSSubscriptionDetailV4 
| where SubscriptionStatus == "Active"
| where DivisionName =~ "AI & Research Group"
| where OrganizationName in ("MSR AI","MSR NExT","MSR Operations","Office of the Chief Economist") 
| project OrganizationName, ServiceGroupName, ServiceName, SubscriptionId, Environment, AccountOwner, SubscriptionRegisteredBy, BillingAccountId
| order by OrganizationName asc 

Then I extract the admins from AccountOwner and SubscriptionRegisteredBy, dedupe for the Azure admin list. Where applicable, I add both numbers together for our Persistent Admin counts and break down those counts by Org (L2).


MFA:
There are two components to this metric:
1.	Azure subscription admins plus on-prem domain admins (scoped to just server assets)
2.	Count fully isolated admin accounts.  This includes any account that is a non-info worker account such as accounts that are SC-ALT, AME, GME, etc

Basically, this is almost the exact same as what I’m doing above.  The only difference is the additional filter for our isolated accounts

How numerator and denominator are calculated
Numerator: All admins in Azure subscriptions hosted in the Microsoft Tenant that are federated (@microsoft.com addresses) + any admins on on-prem assets that are either a. fully isolated identities or b. admins on machines that have SC-Enforce option enabled
Denominator: All on-prem admins  + all Azure admins in the Microsoft Tenant


Security Monitoring KPI:
There are two components to this metric:
1.	Azure asset Security Monitoring
2.	On-prem assets that are reporting WEF events

For our Azure assets, it’s basically whether or not we have AzSecPack installed.  We’ve been focused primarily on Windows_IaaS machines but I think next month we’re going to increase the scope to include Linux assets as well.  Here is the query that I’ve been using for Azure:
// AI & Research AZSecPack Coverage
set truncationmaxrecords=5000;
let azsecpackcount = AzSecPackCoverageKPIDetail
                     | where DivisionName == "AI & Research Group"
                     | where PlatformType =~ "Windows_IaaS" 
                     | where IsRunningAzSecPack == "YES"
                     | summarize AzSecPackCount = count() by DivisionName, OrganizationName, PlatformType ;
let invcount = AzSecPackCoverageKPIDetail
               | where DivisionName == "AI & Research Group"
               | where PlatformType =~ "Windows_IaaS" 
               | summarize InvCount = count() by DivisionName, OrganizationName, PlatformType ;
invcount
| join kind= leftouter (
   azsecpackcount 
) on DivisionName, OrganizationName 
| project DivisionName, OrganizationName,  PlatformType, InvCount, AzSecPackCount 
| order by OrganizationName asc      

For on-prem assets, I leverage the powerBI dashboard (https://msit.powerbi.com/groups/me/reports/67c9cc1d-777a-425d-b69e-4caf99e77c9c/ReportSection) and filter out the OUs (currently it’s just Research-RED/SMSException) that don’t inherit WEF reporting.  Please note that we’re not filtering out any machines in this view, all windows-based machines should have WEF events enabled.

How numerator and denominator are calculated
Numerator: All assets reporting
Denominator: All assets in scope (on-prem from PBI report) + all Azure assets that are Windows_IaaS
