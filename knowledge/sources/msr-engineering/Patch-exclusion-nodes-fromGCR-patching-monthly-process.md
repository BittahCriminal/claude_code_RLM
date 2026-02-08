### Excluding a Node from the SES Monthly Patching Process

**Important:**  
The person assigned a ticket in **GCRSupp** to exclude a node from the GCR monthly patching process must **notify the GCRAdmin team as soon as possible**.
After notification, follow the steps below to exclude the node from **automatic** and **manual** patching. **Keep the ticket open** until you:
*   Coordinate with the customer on an alternative patch window,
    
*   Manually patch the system, and
    
*   Confirm completion before closing the ticket.
    

* * *

### 🔧 Step 1: Exclude from **Automatic Patch Deployment**

1.  **Detach the node from its maintenance configuration:**
    *   Go to the node in the Azure portal.
        
    *   Click on **"Updates"**.
        
    *   Click on **"Scheduling"**.
        
    *   Click the **three-dot menu (⋮)** and choose **"Detach from existing maintenance configuration"**.


![image.png](/.attachments/image-fa0f581a-8854-4fef-ba2d-5d1e87724bfb.png)

        
2.  **Remove the node from the centralized maintenance configuration:**
    *   Navigate to:  
        [GCR-patching-automatic-maintenance-configuration](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/fc21bb37-3abe-40cb-8cc0-8768f1a4f086/resourceGroups/GCR-Patching-RG/providers/Microsoft.Maintenance/maintenanceConfigurations/GCR-patching-automatic-maintenance-configuration/overview)
        
    *   Click on **"Resources"**.
        
    *   Scroll through the list to locate the node to be excluded.
        
    *   Select the node and click **"Remove"** to exclude it from that month’s patch deployment.
        

* * *



![image.png](/.attachments/image-b7e88e20-4b58-4970-829d-023e07711110.png)

![image.png](/.attachments/image-318dd6b5-c71e-4682-a773-03fa356f7b52.png)

### 🔒 Step 2: Exclude from **Manual Patch Deployment**

Since the SES monthly patching process includes **two rounds**—automatic and manual—it is essential to ensure the node is also excluded from manual patching by manually removing the exception nodes from your manual deployment 


**How to Add the node back to the existing maintenance window:**

navigate to each node that you have excluded in previous steps in Azure portal and click on Updates then click on scheduling and then click on attach existing maintenance configuration and then search for GCR-patching-automatic-maintenance-configuration and click on Add from there Azure policy will add the node to the resources

![image.png](/.attachments/image-59a2cb27-22a6-4532-b649-a28de52330dd.png)