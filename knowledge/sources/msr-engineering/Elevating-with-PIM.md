# Azure Privileged Identity Management

Privileged Identity Management for Azure Resources protects our organization from accidental or malicious activity by reducing persistent access to Azure resources. It provides just-in-time, or time-limited access when needed.

## Quick Start

1. Download the Azure Portal App 
    a. \\\cow\drop\pim has a copy of the portal app.

2. Launch the Azure Portal App from your start menu.

     

![image.png](/.attachments/image-44fec7b7-4fda-4d8b-9944-57668be0aab8.png)

 When prompted to login specify your SC-ALT (sc-###@microsoft.com) credentials.

![image.png](/.attachments/image-c79a520c-e081-4ac3-bc1c-a0b05f1cc300.png)

When asked for 2FA select "Sign in with your PIN or smartcard".

![image.png](/.attachments/image-bd8bdbc0-9d00-4934-8eab-5d4bdcf47f17.png)

Select your SC-ALT card when prompted.

Note: If your SC-Alt card does not appear like the below, see "Running into smartcard driver issues?" troubleshooting guidance below.

![image.png](/.attachments/image-5de0c956-43d2-4097-8d2a-98f50d7e22ab.png)

Note: 

- This should cache an access token the first time you successfully login, so future logins shouldn't require the physical alt card while that token is valid (I believe this is 90 days, if someone finds a way to check the token validity, please share).

- You may also need to "login" twice when using the Azure Portal App. 

- The next time you login to the portal app, it should automatically launch with the last login you did. 

- If you logout or switch users you should be able to simply select one of your identities to login with, without needing your SC-Alt card physically plugged into your device.

![image.png](/.attachments/image-6375f9d2-5525-4367-9944-f522861b5ca3.png)

3. Navigate to the PIM portal in the Portal App. 
Select the "All services" icon on the top left of the page, search for "PIM" and select that.

TIP: I recommend saving the PIM resource in your favorites sidebar for quicker access
![image.png](/.attachments/image-e1423b0c-2e84-41fe-81b2-50e5067b1293.png)

4. Under **Tasks**, select "**My roles**", then "**Azure Resources**".

![image.png](/.attachments/image-c3530cc6-654a-4b15-9e95-1b36b0ff06c4.png)

5. You should now see a list of resources (subscriptions) you can elevate into by activating your role.

TIP: On the top right, you can PIN this window on your dashboard to easily get here again quickly.

![image.png](/.attachments/image-143b2d50-3465-4ca2-b80c-65df385ab5d1.png)

6. Search for the subscription in the list you need to perform the administrative action on and you should only need to select **Activate**.

![image.png](/.attachments/image-f9148cf0-9982-4bbf-ab31-acdd061f44db.png)

7. After activation, refresh the portal app (F5 on your keyboard) and then select the directory icon and select the subscription you elevated into (I generally just select all subscriptions). Annoyingly this appears to be required each time you elevate, even if you already selected all your subscriptions previously.
NOTE: If rights are not assigned as expected close and re-open the app.

![image.png](/.attachments/image-ce5d024d-dc49-4ac6-9e52-78fefc28033b.png)

![image.png](/.attachments/image-4f1123cc-9b5b-4cd8-b88b-f97ee9fe704e.png)

8. You should now be elevated. Perform your administrative task!

## PowerShell Elevation Method

1. Install Az and AzSK powershell Modules if you haven't already

    a. Install-Module AzSK -Scope CurrentUser

2. Login-AzAccount

   a. Make sure you login with your SC-ALT creds
![image.png](/.attachments/image-659badef-323d-4994-8a87-030c89c96211.png)

![image.png](/.attachments/image-079dde5b-2f39-4b77-84fb-28344c53a324.png)
![image.png](/.attachments/image-dfe34967-ab3c-4cb2-96ea-7eb3c64b2672.png)

![image.png](/.attachments/image-1767273d-b707-44f4-b5b6-d6e4604e09b7.png)

3. Run the command **Get-AzSKPIMConfiguration** to get a list of your PIM eligible assignments



4. Using the above, you can use the Set-AzSKPIMConfiguration cmdlet to elevate into your eligible rolls.

    You need the subscriptionId (listed in ResourceId)
    the role name you are elevating into (listed in RoleName)
    duration to elevate (default is typically 8 so stick with that or less)


```PowerShell
Set-AzSKPIMConfiguration -ActivateMyRole `
                        -SubscriptionId <SubId> `
                        -RoleName <RoleName> `
                        -DurationInHours <Duration> `

```

from that you can create a function to elevate into subscriptions you commonly perform admin tasks on 

```PowerShell
#Elevate into multiple GCR subs
function Elevate-PIM
{
#GCR Prod 
Set-AzSKPIMConfiguration -ActivateMyRole `
                        -SubscriptionId fade1c90-3738-444a-874a-0d0005fb376d `
                        -RoleName Owner `
                        -DurationInHours 8 `
# GCR Prod 2
Set-AzSKPIMConfiguration -ActivateMyRole `
                        -SubscriptionId 40641f8d-33f8-4948-b0ae-3df7e85e94e9 `
                        -RoleName Owner `
                        -DurationInHours 8 `
}
#Perform the elevation
Elevate-PIM
```
for example assigning a secure group the  owner role in a subscription
```PowerShell
#Select and set the subscription with a variable to make it easier to work with.
$SubId = “REPLACE_WITH_SUBSCRIPTION_ID”

# Then add the secure group so you don’t lose access.
Set-AzSKPIMConfiguration -AssignRole -SubscriptionId $subId -DurationInDays 365 -RoleName "Owner" -PrincipalNames “REPLACE_WITH_YOUR_SECOURE_GROUP_NAME”

```



## Normal Workflow

1. Login to the Azure portal in your browser with your normal domain credentials. 

    a. You should have read access to all the Azure subscriptions we directly manage with your domain credentials, and you likely don't require administrative privileges for a lot of what you do. 

    b. Here is [the list](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/1664/RTE-Azure-Subscriptions-Access-SGs) of subscriptions we directly manage - if a subscription we manage isn't listed that should be or if you do not have access to a subscription in the PIM portal, please reach out to @<5CAC31D0-D85D-4056-A4D3-F252E353DDC5> and @<CF599EAD-570E-4E54-829B-A84AAF63D4CC> for onboarding that subscription to PIM.

2.  If the task you are performing requires administrative privileges, note the subscription(s) names or Ids you are working with (you'll use this info to elevate).

3. Login to the Azure portal app with your SC-ALT credentials.

4. Navigate to the PIM portal and elevate into the subscription(s) you noted earlier that you need to perform the admin task on.

## Common Issues

1. After elevating, subscriptions aren't showing up or I don't have access to resources still! 
   a. Try to refresh the portal (F5) for the new subscriptions to appear in your directory listing. This may take up to a minute for subscriptions to show up. If it's still not working after a minute, try to log out of the portal app and back in again if you don't see the subscriptions listed (SC-Alt creds will persist despite logging out so you shouldn't need your physical card). Once you log back in, make sure you select those subscriptions in your subscription directory filter (top section of the portal app). By default after elevating they will NOT be selected, so Azure search won't return any resources.

2. Azure Portal App login experience isn't working. 
   
   a.  Try to login with your domain credentials first, then use the login with other user option to login with your alt creds. I've seen that sometimes helps if you are having issues logging in with your SC-ALT creds and the portal app.

3. The subscription I need to access isn't showing up in my PIM eligible assignments!
   
   a. Reach out to Chris Erdman or Jordan Dahl to validate that you are in the right security groups, or that the subscription you need has been onboarded with PIM.

4. Running into SmartCard Driver issues?
![image.png](/.attachments/image-ad87bafc-aa35-4971-bd78-fe2df7914dbe.png)
    
    a. Install the Gemalto driver from \\\cow\drop\scaltdriver and run setup.cmd. If you're trying to remote a system that doesn't have this driver installed with your alt cred, it will not work. If you have an Azure Desktop VM, you may want to install this driver if you plan on elevating with your alt creds from that remote system.


5. Chrome Edge / Firefox / Chrome occasionally won't provide the cert prompt.
    a. Generally installing the above Gemalto driver and logging out and back in again seems to do the trick. Apart from using the Azure Portal app, I haven't found a better workaround. If someone has any suggestions/workarounds, please share.

6. An Administrative task in Azure that I'm doing requires my standard Corp credentials

    a. Please contact JordanD and Trevor/Katie to talk about your scenario and whether we can find a compliant solution, or if we need an exception.

    b. **NOTE If this is currently resulting in a work stoppage:** 
To unblock yourself, you may temporarily add your corp identity by elevating with your SC-Alt account, and temporarily adding your Corp account on the subscription you need. In parallel, you must immediately contact Trevor/Katie/JordanD to talk about your scenario and whether we can find a compliant solution, or if we need an exception.


## Provide Feedback

What's working well? What isn't? 
Do you have Suggestions/Improvements/Tips?

Please provide feedback in the [MSR-Green Teams Channel](https://teams.microsoft.com/l/channel/19%3a3536a6d6840c46a48e25576db92c6576%40thread.skype/MSR-Green?groupId=fd26e2e0-b498-478b-ac30-039597e1c8b7&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47) and to @<CF599EAD-570E-4E54-829B-A84AAF63D4CC>, @<5CAC31D0-D85D-4056-A4D3-F252E353DDC5>. 

You are empowered to improve/edit this wiki!


## Help us establish a compliant workflow
We are working toward improving the usability of administrative Azure management operations. We are identifying specific RBAC roles we can persistently add to the subscriptions we directly manage to make service management and operations easier (i.e. PIM is NOT required), while maintaining compliance requirements from the Protect the Admin initiative. 

The goal is to have our engineering and operations team very rarely needing to use PIM as we start enabling more of these roles across our subscriptions (SC-Alt will still be required for these Admin tasks but no elevation will be required for most things).

If you have a workflow that requires you to PIM frequently, please contact JordanD to discuss your scenario and whether this is an area we can improve.

Common scenarios we are looking into enabling without requiring PIM (SC-Alt still required): 

* VM Management (VM Restart/enabling boot diagnostics) 
* Keyvault: Modify Key Vault access policy
* 

Things that will still require PIM+SC-Alt:
* Assigning service principal/MSI permissions
* Resource deletion (potentially some RBAC roles we can use at the RG level if this is something we frequently do).
* 


####References

- <Link to AIRDEPOT>


- [CSEO PIM Guidance](https://microsoftit.visualstudio.com/OneITVSO/_wiki/wikis/OneITVSO.wiki?wikiVersion=GBwikiMaster&pagePath=%2FService%20Offerings%2FSecurity%2FPIM%20Guidance&pageId=2666)


- [Protect the Admin - Get to green using AzSK](https://microsoftit.visualstudio.com/OneITVSO/_wiki/wikis/OneITVSO.wiki?pagePath=%2FService%20Offerings%2FCommercial%20Sales%20and%20Marketing%2FModern%20Engineering%20Practices%2FProtect%20the%20Admin%20%252D%20Get%20to%20Green%20using%20AzSK%252DPIM%20Utilities&pageId=4157&wikiVersion=GBwikiMaster)

## Limitations and Gaps

|Limitation|Additional Details|WorkItem for tracking
|----|----|----|
|[PIM PowerShell Module Functionality](https://stackoverflow.microsoft.com/questions/153711/powershell-alternative-for-activating-azure-resource-roles-in-pim)| PowerShell module support doesn't support full PIM features (i.e. no support for targetting AMG, modifying RBAC settings for role assignment) [This maybe a workaround worth looking into](http://www.anujchaudhary.com/2018/02/powershell-sample-for-privileged.html) |
