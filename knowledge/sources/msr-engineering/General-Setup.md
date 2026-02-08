## HyWay Setup
- [User Guide](https://microsoftapc.sharepoint.com/:w:/t/HyWay/EaxAugP2wdhFszNOYfnrpe4BTBSZV150rdjwzrUak5hdMw?e=hnbQTl)

<hyway url> / map

# System Setup

## Windows Settings Setup

Current Demo setup as of 6/15/23:
For ease of use/Kiosk mode use a non-domain joined machine with autologin enabled **DO NOT DOMAIN or AAD JOIN.** 
Domain Joined PC's with auto login enabled are NOT compliant for public spaces.  


Rufus Installation (For easy Local Auto Login)
We HIGHLY recommended using this style of installation. 
https://pureinfotech.com/rufus-create-bootable-windows-11-usb/


For our current version dubbed V1.0 we are using a Windows 11 install created from Rufus with the following options enabled
![image.png](/.attachments/image-9582f3db-920f-494d-a970-d8c6dd3eb074.png)

This will automatically create an account named "hyway" with no password as an administrator. 
**NOTE- At first login, it will prompt you to change the password DON'T just hit enter and leave it blank or autologin will break**




**Win 11 License-** 
We have requested a MAK license for Demo use. Please contact SES-hyway@services.microsoft.com



## MSA Account for Hyway use ##
Since we are using a local account for autologin, we now need to use an MSA to sign into our Edge profile and authenticate into HyWay. At the moment we are using a single MSA account for this. **Msr-hyway-1@outlook.com**
The password for this account can be found in the Keyvault located [here](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/a5224fa9-985e-4c4a-9636-738af9bc5e82/resourceGroups/Hyway-Collaboration/providers/Microsoft.KeyVault/vaults/Hyway/overview)(Permissions need to be granted manually at the moment please contact ses-hyway@services.microsoft.com for secure access to password)

The Hyway Enterprise App currently requires 2FA as well, in order to comply with this requirement, we have enabled email code based 2FA and pointed this account to a group email address of 
**ses-hyway@service.microsoft.com** you can request to be added to this group in Outlook Web or Desktop. 
![image.png](/.attachments/image-55e028cb-92a3-4db4-b639-43dd8623f308.png)

After you are in the group, you'll be able to obtain 2FA codes via email. 

#Hyway Sign in and usage.
Our main goal is to try and set up the Hyway Experience to be as easy as possible. 
In our current V1.0 version we are utilizing Edge profiles, and Edge Apps to help achieve this goal. 


##Edge profile sign in-
The first thing we want to do is create a new Edge profile. This only needs to be done once on each machine. 
![image.png](/.attachments/image-44f9da9c-ba0d-4841-9c6e-3a5288e42d8f.png)
Once the profile is created, choose to Sync data. This account 

## Installing Hyway as an Edge App- 
Here's a quick Video explaining how to install Hyway as an Edge App. 
[Hyway as Edge App](https://microsoft-my.sharepoint.com/personal/johjo_microsoft_com/_layouts/15/stream.aspx?id=%2Fpersonal%2Fjohjo%5Fmicrosoft%5Fcom%2FDocuments%2FHywayAppmode%2Emkv&ga=1)

**Office Installation**- 
Office is often needed depending on the use case of the Hyway Kiosk. For office installation you can use the common office installer.

Please follow the common office installation instructions. 
[https://www.microsoft.com/en-us/microsoft-365/download-office](Office Install) 

For Office installation Licensing you can either use the 1 week trial or you can procure keys from the internal keys service. Utilizing your Corporate account for automatic licensing IS NOT recommended. 
[https://mskeys.microsoft.com/Home](Mskeys)

This process can take up to 5 business days, please plan accordingly. 



##Audio Settings- 
Hyway now adopts the audio settings from Windows. Set your Speaker/Microphone and Hyway will respect it. If you make changes, make sure to refresh the Hyway Web App

## Surface Hub Settings Setup
Coming soon

# Troubleshooting

## Speaker/Mic Troubleshooting
HyWay utilizes Microsoft Edge for setting up the audio SubSystem. Behind the scenes this app will utilize your Default Sound devices. Ensure that your Windows Mic/Speakers are set up properly. 

### Hub OS Limitations

## 3rd Party Applications


#### Configuration Settings

#### Troubleshooting
