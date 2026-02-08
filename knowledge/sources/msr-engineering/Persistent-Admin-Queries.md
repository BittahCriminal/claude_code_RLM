## Prod + NonProd Persistent Access Check
The query below will check for persistent access of a user identity in production and nonproduction subscriptions.

Update `Upn=='alias@microsoft.com'` before running the query below.
to the alias you want to check access for.

---

Execute query in: 
- [Web](https://dataexplorer.azure.com/clusters/ampcprodpartner.centralus/databases/Reports?query=H4sIAAAAAAAAA5VTW2%2FaMBR%2B51ecpwUkEhBrC6hDGhqs3dZWjNC9TBMyzunw5tiWL6BM%2FfGzHQLaRRPzS6zzXeJz42hhnaPeMYrvCpgA5c5Y1O3E1EGrEZXbcEazPRrrTPbdE2S2Z6KQe5MJtEknK4glG2KwneRborHwoZkP5dYVTDb%2BK2%2B1vmWoiabbap0LosxW2tYz7LeoEWZsxwyT4oGUCJMJJCukWyG5%2FFrBC1iiwSCEGy2dSoCIAu5whzxSD79IWs9Ky29ILRyTum7xkOQbLl1IsKgEKRltf04WMa3kS%2Be61evx3wtx4pHLpwJHw5cpuSKD9GLTv0rH4z6m%2FYvReHC5GfZHw1F0qT2k0xR%2FMZgu7yN%2Bg3bK96Qy75ldoDbMV1rYKaVozHo5eztvd3wxnPA1gH9yH2SB53I%2FYPWJOG7P5U9%2FOI35x7uz%2FcM4nG2%2BvM%2FdxlDNlPXk%2F5D5nMVCyyJK6nk5dYsJ8GU%2Btc9XG440ZrBUtoqE2JuASg2HRjXaBvqbLs7OQVbP0UHVAEfRoxKTSaJ9wfVr33wtjXyyGZVlAr0evErrA4%2BL2XQ1h9v5cu6lf4xst7mGVeiG0Y%2BvC0BzX1XKI%2FWrm2%2FA64rFxeiG13RhJVVcmdrruH8eYKXfaFKq4KqktseAfxNnJbMw6PvzEwpv66EkBAAA)

- [Desktop](https://ampcprodpartner.centralus.kusto.windows.net/Reports?query=H4sIAAAAAAAAA5VTW2%2FaMBR%2B51ecpwUkEhBrC6hDGhqs3dZWjNC9TBMyzunw5tiWL6BM%2FfGzHQLaRRPzS6zzXeJz42hhnaPeMYrvCpgA5c5Y1O3E1EGrEZXbcEazPRrrTPbdE2S2Z6KQe5MJtEknK4glG2KwneRborHwoZkP5dYVTDb%2BK2%2B1vmWoiabbap0LosxW2tYz7LeoEWZsxwyT4oGUCJMJJCukWyG5%2FFrBC1iiwSCEGy2dSoCIAu5whzxSD79IWs9Ky29ILRyTum7xkOQbLl1IsKgEKRltf04WMa3kS%2Be61evx3wtx4pHLpwJHw5cpuSKD9GLTv0rH4z6m%2FYvReHC5GfZHw1F0qT2k0xR%2FMZgu7yN%2Bg3bK96Qy75ldoDbMV1rYKaVozHo5eztvd3wxnPA1gH9yH2SB53I%2FYPWJOG7P5U9%2FOI35x7uz%2FcM4nG2%2BvM%2FdxlDNlPXk%2F5D5nMVCyyJK6nk5dYsJ8GU%2Btc9XG440ZrBUtoqE2JuASg2HRjXaBvqbLs7OQVbP0UHVAEfRoxKTSaJ9wfVr33wtjXyyGZVlAr0evErrA4%2BL2XQ1h9v5cu6lf4xst7mGVeiG0Y%2BvC0BzX1XKI%2FWrm2%2FA64rFxeiG13RhJVVcmdrruH8eYKXfaFKq4KqktseAfxNnJbMw6PvzEwpv66EkBAAA&web=0)

- [cluster('ampcprodpartner.centralus.kusto.windows.net').database('Reports')](https://dataexplorer.azure.com/clusters/ampcprodpartner.centralus/databases/Reports)
```
let _ServiceId = cluster('servicetreepublic.westus.kusto.windows.net').database('Shared').DataStudio_ServiceTree_Hierarchy_Snapshot
| where DivisionName == 'Technology & Research Group' and Level == 'Service'
|project ServiceId;
let _Cloud = dynamic(['Public']);
//let _ServiceId = dynamic(['a5fde873-a6a2-4b06-990e-048925b70878']);
let _Source = dynamic(['ARM']);
GetAlwaysJitPersistentAccess_RDFE()
| union GetAlwaysJitPersistentAccess_Node()
| union GetAlwaysJitPersistentAccess_KeyVault()
| union GetAlwaysJitPersistentAccess_AzureSQL()
| union GetAlwaysJitPersistentAccess_Kusto()
| union GetAlwaysJitPersistentAccess_ARMSubscription()
| union GetAlwaysJitPersistentAccess_ARM_NonProd()
| where ServiceId in (['_ServiceId']) 
| where isempty(['_Source']) or Source in (['_Source'])
| where isempty(['_Cloud']) or Cloud in (['_Cloud'])
| where Upn=='alias@microsoft.com' // <------- UPDATE ALIAS HERE
| project ServiceId, ServiceName, ResourceId, ResourceType, Source, SourceId, AccessLevel, Upn, TopGroupName, Hierarchy, Timestamp, ReportTimestamp
| limit 20000
```

## Always JIT 
- Below AlwaysJIT queries are from the KPI Owner for T+R.
- These queries are split between NonProduction and Production subscriptions and by default just list the count of non-compliant assignments for each
- Modify the query to remove the summarize/count if you want to view the non-compliant assignments

### NonProduction

Execute: [Web](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fdataexplorer.azure.com%2Fclusters%2Fhttps%253a%252f%252fampcprodpartner.centralus.kusto.windows.net%2Fdatabases%2FReports%3Fquery%3DH4sIAAAAAAAEAG1RTW%252fCMAw9F4n%252fYHqBSgPBdROHSmwShyEE7DRNU5ZaEC2Nq9gFdR%252f%252ffQllg2nzIV%252fPz37PSSwKzDm3kmtNtROYwuCxr6xR3H%252b6ZvHGbbP3bidJjm%252fAorzwwcgOUtbDFMjDX0RZeU4D6fMmgbA9MPpQH5lXWJGXBbmlpyIgH3DYoUc4dd80FcJ0CmlkpKBcAUv0bFjQ6Rb5uUuLt3WXZI1ufmm4tbhXgkXQASFi7uDS6SCPsrNY9E5ZxuhkrakVYMltB5MsO9LW6PdG47yAXhAwPsXwn%252bU7ovfInFGpjIOeJifhwJBWvhDP48moCgMYUS2W6HWkqUwvprGm2ge7Z1a%252bum%252fdzszesCG3UOUlvkG9c2Rp27RluC5L5c1bzIlWM3hpzjauTg2Oqe2vdzudLyjVGGILAgAA&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062787906%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=0Beu2g50gYu34L1r%2BkxgaPRmiXj10IdHnLUFmr%2BAIpE%3D&reserved=0) [Desktop](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fampcprodpartner.centralus.kusto.windows.net%2FReports%3Fquery%3DH4sIAAAAAAAEAG1RTW%252fCMAw9F4n%252fYHqBSgPBdROHSmwShyEE7DRNU5ZaEC2Nq9gFdR%252f%252ffQllg2nzIV%252fPz37PSSwKzDm3kmtNtROYwuCxr6xR3H%252b6ZvHGbbP3bidJjm%252fAorzwwcgOUtbDFMjDX0RZeU4D6fMmgbA9MPpQH5lXWJGXBbmlpyIgH3DYoUc4dd80FcJ0CmlkpKBcAUv0bFjQ6Rb5uUuLt3WXZI1ufmm4tbhXgkXQASFi7uDS6SCPsrNY9E5ZxuhkrakVYMltB5MsO9LW6PdG47yAXhAwPsXwn%252bU7ovfInFGpjIOeJifhwJBWvhDP48moCgMYUS2W6HWkqUwvprGm2ge7Z1a%252bum%252fdzszesCG3UOUlvkG9c2Rp27RluC5L5c1bzIlWM3hpzjauTg2Oqe2vdzudLyjVGGILAgAA%26web%3D0&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062801731%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=XlDfc4XQjER09rhOcUBQ69EqUXo%2FYwcoBt8s83wKqKs%3D&reserved=0) [Web (Lens)](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Flens.msftcloudes.com%2Fv2%2F%23%2Fdiscover%2Fquery%2F%2Fresults%3Fdatasource%3D(cluster%3Aampcprodpartner.centralus.kusto.windows.net%2Cdatabase%3AReports%2Ctype%3AKusto)%26query%3DH4sIAAAAAAAEAG1RTW%252fCMAw9F4n%252fYHqBSgPBdROHSmwShyEE7DRNU5ZaEC2Nq9gFdR%252f%252ffQllg2nzIV%252fPz37PSSwKzDm3kmtNtROYwuCxr6xR3H%252b6ZvHGbbP3bidJjm%252fAorzwwcgOUtbDFMjDX0RZeU4D6fMmgbA9MPpQH5lXWJGXBbmlpyIgH3DYoUc4dd80FcJ0CmlkpKBcAUv0bFjQ6Rb5uUuLt3WXZI1ufmm4tbhXgkXQASFi7uDS6SCPsrNY9E5ZxuhkrakVYMltB5MsO9LW6PdG47yAXhAwPsXwn%252bU7ovfInFGpjIOeJifhwJBWvhDP48moCgMYUS2W6HWkqUwvprGm2ge7Z1a%252bum%252fdzszesCG3UOUlvkG9c2Rp27RluC5L5c1bzIlWM3hpzjauTg2Oqe2vdzudLyjVGGILAgAA%26runquery%3D1&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062811380%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=CYMZsEj4OQ6JkSUDnuEQNOnDimzgiqneD7bGvdwATag%3D&reserved=0) [Desktop (SAW)](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fampcprodpartner.centralus.kusto.windows.net%2FReports%3Fquery%3DH4sIAAAAAAAEAG1RTW%252fCMAw9F4n%252fYHqBSgPBdROHSmwShyEE7DRNU5ZaEC2Nq9gFdR%252f%252ffQllg2nzIV%252fPz37PSSwKzDm3kmtNtROYwuCxr6xR3H%252b6ZvHGbbP3bidJjm%252fAorzwwcgOUtbDFMjDX0RZeU4D6fMmgbA9MPpQH5lXWJGXBbmlpyIgH3DYoUc4dd80FcJ0CmlkpKBcAUv0bFjQ6Rb5uUuLt3WXZI1ufmm4tbhXgkXQASFi7uDS6SCPsrNY9E5ZxuhkrakVYMltB5MsO9LW6PdG47yAXhAwPsXwn%252bU7ovfInFGpjIOeJifhwJBWvhDP48moCgMYUS2W6HWkqUwvprGm2ge7Z1a%252bum%252fdzszesCG3UOUlvkG9c2Rp27RluC5L5c1bzIlWM3hpzjauTg2Oqe2vdzudLyjVGGILAgAA%26saw%3D1&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062818460%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=hCiWxdQR4fnX1yWfIJeF7Xrlcs1%2BdL5edMKkHoRD3KI%3D&reserved=0) 
https://ampcprodpartner.centralus.kusto.windows.net/Reports
``` cs
let IsAltAccount = (['alias']:string){
	alias startswith "sc-" or alias startswith "alt_"
};	 
UserAccessReportNonProd
| where AccountType == "User" 
	and Persistence == "Persistent" 
	and AccessPolicy startswith "Elevated"
	and (IsAltAccount(Alias) == False 
	or Scope == long(1)) 
	and ServiceId != "00000000-0000-0000-0000-000000000000"
	and Domain !contains "prdtrs01.prod.outlook.com"
| where Source contains "ARM" and DivisionName contains "Technology"
| summarize count() by ServiceId, Source
| count 
```

### Production
Execute: [Web](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fdataexplorer.azure.com%2Fclusters%2Fhttps%253a%252f%252fampcprodpartner.centralus.kusto.windows.net%2Fdatabases%2FReports%3Fquery%3DH4sIAAAAAAAEAD3KwQqCQBAA0LtfMXixoF%252fwIFRgh4jWPmCbhhzQWZnZVTb6%252bKxD5%252ffc4XghNbZIEm9G2iCS2ZWmoLF4w9KTErTSDIvPdmo7h2EiqGuoOk1Uwf%252fseWbjIGc%252fEmCQ6FkMykjYSxjCM5drtTSOXvn1HUniZgv3DI50ZqT2sQMXkiKt8cdQFB9uhzQSoAAAAA%253d%253d&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062831239%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=IshCJ0nkwFOwzrwRxKAF882mrP6n1l%2Fq3W42LYc%2BWII%3D&reserved=0) [Desktop](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fampcprodpartner.centralus.kusto.windows.net%2FReports%3Fquery%3DH4sIAAAAAAAEAD3KwQqCQBAA0LtfMXixoF%252fwIFRgh4jWPmCbhhzQWZnZVTb6%252bKxD5%252ffc4XghNbZIEm9G2iCS2ZWmoLF4w9KTErTSDIvPdmo7h2EiqGuoOk1Uwf%252fseWbjIGc%252fEmCQ6FkMykjYSxjCM5drtTSOXvn1HUniZgv3DI50ZqT2sQMXkiKt8cdQFB9uhzQSoAAAAA%253d%253d%26web%3D0&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062837431%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=rLh1kR1EK7SIAWhtsLLMj0LHYGOFKw%2FMMDHRr3IvKbI%3D&reserved=0) [Web (Lens)](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Flens.msftcloudes.com%2Fv2%2F%23%2Fdiscover%2Fquery%2F%2Fresults%3Fdatasource%3D(cluster%3Aampcprodpartner.centralus.kusto.windows.net%2Cdatabase%3AReports%2Ctype%3AKusto)%26query%3DH4sIAAAAAAAEAD3KwQqCQBAA0LtfMXixoF%252fwIFRgh4jWPmCbhhzQWZnZVTb6%252bKxD5%252ffc4XghNbZIEm9G2iCS2ZWmoLF4w9KTErTSDIvPdmo7h2EiqGuoOk1Uwf%252fseWbjIGc%252fEmCQ6FkMykjYSxjCM5drtTSOXvn1HUniZgv3DI50ZqT2sQMXkiKt8cdQFB9uhzQSoAAAAA%253d%253d%26runquery%3D1&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062843453%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=b4dRy71qYUiJZn0cmkIe7ARTKaDlxxnYbh6%2ByDTMmiw%3D&reserved=0) [Desktop (SAW)](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fampcprodpartner.centralus.kusto.windows.net%2FReports%3Fquery%3DH4sIAAAAAAAEAD3KwQqCQBAA0LtfMXixoF%252fwIFRgh4jWPmCbhhzQWZnZVTb6%252bKxD5%252ffc4XghNbZIEm9G2iCS2ZWmoLF4w9KTErTSDIvPdmo7h2EiqGuoOk1Uwf%252fseWbjIGc%252fEmCQ6FkMykjYSxjCM5drtTSOXvn1HUniZgv3DI50ZqT2sQMXkiKt8cdQFB9uhzQSoAAAAA%253d%253d%26saw%3D1&data=05%7C02%7Ccllieu%40microsoft.com%7Cc6739d0336d14fba5c0b08dc9146b29f%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638544980062849539%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=7hPGXNV%2BxzX1CXl3rMjiIyU1kYVnGzmr1qRNO8cvz%2FQ%3D&reserved=0)https://ampcprodpartner.centralus.kusto.windows.net/Reports

``` cs
SEFPersistentUserAccessReport
| where InAlwaysJITScope == 'True'
| where DivisionName contains "technology"
| summarize count() by ServiceId, Source
| count
```