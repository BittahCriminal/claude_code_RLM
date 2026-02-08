This page explains how to monitor the health of AUM agent for GCR patching so when it comes to patch day we can ensure all our nodes have healthy AUM agent.

When AUM agent is not healthy then during patch deployment AUM will skip those nodes and therefore, the node remains on non-complaint state to make sure we have all the agent ready and healthy we have enabled Azure monitoring to check the health of AUM agent.

Preferably once a month on a Friday before patch Monday. Operations team to look into the monitoring dashboard identify the unhealthy agent and remediate. 

**How to check and find Unhealthy Agent**

Navigate to [GCR-Patching log analytical workspace](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/40641f8d-33f8-4948-b0ae-3df7e85e94e9/resourceGroups/GCR-patching/providers/Microsoft.OperationalInsights/workspaces/GCR-patching/Overview) on the left side menu under Monitoring click on Insights then click on Agents button on the middle from there you can see the healthy and unhealthy agent once you click on Unhealthy agents Azure will provide you a list of unhealthy node.

![image.png](/.attachments/image-e1b54432-5186-4125-8bd3-e60e166244e8.png)

![image.png](/.attachments/image-5ee8bf0a-5548-4de6-8516-dfe92c74c212.png)


**AUM agent remediation** 

- Now that you identify the unhealthy agent is it time to fix them. one of the main reason for this could be due to VM being offline or de-allocate, check to make sure VM is Online.
- Navigate to unhealthy agent VM and click on updates in left corner menu and make sure it is not onboarded to another log analytical workspace nor automation account. when the AUM agent is not onboarded correctly you usually see the error message similar to below

 ![image.png](/.attachments/image-a2ce361b-c2e1-47b2-b062-4e15c2dabed9.png)

If this is the case then make sure you onboard the node to GCR-patching again using the wiki docs.