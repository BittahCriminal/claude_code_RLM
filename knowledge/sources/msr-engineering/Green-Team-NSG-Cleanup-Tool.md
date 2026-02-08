# Introduction

The cleanup tool is a security tool meant to reduce attack vectors on Internet facing subscriptions. ExpressRoute subscriptions don't apply to this article.

The cleanup tool's front end is a Windows only GUI application that can be downloaded via the [cleanuptool main page](http://aka.ms/cleanuptool).

# Purpose

Most of the details can be found in the [Cleanup Tool](http://aka.ms/cleanuptool) page. At a high level. The cleanup tool is meant to go though Azure subscriptions, and enforce removal "non-compliant" objects. These include:

* Service Principal Credentials
* Exposed management ports (endpoints) on an NSG (NSG Managment)
  * This includes a fixed list of: RDP, WinRM, SSH, SQL, SMB, Telnet and WMI
* Management Certificates
* Co-Administrators and Service Administrators (via IAM)

# Applications

One of the main applications of the tool is to bring compliance in line on the [rdpcleanup dashboard](https://rdpcleanup.azurewebsites.net/?purpose=Prod%2CNonProd&date=&id=&serviceTree=DivisionOid). This is generated via a scanner that resides in Azure, so if you fully allow an Azure Region access as per [this list](https://www.microsoft.com/en-us/download/details.aspx?id=41653), you'll likely include the scan tool as well. Note that the scorecard in the rdpcleanup tool is the same as what the Azure Cleanuptool can restrict.

# NSG Cleanup Tool Functionality

This is just one aspect of the cleanup tool, however it's probably one of the most used.

## Pre Deployment

You'll need to enable the Microsoft.Web Resource on your Subscription for the deployment to work, otherwise it'll fail after multiple retries. Go to your Subscription pane and click "Resource Providers". Search for Microsoft.Web, and click the Register button. It's possible that the Cleanup Tool does this for you.
This can also be done [with the CLI](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-supported-services#azure-cli):

```bash
az provider register --namespace Microsoft.Web
```

![image.png](/.attachments/image-34cd9a2b-ade5-4a9f-9df1-8474957ce4a1.png)

## Deployment/Service Details

In the Subscription Cleanup Tool under the "Restrict Arm Resources" tab you can "select the Management Network to restrict access to". Your choices are Corpnet + SAW or just SAW. You can also add a custom IP Range. Select your options, and your Subscription and click the "Deploy Cleanup Service" Button. See Below for the interface:
![image.png](/.attachments/image-709daf7b-34cb-411c-a053-029d6d21e9d0.png)

This will create a `cleanupservice` RG with an Azure App Service Plan and App Service inside. The App Service appears to be a continuously running .NET windows service.

## Rule Management

Custom rules get stored in multiple NSGs inside the `cleanupservice` RG. A different NSG is made per Azure Region. The nomenclature is `rg-cleanupservice-nsg` with subsequent NSGs being named sequentially `rg-cleanupservice-nsg1`, etc.

Rules in each of the NSGs are named Cleanuptool-Allow-100, Cleanuptool-Allow-101 with the ports of fixed list of management endpoints included. There doesn't seem to be a way to add custom ports, and ports outside of the fixed list of management endpoints are ignored.

## Rule Gaps

While there are ways to fill the Cleanup Tool with custom rules. There are gaps out of the box with the rules they supply. Namely  the Azure ER SNAT addresses are not included in their list.

# References

* http://aka.ms/cleanuptool
* https://mgmtcerts.azurewebsites.net/certremovaltool (same as above)
* [Cleanuptool Dashboard](https://rdpcleanup.azurewebsites.net/?purpose=Prod%2CNonProd&date=&id=&serviceTree=DivisionOid)
* [Cleanup Tool Onenote](https://microsoft.sharepoint.com/teams/mgmtports2/_layouts/OneNote.aspx?id=%2Fteams%2Fmgmtports2%2FShared%20Documents%2FGuidance&wd=target%28Mgmt%20Ports.one%7C376405A4-1ADE-4B39-9553-826E2C062989%2FTransform%20ARM%20Templates%7CC95DC806-7D20-4033-8206-7392159C5387%2F%29)
