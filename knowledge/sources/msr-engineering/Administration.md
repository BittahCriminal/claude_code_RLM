[[_TOC_]]

## Open Service Issues
TODO: 
- Create ADO Query that filters by tag (PBISvc?)

## Service Elements

### Service View Diagram
Please add/edit to en
::: mermaid
 graph BT;
 A[(On-Premises Data Sources)]
 A2[("Cloud" Data Sources)] 
 B([PowerBI Connection])
 C[PowerBI On-Premises Data Gateway]
 D>PowerBI Reports]

 A --> C;
 A2 --> B;
 C --> B;
 B --> D;
:::


- [tnr-script-w3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/e82dbbc9-6196-4755-8bbb-9ce911a2072c/resourceGroups/TnR-Script-asr/providers/Microsoft.Compute/virtualMachines/tnr-script-w3/overview) (VM)
    - PowerBI Gateway Service
    - Azure Monitor
    - Azure Monitor Action Group
    - Inventory Tracking Solution
    - Kusto Query

### Monitoring Elements


[Azure portal link for TNR-SCRIPT-W3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/e82dbbc9-6196-4755-8bbb-9ce911a2072c/resourceGroups/TnR-Script-asr/providers/Microsoft.Compute/virtualMachines/tnr-script-w3/overview) (VM hosting the Onprem Data Gateway)
## PowerBI Gateway Service

#### Azure Monitor
Alerts setup based on KQL Query

#### Azure Monitor Action Group
Used to notify Teams channel(s) + Email

#### Inventory Tracking Solution
Enabled on this VM to monitor Windows Service history in Log Analytics

#### Kusto Query
Used to monitor the above inventor tracking solution log history to determine when the service has entered the "Stopped" state

[PowerBI Gateways page](https://msit.powerbi.com/groups/fd26e2e0-b498-478b-ac30-039597e1c8b7/gateways)

This page lists `data gateways`, and `connections` to data sources that you have admin rights to for data gateways listed in the `On-Premise Data Gateways` Tab.



### PowerBI Gateways & Connections

#### TNR-Script-W3 On-premises Data Gateway
- PowerBI-GW2 is listed in the portal as the friendly name for the data gateway.
- `tnr-script-w3` is:
    - an Azure virtual machine hosting the Onpremises data gateway
    - CorpNet domain joined via the express route on `MSRSupp_Corpnet_Resources` azure subscription. 
    - Running Windows Server 2016

#### Alerts Setup
We are monitoring the above VM and have alerts configured via action groups to send to our teams channel and email.

## TSG 

### PowerBI Service has failed to start
---
**Problem Description:** 
PBI Service has entered a stopped state. Please restart the service.

---

**Manual Resolution Guidance:**
- Elevate with your SC-Alt via https://aka.ms/sasweb to the TnR Server Silo
- RDP to tnr-script-w3
- Open `services.msc`
- Validate that the On-premises date gateway service is running
     - Start the service if it is not

---

**Automated Remediation**
- Automates restart of PowerBI Gateway Service based on alert trigger
- aka.ms/ link to this page and update alert description with aka.ms TSG

_TODO:_
-  #170675 

## References
- https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem
- https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-tshoot
- https://learn.microsoft.com/en-us/power-bi/connect-data/power-bi-data-sources
- https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-mashup-on-premises-cloud
- https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-performance
- https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-powershell-support
- https://learn.microsoft.com/en-us/data-integration/gateway/plan-scale-maintain