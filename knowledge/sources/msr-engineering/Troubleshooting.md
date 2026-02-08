##  Update agent readiness is Not configured.

One of the issues you may encounter is when update agent readiness is not configured. You need to make sure update agent readiness is always set to ready status otherwise, patch deployment will fail on the machine. 

For windows:

![32.PNG](/.attachments/32-f719e012-64e3-455f-a127-1cdd08395e4a.PNG)

If you see update agent is not configured do the followings

- RDP into the host which has this issue and navigate to C:\Program Files\Microsoft Monitoring Agent\Agent
- click on Agent control panel and navigate to Azure log analytical. 
- make sure the only workspace which is linked there is `383511da-50b6-4c5b-afef-8b2295dbc42b` if you see any other workspace listed there then click on edit and delete those, click apply and make sure the extra workspace ID get deleted.
![423.PNG](/.attachments/423-a341516d-7f56-4112-8a28-b4074d3873dc.PNG)
- Above can be done via PowerShell by running the follow command: replace the workspace ID with any workspace listed in azure log analytical which you would like to delete:

`$workspaceId = "9b0284d5-010e-46c0-9447-f80b32f5d0e3"; $mma = New-Object -ComObject 'AgentConfigManager.MgmtSvcCfg'; $mma.RemoveCloudWorkspace($workspaceId); $mma.ReloadConfiguration()`

- visit [troubleshooting windows update agents issues](https://docs.microsoft.com/en-us/azure/automation/troubleshoot/update-agent-issues) for more troubleshooting steps if above didn't fix the problem.

 For Linux

- SSH into the node which has the update agent readiness problem and run the following command to restart the azure agent monitoring service

`sudo /opt/microsoft/omsagent/bin/service_control restart`

- if above doesn't fix the issue, visit [troubleshooting Linux update agent issues](https://docs.microsoft.com/en-us/azure/automation/troubleshoot/update-agent-issues-linux) for more troubleshooting steps 


## Log Analytics agent for Linux isn't running


If the agent isn't running, it prevents the Linux Hybrid Runbook Worker from communicating with Azure Automation. The agent might not be running for various reasons.

Verify the agent is running by entering the command `ps -ef | grep python`. You should see output similar to the following. The Python processes with the nxautomation user account. If the Azure Automation feature isn't enabled, none of the following processes are running.


`nxautom+   8567      1  0 14:45 ?        00:00:00 python /opt/microsoft/omsconfig/modules/nxOMSAutomationWorker/DSCResources/MSFT_nxOMSAutomationWorkerResource/automationworker/worker/main.py`

If the agent isn't running, run the following command to start the service: `sudo /opt/microsoft/omsagent/bin/service_control restart`.

If restarting agent doesn't help , try to purge the existing OMS agent and reinstall the agent with following command:

First lets purge:

` 
curl -s https://raw.githubusercontent.com/microsoft/OMS-Agent-for-Linux/master/tools/purge_omsagent.sh|sh`

Now lets re-onboard the Agent:

`wget https://raw.githubusercontent.com/Microsoft/OMS-Agent-for-Linux/master/installer/scripts/onboard_agent.sh && sh onboard_agent.sh -w 383511da-50b6-4c5b-afef-8b2295dbc42b -s TGful6VxTvOrHPFliFvrWVTEZBh77ljwz+ldVLXClq+KWXlvcVFluiCxuNjOSIq0XKvOTsg0xBwrfSsmzkxnLw== -d opinsights.azure.com`

On some nodes installing the agent on Linux DSVM ( GCRAZGDL) may fail on SCX installation as follow

![image.png](/.attachments/image-db4b267d-d4e4-4899-9043-55b0492cb816.png)

This is because there is a bug in Azure DSVM image where it cannot installs conda and SCX packages at the same time. The issue is currently open and azure investigating. workaround would be to run the following command and then run the onboard command.

`echo 'conda activate py37_default &'>/etc/profile.d/conda_env.sh`

Below command comes handy when troubleshooting why Linux agent isn't running.

`tail /var/opt/microsoft/omsagent/383511da-50b6-4c5b-afef-8b2295dbc42b/log/omsagent.log`

If the agent is healthy and running you should see something like this otherwise tail command will give you more information about the failure.

![image.png](/.attachments/image-26dced62-0f75-4ed7-987c-50bcf5ab6411.png)

Check the status of Azure patch management on the client node : 

`sudo /opt/microsoft/omsagent/bin/omsadmin.sh -l` if you see the primary workspace is something different that our workspace or the status is not onboarded it might be the issue.

`root@GCRSANDBOX106:~# sudo /opt/microsoft/omsagent/bin/omsadmin.sh -l
Primary Workspace: 383511da-50b6-4c5b-afef-8b2295dbc42b    Status: Onboarded(OMS                                                                                          Agent Running)
`