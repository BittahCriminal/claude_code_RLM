# Introduction
Prerequisites for this article should be to read the [Azure Monitor for Sandbox](/Team-Pages/SES/Service-Management/Services/Azure-Monitor-for-Sandbox) and [Azure Monitor for Sandbox   Agent](/Team-Pages/SES/Service-Management/Services/Azure-Monitor-for-Sandbox/Azure-Monitor-for-Sandbox-%2D-Agent) articles.

This describes how to create an alert in Azure Monitor for Sandbox. I will not be going over how to make alerts based on Metrics. However, these can be made by either the Wizard, or scanning the `Perf` table in the LAW, depending on if the Wizard gets you the alerts you want.


- **Shell Script or Binary** - You'll need to create and test a shell script or binary on a host. Ensure that the output meets the [Check Standard output](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/13966/Azure-Monitor-for-Sandbox?anchor=check-standard) or you will likely get weird results and performance.
## Add to Ansible - (Requires some knowledge of git and Ansible).
  - You'll need to make a new [branch in the gcr-ansible repo](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible/branches).
  - Add the binary itself to Ansible in the [roles/gcr-azmonsandbox/files/custom_checks directory].(https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible?path=%2Froles%2Fgcr-azmonsandbox%2Ffiles%2Fcustom_checks).
  - Ensure the check itself gets added to the host by adding it to the [checks.yml](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible?path=/roles/gcr-azmonsandbox/tasks/checks.yml).
  - You'll want to check out a host, and test the changes you made to your branch. It's fine to manually update the code on the host at `/opt/ansible/repo/gcr-ansible`. New changes will overwrite any you make.
  - Ensure that your alert is creating logs in `/var/log/azmonsandbox.log`
  - Once you're satisfied, [create a pull request](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible/pullrequests?_a=mine) and wait for approval and release.

## Create the Azure Monitor Alert
  - Currently, we have alerts is both the [Azure Arc Resource Group for Azure Monitor for Sandbox](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/overview), and the [regular resource group](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/overview). We have alerts in both locations, though it's possible to make alerts that query both LAWs if you want. These may get consolidated in the future.
  - To create the alert from scratch go to the [azmon-sandbox-law alerts blade](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/providers/Microsoft.OperationalInsights/workspaces/azmon-sandbox-law/alerts).
  - Click the "+ Create" button at the top, and click "Alert Rule"
  - Under Signal name select "Custom log search"
  - For the query, you'll want something like the below. Change AlertName to the check output your alert script makes.
  ```kusto
  Syslog
  | where Facility == "local7"
  | extend AlertName = extract(@"(\w+)", 1, SyslogMessage)
  | extend AlertStatus = extract(@"\w+ (\w+)", 1, SyslogMessage)
  | extend AlertText = extract(@"\w+ \w+ - (.*)", 1, SyslogMessage)
  | where AlertStatus == "CRITICAL" and AlertName == "CHECK_GPU"
  ```
  - **Measurement**

  | Name                    | Value      |
  | ----------------------- | ---------- |
  | Measure                 | Table Rows |
  | Aggregation type        | Count      |
  | Aggregation granularity | 45m        |

  - **Split by dimensions**
    - Resource ID column: \_ResourceId
  - **Alert logic**

  | Name                    | Value        |
  | ----------------------- | ------------ |
  | Threshold type          | Static       |
  | Operator                | Greater than |
  | Threshold value         | 0            |
  | Frequency of Evaluation | 30m          |

  - **Advanced options**
    - Number of violations to trigger the alert:

  | Name                      | Value      |
  | ------------------------- | ---------- |
  | Number of violations      | 1          |
  | Evaluation period         | 45m        |
  | Override query time range | None (45m) |
  - **Details**
    Severity: 0 - Critical
    Alert rule name: Azure Sandbox CHECK_GPU_AMD Critical

  - **Identity**
    Use the user assigned managed identity here. Ensure that this identity has Log Analytics Reader permission to the LAW its querying.

  - **Advanced Options**
    Enable upon creation ☑️
    Automatically resolve alerts ☑️ 

## Test
After this, you'll want to test the alert to ensure it performs the way you expect