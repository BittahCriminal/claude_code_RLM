[[_TOC_]]

#Overview 

## How to setup the MSR Powershell Profile


## Option 1 from Redmond CorpNet
> In alignment with our Internet First initiative, I have migrated our MSRSUPP PS profile and all the files in that share to the path below.  Just change your reference in the local profile.ps1

- Security is based on SMB RBAC roles.  
    - Currently, RTE-ALL-RO should have R/W access to the share

   - `\\rtestorage.file.core.windows.net\psstore\profile.ps1`

## Option 2
The below seems to work from home but YMMV 
1. navigate to [psstore - Microsoft Azure](https://ms.portal.azure.com/#view/Microsoft_Azure_FileStorage/FileShareMenuBlade/~/overview/storageAccountId/%2Fsubscriptions%2Fe82dbbc9-6196-4755-8bbb-9ce911a2072c%2FresourceGroups%2Frteinfra%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Frtestorage/path/psstore/protocol/SMB)

2. Click "Connect"

    a. Change authentication method from AAD to storage account key

       >Note, I added `rte-eng-rw `to the `Storage Account Key Operator` role on that storage account. Others may need to do that as well if they experience list key storage account errors.

    b. click `Show Script`, then copy the script to clipboard

3. Open powershell (non-admin)
   a. Paste the clipboard contents from the script and press enter

At this point, you should be able to import the powershell profile by sourcing it with `. z:\profile.ps1`

The network drive we just mapped should should persist upon reboot:
   - `Z:` drive by default but you can change it during step 3, or modify the script
   - Optionally, if you want the MSR PS profile in an admin console as well, edit the script to add -scope Global as well to the following line e.g. 
>"`\\rtestorage.file.core.windows.net\psstore" -Persist -scope Global`

## How to load the MSR PS Profile automatically
1. Create a new file and save the output from the script
   - Using onedrive works well, I used the following `"C:\users\jorda\OneDrive - Microsoft\Tools\rtefileshare.ps1"`
   - [optional note] to get this to work in Admin powershell prompts
    - Edit `rtefileshare.ps1` to add -scope Global like the following e.g. 
         >`"\\rtestorage.file.core.windows.net\psstore" -Persist -scope Global`
![image.png](/.attachments/image-3951320e-3bc0-4a2f-91ab-2c9114b7f613.png)
- Load your local powershell profile
   - from powershell, you can type `notepad $profile`
  - if prompted, select `yes` to Create a new profile:
![image.png](/.attachments/image-fc53942d-7ba2-4983-8b04-ea3c4a2534a9.png)

- Paste in the below and edit the line that points to the script (e.g. step 6a), and then save

```powershell
#Checks path to remote share and loads the PS Profile
#otherwise attempts to remount the fileshare using the script 

if(test-path z:\profile.ps1){. Z:\profile.ps1}
else
{

#attempt remount and retry one more time
& 'c:\users\jorda\OneDrive - Microsoft\Tools\rtefileshare.ps1' #CHANGE ME

if(test-path z:\profile.ps1){. Z:\profile.ps1}
}
```
 
- Try to launch a new powershell window and validate if the MSR PS Profile shows up.
​
![image.png](/.attachments/image-ee291fd9-a807-4b10-93b5-bc433cd501dd.png)


## workaround for Windows PowerShell Unblock-File prompt 

- Navigate to `Internet properties `
    - open a Run window and `inetcpl.cpl`
    - Select the `Security` tab
    - Select the Local intranet
    - Select the Advanced
    - Add in `file://rtestorage.file.core.windows.net`
    - Open PowerShell and it should no longer prompt you to unblock the file

![image.png](/.attachments/image-a4079956-186a-4ba7-b393-447e3dba6d4b.png)







