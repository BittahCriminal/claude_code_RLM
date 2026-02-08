
# Introduction
This page attempts to put together the various considerations in making a Go (or golang) application in an Azure Container Instance. In many cases, this can be better than [Go with Azure Functions](/Team-Pages/SES/Toolbox/Tooling-Standards/Tool-%2D-Go-Azure-Functions).

## Vs Azure Functions
Using Azure Container Instances instead of Azure Functions can be attractive for the following reasons, especially when you're using it to perform scheduled tasks:
- **Costs are lower** - Azure Functions need to be on all the time and have itself on standby, you also need to spin up an App Service Plan which can be costly. With the ACI, the container will run and then automatically terminate when the script is finished. There are no costs for having a stopped ACI, which also given an advantage over Virtual Machines. For a 4 ACI deployment, we have a run rate of $0.20/day compared to an equivalent Azure Function which is $5.00/day.
- **Easier to deploy** - The paradigm I use with this container setup is to have the binary live on an Azure Files section, and have the ACI configuration mount that Azure Files repository. You can then pass the command to the container to run the binary within. 
- **Easier to debug** - Azure Container Instances have a log tab that shows all output to stdout. You can also route all the logs to a Log Analytics Workstation to query logs across a number of containers. It's also possible to run a container with a shell, and connect to the shell from the portal to troubleshoot the container interactively. With Azure Functions, you must configure the binary as a web service, and to troubleshoot it, you need to install and run the [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?tabs=v2). To run various modes of the Function on-demand from Azure, you need to connect to it from Visual Studio Code, or know the proper incantation from the command line. You're also required to construct your logs a special way that they are emitted in a JSON format after the run, otherwise you'll get no logging at all. 
- **Fewer Constraints** - The Azure Function limits runs to 10 minutes on their cheaper Application Service Plans, though longer runs can be prohibitively expensive with the higher plans.

# Applications
The following services are using this method:
[autodeploy](/Team-Pages/SES/Service-Management/Services/autodeploy)
[user/group sync](/Team-Pages/SES/Service-Management/Services/Linux-user+group-service-\(usergroupfiles\))

# Outline/Components
- **Azure Storage Account** - This will host the binary (or other artifacts) you'll be using from the container. Best to push things here from a respitory and pipeline.
- **Azure Devops Repository** - You'll want a repository where you'll store the codebase, and also define a pipeline for building it.
- **Azure Devops Pipeline** - The pipeline will be responsible for building the binary, and deploying this to an Azure Files instance.
- **Azure Bicep file and execution script** - These are responsible for deploying the Azure Container Instance. You can find samples in the code bases for the applications above. If you run a bicep file deploying an ACI over an existing one, it will overwrite it.
- **Azure Container Instance** - You'll be best off if you can use an Azure Linux distroless container to run your code. This will reduce the container overhead, and ideally, you won't have to create a custom container which means you won't have to manage container versioning or host your own Azure Container Repository.
- **[User Assigned Managed Identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities?pivots=identity-mi-methods-azp)** - You'll need one of these so that your container or containers can all have a common permission used to access Azure Files, and any other artifacts needed to run your binary. You may consider using this one, or a different one to be used by your Logic Apps which are used to trigger the containers.
- **Log Analytics Workstation** (optional) - Used to send all logs from your container. Good for having a central place for debugging.
- **Azure Logic App** - Used to trigger the containers if you're using the cron/scheduled task method. To do so:
  - Enable a system assigned or user assigned principal. You can also use an SP if you want another thing to manage
  - In the Logic App Designer, use the Recurrence Trigger, and set the interval to what you want
  - Add the Azure Resource Manager action, and use Invoke resource operation
  - Sample:
    ```
    Subscription: Sesame GCR
    Resource Group: autodeployment
    Resource Provider: Microsoft.ContainerInstance
    Short Resource ID: containerGroups/autodeployment
    Client API Version: 2022-09-01
    Action Name: start
- **Azure Alerts** (optional) - You can alerts from the logic app, and have them tell me if the Logic App failed to deploy the container.

# Troubleshooting with ACI
If you are using a container that you can log in to, either using the `base` Azure Linux type, or the `debug` type for Azure Linux Distroless, you can click on the container object, then click on the `Containers` blade, and click on the "connect" tab to have an interactive shell session inside the container.

You can view logs for a single ACI from the portal by clicking on the container object such as [this one](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/groupsyncdirpgsql-container-instance/providers/Microsoft.ContainerInstance/containerGroups/groupsyncdirpgsql-groupsync/containers), clicking on the "Containers" blade, and then clicking on the Logs tab.

Logs for all the containers are sent to the LAW you configure for them. You can use this in scenarios, such as finding a username if you have a syncing process working. A query like the below can search for a username in the log text:
```kusto
ContainerInstanceLog_CL
| where Message contains "krisz"
```
These logs will be configured to store data at the Log Analytics Workspace default of 30 days. The Custom Log container is created automatically when executing the bicep with this relevant section:
```yaml
    diagnostics: {
      logAnalytics: {
        workspaceId: LAW_WORKSPACE_ID
        workspaceKey: LAW_PRIMARY_KEY
      }
```