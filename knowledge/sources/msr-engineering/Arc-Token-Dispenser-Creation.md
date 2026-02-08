
# Function App Creation Considerations
Ideally this will become a bicep deployment, but for now this is manual.

## Function App Creation
In creating a new function app, follow the following steps
- Create a Premium Function App
  ![image.png](/.attachments/image-acdc6d97-160c-498a-be32-ceea8f7ef586.png)

- Here's a sample of the first creation page, of note:
  - Be sure the location matches the name
  - Powershell Core as the Runtime stack
  - Version should be 7.4 (or the recent)
  - Region should be either WestUS3, or South Central. EastUS is displayed for sample purposes, but we only use that for our dev instance.
  - Operating System should be Windows

  ![image.png](/.attachments/image-f46de0e6-5e46-468b-a505-e89fdff23af1.png)

- Create a new storage account at the next page
- In networking, keep the default "Enable Public Access"
- Enable Application Insights on the next page

## Function App Configuration
### Assigned Identity Work
- Enable System Assigned Identity from the Security -> Identity blade in the Azure Portal
- Assign the following User Assigned Identities to the Function App:
  - [GCRArcOnboardingUAMI](https://ms.portal.azure.com/?feature.tokencaching=true&feature.internalgraphapiversion=true&feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourcegroups/arc-onboarding/providers/microsoft.managedidentity/userassignedidentities/gcrarconboardinguami/overview)
  - [gcransibleaccess](https://ms.portal.azure.com/?feature.tokencaching=true&feature.internalgraphapiversion=true&feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourcegroups/gcr-ansible/providers/microsoft.managedidentity/userassignedidentities/gcransibleaccess/overview)
  - [samleaccess](https://ms.portal.azure.com/?feature.tokencaching=true&feature.internalgraphapiversion=true&feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourcegroups/samle/providers/microsoft.managedidentity/userassignedidentities/samleaccess/overview)
  - [gpumetricsaccess](https://ms.portal.azure.com/?feature.tokencaching=true&feature.internalgraphapiversion=true&feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourcegroups/gpumetrics/providers/microsoft.managedidentity/userassignedidentities/gpumetricsaccess/overview)
- Give the System Assigned Identity "Key Vault Secrets User" access to the [tokendispenservault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/arc-onboarding/providers/Microsoft.KeyVault/vaults/tokendispenservault/overview) AKV
- Add environment variables to the Function App with the following command (edit the function appand resource group name)
  ```bash
  az functionapp config appsettings set \
    --name gcr-arc-onboarding-wus3 \
    --resource-group gcr-arc-onboarding-wus3 \
    --settings \
      ansible_req_client_id="@Microsoft.KeyVault(SecretUri=https://tokendispenservault.vault.azure.net/secrets/ansible-req-client-id/)" \
      gcr_arc_onboarding_client_id="@Microsoft.KeyVault(SecretUri=https://tokendispenservault.vault.azure.net/secrets/gcr-arc-onboarding-req-client-id/)" \
      gpumetrics_req_client_id="@Microsoft.KeyVault(SecretUri=https://tokendispenservault.vault.azure.net/secrets/gpumetrics-req-client-id/)" \
      samle_req_client_id="@Microsoft.KeyVault(SecretUri=https://tokendispenservault.vault.azure.net/secrets/samle-req-client-id/)"
  ```
### App Keys
- In the Functions -> App Keys menu make the following keys:
  - archosts which can be found [here](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://gcrcmvault.vault.azure.net/secrets/gcr-arc-onboarding-app-key/e37000ec42fe4f0483611d8dd59e551b).
  - healthcheck which can be found [here](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/GCRCMVault/providers/Microsoft.KeyVault/vaults/GCRCMVault/secrets)

## Deployment
- For a new system, you'll want to add it to the Azure_Function-arc_token_dispenser [pipeline](https://dev.azure.com/msresearch/MSR%20Engineering/_git/Azure_Function-arc_token_dispenser?path=/azure-pipelines.yml) so it gets automatically deployed.
- Manual deployment can be done with Visual Studio Code, or the CLI.
  - You'll need to check out the [codebase](https://dev.azure.com/msresearch/MSR%20Engineering/_git/Azure_Function-arc_token_dispenser)
  - For the CLI you can use the script below:
  ```bash
  az account set --subscription 923239b9-27ca-40bb-9868-3932f1fb42a2 
  zip -r publish.zip ansible-* gcr-arc-onboarding-* gpumetrics-* host.json profile.ps1 requirements.psd1
  az account set --subscription 46e0b8e9-eb7f-4bbf-af34-a502c2d310f7
  az functionapp deployment source config-zip -g <resource_group> -n <app_name> --src publish.zip
  rm publish.zip
  ```

## Health Checks
- From the Function App Overview, click "Health Check" on the top right
- Click "Enable"
- Make the path: `/api/ansible-vault-req?code=<health app key>`
  - Where the app key is the key you created above, the text is in this [secret](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/GCRCMVault/providers/Microsoft.KeyVault/vaults/GCRCMVault/secrets).
  - Make the load balancing threshold at 5 minutes
- Click save

## Scale Out
- From the Scale Out blade, create some reasonable settings:
![image.png](/.attachments/image-22bc8095-b773-497d-b931-e394563d0673.png)

## Test
Test that you can get a token from the token dispenser from an on prem GCR Arc sandbox host. Ensure you have the FUNCTION_KEY value from [here](https://ms.portal.azure.com/?feature.msaljs=true#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://gcrcmvault.vault.azure.net/secrets/gcr-arc-onboarding-app-key/).

A curl command like this will work:
  ```bash
    export FUNCTION_KEY=<function key value>
    curl -sL https://gcr-arc-onboarding-sc.azurewebsites.net/api/gcr-arc-onboarding-req?code=$FUNCTION_KEY  
  ```
Ensure you get a token back from this command.

## Add to Traffic Manager
- Go to the [endpoints blade of the gcr-arc-onboarding Azure Traffic Manager profile](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/46e0b8e9-eb7f-4bbf-af34-a502c2d310f7/resourceGroups/arc-onboarding/providers/Microsoft.Network/trafficmanagerprofiles/gcr-arc-onboarding/endpoints) and click "Add"
- Use the below example to add your Azure Function. If it's created and working, you should see it as selectable.
  Once you enable the endpoint, you'll need to work quickly through the next steps as you'll have a broken endpoint. There's not a way I know of to disable the endpoint and enable the certificates.
  ![image.png](/.attachments/image-127192eb-22fb-43e9-8ad1-3f7140889053.png)


## Add Certificate

### Certificate
- Go to your Azure Function, and click on the Settings -> Certificates blade
- Click Add Certificate, you should be able to add the Traffic Manager certificate:
  ![image.png](/.attachments/image-0f46c658-266c-4172-b03f-a5e8450218bc.png)

### Binding
- Go to your Azure Function, and click on the Settings -> Custom Domains blade
![image.png](/.attachments/image-e6ffa46e-cca7-4ac1-9754-837bdb7697f0.png)
- Click on Add Binding
![image.png](/.attachments/image-d16dcd65-0129-49a2-81e6-094a26ae1ef7.png)


# Congratulations, you're done!