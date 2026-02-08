http://aka.ms/sshHow2 - This Page 

**Create SSH Key** 
```
**Windows 11/Server 2019/2022/2025**
Open PowerShell(*not* admin prompt)
ssh-keygen -t ed25519 -C $env:USERNAME@microsoft.com #replace with your email.
ssh-keygen -y -f .ssh/id_ed25519|clip

**Linux**
ssh-keygen -t ed25519 -C sdahl@microsoft.com #replace with your email
cat .ssh/id_ed25519.pub

**Add Passphrase to key if you forgot**
ssh-keygen -p -f .ssh/id_ed25519

#correct your alias in the file for any mistakes without changing the keypair.
ssh-keygen -c -f ~/.ssh/id_ed25519 -C "alias@microsoft.com" 

#Update Public Key from clipboard to: 
start http://aka.ms/gcrssh

**Now you can SSH to your system: (update your alias & servername)**
ssh alias@microsoft.com@gcrsandbox888.redmond.corp.microsoft.com

```
**Problems**
```
**Windows**
**Run this to correct permissions if you see(WARNING: UNPROTECTED PRIVATE KEY FILE!) during connection**
$path = ".ssh\id_ed25519"
icacls.exe $path /reset
icacls.exe $path /GRANT:R "$($env:USERNAME):(R)"
icacls.exe $path /inheritance:r
```
###PassPhrase Driving you Crazy?
```
eval $(ssh-agent)
ssh-add .ssh/id_ed25519
ssh-add -l # shows hash of key(s) you have added.

```
##OpenSSH Configuration
You can do this by creating a config file in the ~/.ssh folder and create/adjusting the ~/.ssh/config file.
```
Host *
  User sdahl@microsoft.com
  ForwardAgent yes
  ForwardX11 yes
  Compression yes
  Protocol 2
  ServerAliveInterval 60
  ServerAliveCountMax 5
  TCPKeepAlive yes
  NoHostAuthenticationForLocalhost yes
  StrictHostKeyChecking no
  UserKnownHostsFile=\\.\NUL
  IdentityFile ~/.ssh/sdahl_ed25519_rsa

Host GCRSANDBOX*
  HostName %h.redmond.corp.microsoft.com

Host GCRAZGDL50*
  HostName %h.westus.cloudapp.azure.com

Host GCRAZCDL00* GCRAZGDL31* GCRAZGDL32* gcr-admin01
  HostName %h.westus2.cloudapp.azure.com

Host GCRAZGDL14* GCRAZGDL15* GCRAZGDL16* GCRAZGDL17* GCRAZGDL30* GCRAZGDL40*
  HostName %h.westus3.cloudapp.azure.com

Host GCRAZGDL11* GCRAZGDL12*
  HostName %h.northcentralus.cloudapp.azure.com
```
Troubleshooting:
```
Here is a quick test when someone has an issue and had been in one of the three SG groups above but fails to login.

Validate that user has an SSH key(linux) and that it matches their key:
/etc/ssh/get_ssh_key alias #run this from any node
ssh-keygen -y -f .ssh/id_ed25519  #user runs this from their PC

User Check(Linux check to see if user is registered in AD and in a MSR Security Group):
id alias@microsoft.com

Validate membership(change group from GCRAdmin)
sudo getent group gcradmin|grep alias@microsoft.com
sudo getent group amdgpudev|grep alias@microsoft.com

Check for login failure(On Node Testing when user can’t login):
sudo cat /var/log/auth.log* | grep alias@microsoft.com

Check for Allowed Group Membership
sudo cat /etc/ssh/sshd_config | grep Allow

cat /etc/ssh/sshd_config | grep AllowGroups
#username='sdahl@microsoft.com'
susername=`echo $username | cut -d@ -f1`;echo $username" ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$susername;usermod -aG adm $username;usermod -aG sudo $username

```
**Azure Entra Lookup Members**
[AMDGPUDEV](https://ms.portal.azure.com/#blade/Microsoft_AAD_IAM/GroupDetailsMenuBlade/Members/groupId/c239e204-b29a-4027-816a-20530f4d5812)
[JIT_MLS-Patching-Service_ElevatedAccess](https://ms.portal.azure.com/#blade/Microsoft_AAD_IAM/GroupDetailsMenuBlade/Members/groupId/92f833f3-0e31-443b-bcde-8ac67c452f8d)
[JIT_TnR-GCR-Admin_ElevatedAccess](https://ms.portal.azure.com/#blade/Microsoft_AAD_IAM/GroupDetailsMenuBlade/Members/groupId/ba7b5da8-a2ef-405f-8646-5a0e0c68a710)
[OPENPAIAMD](https://ms.portal.azure.com/#blade/Microsoft_AAD_IAM/GroupDetailsMenuBlade/Members/groupId/fda0c952-bf9f-4ee7-86e1-50b50adf2fbb)
[GCRMEMBERS](https://ms.portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Members/groupId/acca2b01-5230-4aef-a28d-709a63473383)
[GCRMEMBERS-SC](https://ms.portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Members/groupId/cea82699-680c-470e-8393-12ac683a399e)

**SSH over ARC**
[Azure PIM](https://ms.portal.azure.com/#view/Microsoft_Azure_PIMCommon/ActivationMenuBlade/~/azurerbac) to [GCR-ARC](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/overview) [subscription](https://ms.portal.azure.com/#view/Microsoft_Azure_PIMCommon/RBACRoleBlade/resourceId~/null/subjectId/af3c2536-1d54-4d29-adab-926d4e6699b4/bladeExternalName/MyAccess.ReactView/resourceExternalId/%2Fsubscriptions%2F46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/externalExtensionName/HubsExtension/menuId/access)
Overview - https://learn.microsoft.com/en-us/azure/azure-arc/servers/ssh-arc-overview?tabs=azure-cli
```
az login
az extension add --name ssh
az ssh arc --subscription 46e0b8e9-eb7f-4bbf-af34-a502c2d310f7 --resource-group GPU-Sandbox --local-user sdahl@microsoft.com --name GCRHYPC16x --private-key-file ~/.ssh/sdahl_ed25519_rsa

az ssh arc --subscription 46e0b8e9-eb7f-4bbf-af34-a502c2d310f7 --resource-group GPU-Sandbox --local-user sdahl@microsoft.com --name gcrsandbox555 --private-key-file ~/.ssh/sdahl_ed25519_rsa
az ssh arc --subscription 46e0b8e9-eb7f-4bbf-af34-a502c2d310f7 --resource-group GPU-Sandbox --local-user sdahl@microsoft.com --name gcrsandbox555 --private-key-file ~/.ssh/sdahl_ed25519_rsa "-L 2022:127.0.0.1:22"

Other interesting extensions
az extension add --name aksarc
az extension add --name amg
az extension add --name bastion
az extension add --name connectedk8s
az extension add --name k8s-configuration
az extension add --name k8s-extension
az extension add --name kusto
az extension add --name scvmm
az extension add --name ssh
```
Group Add user to SANDBOX System
```
#replace user and paste as sudo
username='alias@microsoft.com'
cat /etc/ssh/sshd_config|grep AllowG
id $username;susername=`echo $username|cut -d/ -f1|cut -d . -f 2`;echo $username" ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$susername;usermod -aG adm $username;usermod -aG sudo $username;cat /etc/sudoers.d/$susername;id $username;/etc/ssh/get_ssh_key $username
```
More help:
https://dev.azure.com/msresearch/GCR/_wiki/wikis/GCR.wiki/572/Support-Contacts
