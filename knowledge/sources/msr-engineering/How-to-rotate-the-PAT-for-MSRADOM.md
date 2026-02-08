# Update 3/5/2024
- Securing engineering forum has discussed [PAT Burndown Guidance](https://eng.ms/docs/cloud-ai-platform/devdiv/one-engineering-system-1es/1es-docs/1es-security-configuration/configuration-guides/pat-burndown-guidance) with the goal of limiting PAT lifespans to 7 days in CY2024.

- We should investigate migrating MSRADOM away from PATS and using a managed identity associated with the Azure function app associated to them.
   - [ADO supports managed identities now](https://learn.microsoft.com/en-us/azure/devops/integrate/get-started/authentication/service-principal-managed-identity) - this wasn't a thing when these reports were created years ago.
   - We can likely use the [system assigned managed identity associated with ADOStatysPy](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/adostats/providers/Microsoft.Web/sites/AdoStatsPy/msi)
      - ObjectID: `33ccb589-eac2-42d3-a808-48f3a5a0b9ef`

   - We'll need to update any functions that rely on MSRADOM to authenticate with a managed identity (instead of the service account + PAT)
   - We'll need to ensure the Managed Identity has the right permissions to MSResearch ADO scopes. [Scopes for the MSRADOM PAT](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/8623/How-to-rotate-the-PAT-for-MSRADOM?_a=edit&anchor=ado-scopes-for-pat) uses as a reference.

- [Snapshot from 3/5/2024 on active PATs in T+R (MSRADOM)](https://microsoft-my.sharepoint.com/:x:/p/jerick/EecS8P9MwRVPtvKva_XNcPwBwK_boW-NUdjrWgIfa4q0fw?e=QaWhlY&wdOrigin=TEAMS-MAGLEV.p2p_ns.rwc&wdExp=TEAMS-TREATMENT&wdhostclicktime=1709665403170&web=1)

> kvnscott	1	["[jordand,trevor,jordan,v-ahuetson,krisz]->MSRADOM"]


# Copilot guidance

You can authenticate to Azure DevOps using Managed Identities. 

Here's how you can modify your Python code to use Managed Identities for authentication:

* First, you need to obtain an access token for the Managed Identity. 
This can be done by making a request to the Azure Instance Metadata Service. 

Here's a function that does this:

```python
import requests

def get_managed_identity_token(resource):
    identity_endpoint = "http://169.254.169.254/metadata/identity/oauth2/token"
    headers = {"Metadata": "true"}
    params = {"api-version": "2018-02-01", "resource": resource}
    response = requests.get(identity_endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["access_token"]
```

You can then use this token to authenticate to Azure DevOps:

```python
from azure.devops.connection import Connection
from msrest.authentication import BasicTokenAuthentication

# Get the access token for the Managed Identity
access_token = get_managed_identity_token("499b84ac-1321-427f-aa17-267ca6975798")

# Use the access token to create a BasicTokenAuthentication object
credentials = BasicTokenAuthentication({"access_token": access_token})

# Use the BasicTokenAuthentication object to create a Connection
connection = Connection(base_url=organization_url, creds=credentials)
```

Please replace `organization_url` with the URL of your Azure DevOps organization.

This code uses the `requests` package to make HTTP requests. 
You'll need to install this package using pip:

```bash
pip install requests
```

Please note that the Managed Identity must have the necessary permissions to access the Azure DevOps organization. 

This can be configured in the Azure DevOps portal.

---

In case we need to rotate the PAT again the below runs through how to do that.

[[_TOC_]]

To rotate a PAT for a service account thats part of the corporate domain (e.g. REDMOND\MSRADOM), you should use the VSTS PAT Generator tool. 

The below guidance will walk you through the requirements and steps to rotate a PAT on the MSRADOM service account.

The PAT expiration window has been lowered. 
You can only generate a PAT that is valid for 6 months

## Pre-requisites
1. Create and login to a Microsoft Devbox (https://aka.ms/TnR/Devbox) and connect to `Azure VPN`.
   
2.  Run the VSTSPatGenerator
     - Download the VSTS PAT Generator: https://aka.ms/vstspatgendownload
     - Extract the zip into a folder 
     - Open `Terminal` and change directory to the folder VSTSPatGen folder you extracted, and run `VSTSPatGenerator.exe` 

       ```powershell
       #Change directory to the folder you extracted the zip

       cd c:\temp\vstspatgen

       # run VSTSPatGenerator.exe and follow the prompts

       .\VSTSPatGenerator.exe
       ```

3. Access to 
[MSRADOM Key Vault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://adostats.vault.azure.net/secrets/MSRADOM-Svc-Account)


## VSTS PAT Generator Instructions



This assumes you have connected to a Devbox and extracted the zip.


1.  Open `powershell` and:
```powershell
#Change into the directory where the .\VstsPatGenerator.exe is copied
cd c:\temp\vstspatgen #example path if you extracted it to a temp folder

#Run the pat generator and follow the prompts
.\VstsPatGenerator.exe
```


---
> Note: Copy the below scopes when generating the PAT

`vso.agentpools,vso.analytics,vso.build,vso.code,vso.gallery,vso.graph,vso.packaging,vso.memberentitlementmanagement,vso.project,vso.release,vso.wiki,vso.work`


----

2. Once the PAT is generated, update the `ADO-PAT` secret with the new PAT in the [ADOStats Keyvault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7bdcf9ec-4326-408b-a69b-c7235c63b5e8/resourceGroups/ADOStats/providers/Microsoft.KeyVault/vaults/ADOStats/secrets). 
   - The function apps reference that secret name specifically.


## Example of how to generate a new PAT for MSRADOM

![image.png](/.attachments/image-e71e5b43-2d9b-47b2-a2df-e5878c45ecfa.png)



## ADO Scopes for PAT
The below scopes are required for ADOStatsPy reporting functionality.
This basically equates to read-only access to most of Azure DevOps.
* vso.agentpools
* vso.analytics
* vso.build
* vso.code
* vso.gallery
* vso.graph
* vso.packaging
* vso.project
* vso.release
* vso.wiki
* vso.work
* vso.memberentitlementmanagement

## References used
For official guidance on the tool: https://aka.ms/VSTSPATGEN