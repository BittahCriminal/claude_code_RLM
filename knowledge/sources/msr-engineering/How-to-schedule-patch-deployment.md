
[[_TOC_]]

## **Edit an Update Deployment**
### Parameters to create an Update Deployment ###
| Setting | Information|
|-|-
Name|Unique name to identify the update deployment.
Operating System|Linux or Windows
Groups to update|Define a query based on a combination of subscription, resource groups, locations, and tags to build a dynamic group of Azure VMs to include in your deployment. To learn more see, [Dynamic Groups](https://docs.microsoft.com/en-us/azure/automation/automation-update-management#using-dynamic-groups)
Machines to update|Select a Saved search, Imported group, or pick Machine from the drop-down and select individual machines. If you choose Machines, the readiness of the machine is shown in the UPDATE AGENT READINESS column. To learn about the different methods of creating computer groups in Computer groups in Log Analytics.     [Computer groups in Log Analytics](https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-computer-groups) 
Update Classifications| Select all the update classifications that you need. If an intranet WSUS is serving the updates instead of MU, only the approved updates will show up irrespective of what classifications are selected.
Updates to exclude| Enter the updates to exclude.  For Windows, enter the KB without the 'KB' prefix.  For Linux, enter the package name or use a wildcard.
Schedule settings|Select the time to start, and select either 'once' or 'recurring' for the recurrence
Maintenance window|Number of minutes set for updates.  The value cannot be less than 30 minutes and no more than 6 hours
Reboot Control| Determines how reboots should be handled.  Available options are:   <BR/>Reboot if required (Default)<BR/>Always reboot<BR/>Never reboot<BR/>Only reboot - will not install update

### How to schedule Update Deployment ###

**For Windows**
- Make sure you PIM into GCRProdEx1, GCRProdEx2, and GCRProdEx3 subs and then Navigate to [GCR-automation](https://ms.portal.azure.com/#@72f988bf-86f1-41af-91ab-2d7cd011db47/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-automation/providers/Microsoft.Automation/automationAccounts/gcr-automation/updateManagementMenuItem) account.

- Click on schedule update deployment. 
![image.png](/.attachments/image-17413c64-8be4-4b89-8d81-f214b76cd87c.png)
- for name lets make it a name which is relevant including date of patching if you are scheduling for Linux something like 220620-lin1 for the 1st group of linux machines scheduled on 6/20/2022.  Repeat for lin2, lin3 and win.

- Select operating system Windows or Linux (you need to schedule 2 different times for Windows and Linux.)  The other patching deployment can be scheduled 2 hours after the 1st one.

- click on groups to update navigate to Azure section and click on subscription, select GCRprodEx1, Ex2 and Ex3 subs and select all Resource groups for both subs e.g CPU-Sandbox and gpu-sandbox (Unselect the databricks RGs if necessary) then click on Add

- once you add it , it will show up under included items, click on preview and review make sure all the nodes you want to patch is included click OK and navigate to next section.  
NOTE - It's important to click preview to see if you've selected >1000 nodes.  If you don't do this it will allow you to schedule, then will error out when it actually runs.  Also if your preview doesn't show any machines, you probably failed to specify windows/linux on the previous step.

![image.png](/.attachments/image-ccf25705-8dd9-4da3-9433-4243e5dedc73.png)
- leave the other options alone and navigate to Schedule settings. select the date for your patching and starting time (give it about 15 minutes in case you need to make changes). make sure you click on Once otherwise, it will auto schedule for next month on same date which may not be our patching day
![image.png](/.attachments/image-06b73e59-e4b8-44c4-96fc-bac6c45a3c53.png)
- Maintenance window for Azure patch management is 6 hours maximum. Set the time to 120 on reboot options select Always reboot and click on create 
 ![image.png](/.attachments/image-f80cd04f-9249-4a9c-a938-af22d8364fe1.png)

**For Linux Azure**

- Repeat the same above process again and for Operating systems just select Linux.

- The linux patchiung deployment can be scheduled +2 hours from the windows one.


**Note:** Make sure two schedule two patch deployment for each platform after first round is finished. schedule another round one for Linux and one for Windows.

