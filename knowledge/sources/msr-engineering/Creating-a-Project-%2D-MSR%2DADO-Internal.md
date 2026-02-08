Note: This process should work fine if all team members are FTEs, but there are concerns if some are external partners or potentially vendors from another division. See the following resources for guidance on that, and good luck deciding which to use.
- https://www.1eswiki.com/wiki/Adding_external_users_to_Microsoft_AAD_VSTS_account
----
Current permissions required for msresearch ADO administration. Located under Organization Settings -> Security -> Permissions. Add the user to be a member tp the following 2 groups below. 

[msresearch]\Project Collection Administrators
[msresearch]\Project Extension Admins

----
To create a project in the msresearch organization, follow the steps below. 
1. If you're using Edge, use your sc-alt profile. Anyone with permissions to create projects will typically need to do so with their sc-alt account.
1. Navigate to dev.azure.com/msresearch
1. Click on the **New Project** button in the upper-right of the projects list:
![image.png](/.attachments/image-9e408da5-91d4-46da-9060-ca31692b81dc.png)
1. Fill in the name and description fields and then click the **Create** button in the bottom right:
![image.png](/.attachments/image-77f50cfe-9c6a-41c5-b4c6-1527dddf887d.png)
1. Once the project is created, it should open automatically. If not, navigate to it.
1. Click on the Settings button in the bottom left:
![image.png](/.attachments/image-c8878789-7b80-4eee-9c9e-f7188b8af004.png)
1.Click the **Teams** link in the Project Settings list on the left:
![image.png](/.attachments/image-bfb4562a-bf9c-4023-971c-7afe25fb7550.png)
1. Open the default team by clicking on it, then click the **Add** button in the upper right.
1. Add users who should be part of the team here. This box is autocomplete enabled and supports multiple people in one operation.
![image.png](/.attachments/image-87593a08-aa74-4899-bebc-e8e2e9e73e86.png)
1.Add a project administrator from the settings Overview page.
![image.png](/.attachments/image-e7646c4f-8151-4fa2-82ac-dcd23abf9778.png)
   - You should definitely add a project administrator, but the request may not specify one. Sometimes the project administrator is everybody in the project.
----
This page's screenshots are from 03/25/2020.