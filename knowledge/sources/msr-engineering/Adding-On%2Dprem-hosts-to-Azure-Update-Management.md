This article explains how to add onprem Linux and windows machine into GCR azure patch management.

## For Linux ubuntu 18.04

Run the following command to onboard your onprem host into GCR Azure patch management


`wget https://raw.githubusercontent.com/Microsoft/OMS-Agent-for-Linux/master/installer/scripts/onboard_agent.sh && sh onboard_agent.sh -w 383511da-50b6-4c5b-afef-8b2295dbc42b -s TGful6VxTvOrHPFliFvrWVTEZBh77ljwz+ldVLXClq+KWXlvcVFluiCxuNjOSIq0XKvOTsg0xBwrfSsmzkxnLw== -d opinsights.azure.com`

Once you run the above command wait for the installation to be completed, make sure at the end of the script shell bundle exiting with code 0, if any other code than 0 you must troubleshoot and find out what is preventing Linux agent to be installed.

![2222.PNG](/.attachments/2222-85cad253-6396-4717-b82e-a89d44c4dfd0.PNG)

Now give it 15 minutes for agent to become available in Azure patch management. navigate to [GCR-automation](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/gcr-automation/providers/Microsoft.Automation/automationAccounts/gcr-automation/overview) account and click on update management , filter the platform selection to look for non-Azure node list and verify the onprem host you onboarded is showing up in the Azure portal.

![3333.PNG](/.attachments/3333-2b0e6bc1-6233-4a31-a0c2-fbbae4eba098.PNG)


## For Linux ubuntu20.04

Since ubuntu20.04 comes with python3 by default, you must install python2 as well in order the to get the Linux agent.

`apt-get install -y python2`
`sudo update-alternatives --remove-all python`
`sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 1`

Once you completed the above steps, simply run below command to install the Linux agent patch management.

`wget https://raw.githubusercontent.com/Microsoft/OMS-Agent-for-Linux/master/installer/scripts/onboard_agent.sh && sh onboard_agent.sh -w 383511da-50b6-4c5b-afef-8b2295dbc42b -s TGful6VxTvOrHPFliFvrWVTEZBh77ljwz+ldVLXClq+KWXlvcVFluiCxuNjOSIq0XKvOTsg0xBwrfSsmzkxnLw== -d opinsights.azure.com`

## For Windows

<u>Automated method - Preferred</u>
Remote desktop to the target system, launch an elevated Powershell prompt and run the follow script:
`\\research\msrsupp\GCRPatching\MMAInstall.ps1`

Wait about 15-60 minutes and you should see the client status change to 'Ready' on the gcr-automation 'Update management' page.

<u>Manual method - For reference only</u>
In order to install Azure patch management agent to your onprem windows machine you need to download and install the agent and add the proper workspace ID and key.

From the Windows server that you have plan to onboard to GCR azure patch management login to Azure portal and navigate to [GCR-patching log analytical workspace](https://ms.portal.azure.com/#@72f988bf-86f1-41af-91ab-2d7cd011db47/resource/subscriptions/40641f8d-33f8-4948-b0ae-3df7e85e94e9/resourceGroups/GCR-patching/providers/Microsoft.OperationalInsights/workspaces/GCR-patching/agentsManagement) under settings click on Agent management and download the Agent to your machine. 

![111111.PNG](/.attachments/111111-165dec04-11ff-482c-ae0a-a5656353fc2f.PNG)

Follow the instruction to install the agent and when it asks for workspace ID and key provide the below details:

workspace ID : `383511da-50b6-4c5b-afef-8b2295dbc42b`
workspace Key: `TGful6VxTvOrHPFliFvrWVTEZBh77ljwz+ldVLXClq+KWXlvcVFluiCxuNjOSIq0XKvOTsg0xBwrfSsmzkxnLw==`


![4444.PNG](/.attachments/4444-57bd2cf4-013f-46eb-bd97-01cefa21f860.PNG)![555.PNG](/.attachments/555-53999f7a-66db-4594-8fba-987d3ae3c45d.PNG)

Once installation is done give it an hour and verify the agent is reporting to our GCR-patching patch management by navigating to GCR-automation account under update management, your server should be report the compliance status. 