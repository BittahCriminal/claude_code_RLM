When we want to refresh on-premises data sources for Power BI reports, we need an on-premises gateway. This page shows information of Power BI gateway used by T&R Engineering team and stakeholders. 

Note: This service is no longer working

## SLO/SLI/KVI

The following are definitions of SLO/SLI and KVI. No actual metrics are available for this service currently.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal;">Ensure 99% uptime via our monitoring of service availability.</span>|
| --- | --- |
| SLI | Create a dashboard that shows the above metric |
| KVI | Number of dashboards this service supports|

### Methodology:
None of the above have been implemented, but here are some proposals and explanations:

**SLO** - May need to be adjusted but is a swag of the service availability. We could also make an automaton that logs into each Bastion to a test host on the other end to show success.  
**SLI** - Would use Azure Metrics to show availability metrics.
**KVI** - Uncertain if we can figure out the dashboards used by this, or the number access times of the dashboards connected to this service.

#How to access Gateway
###Necessary information
- Currently Gateway cluster name: PowerBI-GW2
- VM that hots the GW: [tnr-script-w3](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/e82dbbc9-6196-4755-8bbb-9ce911a2072c/resourceGroups/tnr-script-asr/providers/Microsoft.Compute/virtualMachines/tnr-script-w3/overview)
- Silo need to be elevated: TnR-Srv/USG-MSRSec 
- Recovery Key: [pbi-gateway-recoverykey](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/e82dbbc9-6196-4755-8bbb-9ce911a2072c/resourceGroups/TnR-Script-asr/providers/Microsoft.KeyVault/vaults/pbi-gateway-recoverykey/overview)

### Steps 
Below are steps to access gateway PowerBI-GW2 and configure/update gateway. 
- First you need to access VM tnr-script-w3 that installed the GW, to do this you need to use SASWEB/JIT from a corpnet connected system to elevate into the VM. Use either TNR_SRV silo or USG_MSRSEC-Redmond. 
- In the VM, click on start and type 'gateway' to find 'on-premises data gateway'. Sign in with your Power BI account (should be the same as corp account). Then you can configure the gateway that you are its admin, such like update it or change the configuration. Please note that if you want to configure a GW that is not owned by you, you need the recovery key to take over it. 

# How to configure Gateway on Power BI Services portal

### Download gateway

- If you want to install new PBI on-premises data gateway cluster on local machine or VM, follow below steps
  - Either Download GW from [PowerBI portal](https://powerbi.microsoft.com/en-us/gateway/) 
  - Or you can also do it by selecting download and click on Data Gateway through Power BI Services
![image.png](/.attachments/image-e0345e8f-add6-4e30-a185-f6099586934c.png)
  - Open On-Premises data gateway and sign in with account that you want it to be admin of this GW
  - Configure the GW as need

### Add new data sources to GW Cluster
- To enable on-premises datasets refresh, you need to add new data sources to GW cluster. Go to [Power BI Services portal](https://msit.powerbi.com/home) and click manage gateways 
![image.png](/.attachments/image-7361be92-2cab-4ef2-8c04-07f18d743251.png) 
- Select the cluster you want to use, in our case it is PowerBI-GW2. Then add new data sources. 
![image.png](/.attachments/image-61c7aca7-ff87-45b9-8d77-6b09741e2d32.png)

### If you want to add more Admins for this gateway
- Assign admin of new gateway
  - Go to PBI services portal, select settings and click on Manage Gateway
![image.png](/.attachments/image-7361be92-2cab-4ef2-8c04-07f18d743251.png) 
  - Select gateway cluster that you want to change and go to administrators tab, then add the one you want
![image.png](/.attachments/image-838db246-3d97-4f0a-a3ba-504ad32d0f84.png)

 