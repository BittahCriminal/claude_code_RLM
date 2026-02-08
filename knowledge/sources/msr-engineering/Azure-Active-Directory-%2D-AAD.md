# Azure Active Directory

#### Useful Links

- https://aka.ms/aadonboarding 
- https://cseoaad
- http://aka.ms/ACEAADReview

#### Internal Stack Overflow 

- [Stack Overflow](https://stackoverflow.microsoft.com/questions/tagged/azure-active-directory+or+msa+or+rps+or+firstpartyapps+or+msal+or+adal+or+aad+or+microsoft-graph)

#### Discussion Groups

- AADTalk
- AskADAL
- DirectoryGraphD

## Requesting AAD API Permissions for an Application Registration 
If you have a [registered application](https://ms.portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) in the Microsoft AAD tenant, you may run into a need to request additional API permissions via https://aka.ms//AdminConsent. 

You may need a Service Tree service and https://aka.ms/rct entry for the permissions request form.

>If you need to get a new Service created, reach out to Katie for assistance

---


To register a new app registration: http://aka.ms/SES/AAD/Apps
> Note: If the app already exists, make sure you are listed as an Application Owner.

![MicrosoftTeams-image.png](/.attachments/MicrosoftTeams-image-1a68ac7c-96c2-40ab-a5d0-bc3ad08a742a.png)

If you need to sign in with a guest account (Microsoft Account) or identities from other AAD tenants, choose one of the multi-tenant options that meets your needs.
    - Otherwise, Single tenant is fine.
    - [optional] Redirect URI
    - [optional] If you have an existing Service, use the service tree ID, otherwise just hit next.



After you register the application, you should see an application (client) id.
You will want to save that
![image.png](/.attachments/image-746cabda-80f1-4870-b8d7-a95fff126948.png)

You also want to create a client secret or certificate after, which you use to authenticate with the AppID.
![image.png](/.attachments/image-cc8b1eb1-03b9-4b16-a456-8b04e78f2566.png)


Assuming it has the right AAD API permissions (most commonly these are actions in Microsoft Graph) for what you need, you should be good to go!

> Note: Permissions in this context is NOT RBAC for your service principal, but AAD claims associated with your app.  
>
> The following is a useful reference on the difference between [Delegated vs. Application permissions](https://learn.microsoft.com/en-us/graph/permissions-overview?tabs=http#permission-types)

In general, `delegated permissions` are less risky and easier to get Admin Consent for compared to `application permissions`.

![image.png](/.attachments/image-4444be72-ef98-4c91-9a28-3618fca32d07.png)

Otherwise, navigate to the API permissions blade shown. 

- The [Microsoft Graph Permission](https://learn.microsoft.com/en-us/graph/permissions-reference) reference page is useful to reference to identify what permission you need.

- If you are unable to verify or test the permissions you need in the Microsoft AAD Tenant, the guidance is to create a demo tenant (https://aka.ms/cdxdemo) for validating the AAD permissions you need to request.


Once you know the permissions you need, you can reference the [CSEO AAD](https://microsoft.sharepoint.com/teams/CSEOAAD#api-permission-risk-ratings ) page that has a table of the risk ratings for the various permissions you can request. 
- If the permissions requested are low risk, permissions are auto-approved. 
- Otherwise, DSR may reach out with more questions or asks that you need to provide, before they consent to the permissions.

At this point, you should be equipped to submit the initial permissions request on https://aka.ms/AdminConsent.


### Reference example using DeskPro

Below is showing that we had one permission already approved via a previous consent process.
- The 3 additional delegated permissions were in progress (but never finalized due to deprecating the service)
- The idea is you submit what you want first in the portal.

![image.png](/.attachments/image-fb7eae6d-92d2-47f9-a6c0-3f29950c1a9a.png)

So that when you go to the new request form page, it should have a drop down where you can select your app registration (or managed identity) and the appropriate request details.

![image.png](/.attachments/image-79035e90-5eda-48f4-a063-a71b564d2ea5.png)

> Note: Select the Guest Access option here if it's necessary for "Microsoft Account" (outlook.com/live ID) to access to your application.

The example permissions requested below are reflecting what we submitted in the Azure portal previously. 

You can also see the previous request that was completed  under Other Permissions.

![image.png](/.attachments/image-107500e9-2848-454c-976a-6bfb7d9a9e6e.png)

Submit the permissions you want prior to completing this form.

If there are issues, DSR will reach out asking for additional clarifying information that you may need to provide.