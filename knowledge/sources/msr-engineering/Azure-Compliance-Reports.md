
**Azure Security Pack Compliance Report** 
This Power BI report provides a compliance count and percentage of all hosts running Azure Security Pack by AI + R Organization and platform type. 

Author: mailto: Trevor@microsoft.com 
BI Support: v-togoda@microsoft.com
PM: v-shayus@microsoft.com  

https://msit.powerbi.com/groups/me/reports/8607acae-7018-4cbb-9238-0be29cd7a57d/ReportSection?ctid=72f988bf-86f1-41af-91ab-2d7cd011db47&openReportSource=ReportInvitation


**Base Inventory query:** 
Couple of current data sources.  First is Kusto and probably the easiest to work with.  It also has a lot of other data sources that we can combine.  The second is the AIRS cube.  It covers Azure subs, registration info, pccode and some service tree.  I don’t see the eviction so we might have to pull programmatically.  We’ll chat tomorrow about adding fidelity. (Source: Trevor Eberl) 

**Kusto data:** https://aka.ms/kwe?cluster=lens.kusto.windows.net&database=Shared&q=H4sIAAAAAAAAA41QTU%2BDQBC9k%2FAfJhyMJr3onQNB23CoNMV4JSs7aae2s2R2wcT4412wWCQl8fheZt5XgdJShS%2BCWCbZtiiaN1sJ1Y4MLxH1630YfMHHHgXhkVqynn9WJ4Q4hijJ4Aa2aFFJtYeVmKaOuvNazAErB7nsFNOncuenBRQ%2Fdv1pL%2FNLndETtySGT8jOo%2FRoGj3cjZJdoTINF7GcNHRBDoYY3ol1TMwocBsGAND1LMe%2FFoaKni0Lp1xj%2B4IPEVzaTNxiWOfpZkyuGtIL2KSp0V26JbHiCteK1Q4lOZKynk1qr9cOOAzuwPBU2kefMR3JT8edmejPulfmnx%2F8P%2Fkni38DXxMKeE4CAAA%3D 

ServiceTree_AIRSSubscriptionFeedV1
| where DivisionName == "AI & Research Group"
| project OrganizationName, ServiceGroupName , ServiceName , Environment , CloudName , SubscriptionName , SubscriptionId  , ServiceOid 
| join kind=inner (
   AIRS_Subscriptions | where Sub_Status == "2" | project SubscriptionId = MOCPSubscriptionGuid, PCCode , FinanceManagerAlias , ApproverAlias 
) on SubscriptionId 
|project SubscriptionId , PCCode , OrganizationName , SubscriptionName , ServiceName , ServiceGroupName , Environment , CloudName , FinanceManagerAlias , ApproverAlias , ServiceOid 

**AIRS cube info:** https://microsoft.sharepoint.com/teams/azureinternal/SitePages/AIRS%20Cube.aspx

**Kusto Query from Chris Erdman for ServiceTree compliance data** 

ServiceTree_AIRSSubscriptionFeedV1
| where DivisionName == "AI & Research Group"
| project OrganizationName, ServiceGroupName , ServiceName , Environment , CloudName , SubscriptionName , SubscriptionId  , ServiceOid 
| join kind=inner (
   AIRS_Subscriptions | where Sub_Status == "2" | project SubscriptionId = MOCPSubscriptionGuid, PCCode , FinanceManagerAlias , ApproverAlias 
) on SubscriptionId 
|project SubscriptionId , PCCode , OrganizationName , SubscriptionName , ServiceName , ServiceGroupName , Environment , CloudName , FinanceManagerAlias , ApproverAlias , ServiceOid 




