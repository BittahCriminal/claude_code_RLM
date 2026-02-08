**Prerequisite**

- Make sure your SC-ALT account is added to:
  -  for RTE: gcradmin-sc SG ( if your sc-alt account is not part of gcradmin-sc SG then request that to be added)
  - for MLS:  User_MLS-TechS-ITRED_ManualElevation SG.
-  PIM into Storage blob data contributor role by navigating to https://aka.ms/TnR/PIM or on pim portal under tasks -> My roles -> Azure resources and look for Storage blob data contributor for sescmartifacsts resource as highlighted below



![image.png](/.attachments/image-bb3d61d1-8baa-4ca1-8eab-3381c18c5a21.png)


Once you elevate and activate that role then you can install Ansible package as follow
Please ensure you have [azureCLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=script) installed.
```
curl -sL "https://aka.ms/InstallAzureCLIDeb | sudo bash"
```
-after installing you'll need to restart the shell with `exec -l $SHELL` for az login to work.

**For Installing Ansible on GCR Azure VMs:**



```
sudo -i 
az login --identity --client-id 1ac5cdf4-d3d7-4e2c-bc9a-ad6a88e60b55
cd /tmp
az storage blob download --account-name sescmartifacts --container-name artifacts --name linux/scripts/install_ansible_mi.sh --file install_ansible_mi.sh --auth-mode login && chmod +x install_ansible_mi.sh && ./install_ansible_mi.sh
```

**For Installing Ansible on GCR Onprem ( Arc) nodes:**


```
sudo -i 
az login
cd /tmp
az storage blob download --account-name sescmartifacts --container-name artifacts --name linux/ansible-onboard-arc/ansible-onboard-arc --file ansible-onboard-arc --auth-mode login && chmod +x ansible-onboard-arc && ./ansible-onboard-arc

```


**Note**: For **untethered** folks without sc-alt you must be added to SES-automation PIM first if you are not in there already and then for Az cli login you must login as :

`az login --tenant 72f988bf-86f1-41af-91ab-2d7cd011db47`

And then use SES-automation subscription on the screen when it asks which sub you want to have access to when running az login
![image.png](/.attachments/image-e34ac05e-2a99-464d-80f7-d0bc0b67c0c0.png)