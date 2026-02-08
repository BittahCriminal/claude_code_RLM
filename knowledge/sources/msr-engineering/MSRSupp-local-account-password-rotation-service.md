For better security and compliance, we have an automated runbook in Azure which automatically rotate  msrsupp local account passwords for GCR on Onprem nodes every 3 months and upload the password on GCRCMVault. from there Ansible automatically deploy the new password to all odes.

## SLO/SLI/KVI

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal;">This service exists due to the fact that passwords eventually are shared if they remain static. To avoid this security issue we rotate passwords at the advisement of security professionals in our organization.</span>|
| --- | --- |
| SLI |How do we report errors on the above. Any hosts that didn't get the password? How do we audit that, or can we? |
| KVI | over 1000 GCR Onprem nodes including SANDBOX and ITP/singularity cluster uses this service and A dashboard showing the count of hosts using this service. |


**Notes:**

- We no longer add the `msrsupp` local account to GCR Azure VM or any other VMs managed by RTE. We encourage everyone to use their SSH public key. When a local account is needed you can create a new account via the Azure portal to access the VM.

- We no longer share our passwords with other teams. MLS has been informed that they must use and manage their own passwords.

- We use the `msrsupp` local account for GCR onprem nodes. This password is automatically rotated every 3 months and uploaded to GCRCMVault using Azure Automation runbook written in powershell. It can be found on [GCRCMVault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://gcrcmvault.vault.azure.net/secrets/msrsupp) Azure keyvault under secret. 

**How MSRSupp password rotation works**

We have an Azure runbook script that resides in the GCR-automation account under runbooks called [MSRSupp-Password-Rotation-Service](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-automation/providers/Microsoft.Automation/automationAccounts/gcr-automation/runbooks/MSRSupp-Password-Rotation-Service/overview). This PowerShell script generates a random password with at least 10 characters and uploads it [GCRCMVault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://gcrcmvault.vault.azure.net/secrets/msrsupp) Azure keyvault. From there Ansible uses the new password and rotates it for all the GCR onprem nodes managed via Ansible configuration management.

![image.png](/.attachments/image-99419a46-f216-4d2e-9374-8c6d574c75a7.png)


![image.png](/.attachments/image-cc8724ac-436b-401c-b3a2-24dc4e63f313.png)


