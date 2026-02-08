# AdoStatsPy Functions
## Introduction
The Azure AdoStatsPy project is a collection of functions hosted on an Azure Function App that routinely triggers at scheduled intervals to extract valuable data related to ADO projects. These functions are designed to gather essential information from ADO, process it, and store the results in JSON format as blobs within a designated storage account container.

This page will provide an overview of each function and how they are configured to utilize Azure service bus, storage account containers, and timer triggers.

## **"function.json" Files**
To get a better understanding of how the functions work, it's important to take a look and understand each function's function.json configuration file.

For example, here's the config file for **TimerTriggerProjectStatus**:

![config_projectstatus.png](/.attachments/config_projectstatus-9f69d75d-a9f8-43d5-b664-480400735fd3.png)

As we can see in the first binding, the function is set up to receive as input and be triggered by "mytimer" on a cron schedule: "0 30 0 * * *", meaning the above function will trigger every day at 12:30 AM.

In the second binding we can see configurations for the output indicating to output the msg value to our Azure Service Bus topic "projectstatus".

If we take a look into one of the topictrigger function's config file, we can see an example of the differences in how the function is set up to be triggered by the service topic "projectname":

![config_wikistatus.png](/.attachments/config_wikistatus-c476a6d2-f816-4dac-8b61-39e9924549c7.png)

As we can see, the bindings are set up to trigger the function through the service bus topic, and then output a blob file to the timertriggerprincipal container. A similar configuration is found on the other two topictrigger functions function.json files.

In the case of the function.json for TimerTriggerPrincipal:

![config_principal.png](/.attachments/config_principal-4f262c1e-1f17-4775-8c13-5df895a1bef1.png)

We can see that the function is triggered by a timerTrigger on a cron schedule, and then executes and outputs to the blob file in the storage account.

## **Functions Overview**

1. **TimerTriggerProjectStatus**:
This function serves as a driver of the AdoStatsPy project. With each execution, it establishes a connection to ADO and retrieves a list of projects along with details like project name, ID, last change. However, instead of outputting the data to a blob in our storage account, the function sends the information as a message to a Service Bus topic. The Service Bus then triggers three additional functions: **TopicTriggerGitDataStatus**, **TopicTriggerWikiStatus**, and **TopicTriggerWorkItemStatus**.
2. **TopicTriggerGitDataStatus / TopicTriggerWikiStatus / TopicTriggerWorkItemStatus**:
These three functions are fairly similar in that they're all being triggered by the Service Bus topic. Once they're activated and receive project data from TimertriggerProjectStatus, they establish connections to ADO and retrieve additional data.
&nbsp;&nbsp;&nbsp;&nbsp; - **TopicTriggerGitDataStatus**: Obtains Git-related data for each project. Gathers details such as repositories, recent pull requests, commits, commit dates, and authors. Function then saves this information in two separate blob files: "projectgitdatastatus.json" and "failedrepositorystatus.json" (for repositories that encountered errors) within the "timertriggerprincipal" container.
&nbsp;&nbsp;&nbsp;&nbsp; - **TopicTriggerWikiStatus**: Retrieves information about wiki names, recent changes, and authors for each project. The data is then stored in JSON format and saved as a blob as "projectwikistatus.json" within the storage account container.
&nbsp;&nbsp;&nbsp;&nbsp; - **TopicTriggerWorkItemStatus**: Focuses on ADO project work items by compiling data on most recent work items, count of modified work items, and last project changes. This information is then also stored as "projectworkitemstatus.json" in the designated storage account container.

3. **TimerTriggerPrincipal**:
TimerTriggerPrincipal is a bit different from the other functions in that it's a standalone function and not a part of the Service Bus. With each execution, the function establishes a connection to ADO and retrieves details on all project administration groups and users associated with these groups for each project. The collected data is formatted into JSON and stored as a blob in the "TimerTriggerPrincipal" storage account container.