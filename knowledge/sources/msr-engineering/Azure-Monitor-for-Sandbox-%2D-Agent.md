## Introduction
The Azure Monitor for Sandbox Agent is simply the Azure Monitor Agent, which gets installed by policy.

## Configuration

All agents are configured by their respective DCRs:
- [azmon-sandbox-dcr | Data sources](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox/providers/Microsoft.Insights/dataCollectionRules/azmon-sandbox-dcr/dataSources)
- [azmon-sandbox-arc-dcr | Data sources](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/84ed0d97-78a4-44d4-b12f-c977bf141102/resourceGroups/azmon-sandbox-arc/providers/Microsoft.Insights/dataCollectionRules/azmon-sandbox-arc-dcr/dataSources)

The DCRs are configured for the following:

**Linux Syslog**
| Log Type | Facility | Minimum Log Level | Notes | 
|-|-|-|-|
| Linux Syslog | LOG_AUTH | LOG_INFO | Used to view login attempts | 
| Linux Syslog | LOG_LOCAL7 | LOG_INFO | Used for alerting |
| Linux Syslog | LOG_LOCAL6 | LOG_INFO | Used for custom metrics |

**Performance Counters (Metrics)**
| Performance Counter | Sample Time (in seconds) | Notes |
|-|-|-|
| Processor(*)\% Processor Time | 300 | Used to detect if a host is "busy" |
| Logical Disc(*)\% Free Megabytes | 300 | Use to track disk usage over time |
| Logical Disc(*)\% Used Space | 300 | Use to track disk usage over time |
| Network(*)\Total Bytes | 300 | Used to detect if a host is "busy" |
| Network(*)\Total Bytes Received | 300 | Used to detect if a host is "busy" |
| Network(*)\Total Bytes Transmitted | 300 | Used to detect if a host is "busy" |
| System(*)\Uptime | 300 | Used to detect if a host is "busy" |
| System(*)\Load 1 | 300 | Used to detect if a host is "busy" |
| System(*)\Load 5 | 300 | Used to detect if a host is "busy" |
| System(*)\Load 15 | 300 | Used to detect if a host is "busy" |
| System(*)\Unique Users | 300 | Used to detect if a host is "busy" |

Reference: [Collect Windows and Linux performance data sources with the Log Analytics agent in Azure Monitor - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/data-sources-performance-counters)

## Agent Alert Flow
- Each host has a number of artifacts added to the host by Ansible. All the files mentioned below are Ansible generated.
- A crontab in `/etc/cron.d/azmonsandbox` that triggers a shell script in `/usr/local/bin/run_azmonsandbox_checks.sh` every 30 minutes.
- This shell script iterates over all files in `/etc/azmonsandbox/custom_checks/`. It has a random execution delay for each script of 0 to 15 minutes.
- When the check is executed, it sends the results to syslog (via the `logger` command), these get stored in `/var/log/azmonsandbox.log`. This is configured at /etc/rsyslog.d/60-azmonsandbox.conf.
- The AMA also gets configured by the DCR, and gets a configuration at `/etc/rsyslog.d/10-azuremonitoragent-omfwd.conf`. This forwards the logs passing through rsyslog to the appropriate LAW to the `Syslog` table.
- Configured alerts will scan the Syslog table according to a query. For example:
  ```kusto
  Syslog
  | where Facility == "local7"
  | extend AlertName = extract(@"(\w+)", 1, SyslogMessage)
  | extend AlertStatus = extract(@"\w+ (\w+)", 1, SyslogMessage)
  | extend AlertText = extract(@"\w+ \w+ - (.*)", 1, SyslogMessage)
  | where AlertStatus == "CRITICAL" and AlertName == "CHECK_GPU"
  ```
The above scans the syslog logs for any CHECK_GPU alerts with a CRITICAL status. All logs have the _ResourceId which is the Azure Resource ID, and will be viewable on the appropriate Azure object (except for Arc which doesn't seem to have this ability yet).
- Any triggered alerts end up in a subscription table reachable via Azure Resource Graph called `alertsmanagementresources`. This is queried with the Grafana dashboard, but also can be viewed with the [Monitor -Alerts](https://ms.portal.azure.com/#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/~/alertsV2) blade.
  - Triggered alerts have a non-configurable lifetime of 30 days.