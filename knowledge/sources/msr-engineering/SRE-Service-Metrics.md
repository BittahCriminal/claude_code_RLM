[[_TOC_]]

# Ansible
[Ansible Grafana Dashboard](https://sesameservices-fqf5dvcag4fdftcq.wus2.grafana.azure.com/d/M_jcRvl4k/ansible-service-metric?orgId=1&refresh=1m)
[Metrics Log Analytics Workstation](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/service_metrics/providers/Microsoft.OperationalInsights/workspaces/servicemetrics-law/Tables) (Ansible_CL table)
## Health
- Ratio of errors to successful runs - Available in the "Successful to Failed runs over the last 30 days" [panel](https://sesameservices-fqf5dvcag4fdftcq.wus2.grafana.azure.com/d/M_jcRvl4k/ansible-service-metric?orgId=1&refresh=1m)
- Hosts Reimaged - Available in the "Total number of hosts reimaged in the past 30 days" [panel](https://sesameservices-fqf5dvcag4fdftcq.wus2.grafana.azure.com/d/M_jcRvl4k/ansible-service-metric?orgId=1&refresh=1m)
- Unique hosts using Ansible - Available in the "Total number of hosts using ansible in the last 30 days" [panel](https://sesameservices-fqf5dvcag4fdftcq.wus2.grafana.azure.com/d/M_jcRvl4k/ansible-service-metric?orgId=1&refresh=1m)
- Cluster names and sandbox names - Available in the "List of ansible hosts from the last 30 days" [panel](https://sesameservices-fqf5dvcag4fdftcq.wus2.grafana.azure.com/d/M_jcRvl4k/ansible-service-metric?orgId=1&refresh=1m)
  - To download this data, for sort and manipulation from Grafana:
    - Click the kebab menu
    - Click "Inspect"
    - Click "Data"
    - Click "Download CSV"
  - This data can also be downloaded from the [Log Analytics Workstation](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/resourceGroups/service_metrics/providers/Microsoft.OperationalInsights/workspaces/servicemetrics-law/logs), using the query:
    ```kusto
    ansible_CL
    | where TimeGenerated >= ago(30d)
    | distinct Hostname
    ```
    - Run the query, and then click "Export" on the top to export to your data type of choice
- Commits to the gcr-ansible repo a month Link to [GCR-Ansible Repo](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible)
  - Clone/Pull the gcr-ansible repository
  - The following git commmand can give you a list of PRs over the last month:
  ```bash
  git log --since="last month" --pretty=format:'%h,%an,%ar,%s'
  # For a count of the above
  git log --since="last month" --pretty=format:'%h,%an,%ar,%s'|wc -l
  ```

# GPUMetrics service Metrics
GPUMetrics service metrics are being emitted weekly to the [TnR QBR Metrics Sharepoint List](https://microsoft.sharepoint.com/teams/TnREng7/Lists/QBR%20Metrics/AllItems.aspx).

For manual service, or more insights, metrics can be generated with the scripts in the [ses_service_metrics repo](https://dev.azure.com/msresearch/MSR%20Engineering/_git/ses_service_metrics?path=/gpumetrics).

Output is similar to the below:

**`gpumetrics_hosts.sh`**
```
Total number of hosts in GCR Scope: 1131
Total number of hosts installed in GCR Scope: 1117
Total number of hosts missing in GCR Scope: 14
Percentage of hosts installed in GCR Scope: 98.00

Total number of hosts in Non-GCR Scope: 139
Total number of hosts installed in Non-GCR Scope: 82
Total number of hosts missing in Non-GCR Scope: 57
Percentage of hosts installed in Non-GCR Scope: 58.00

Total number of hosts: 1270
Total number of hosts installed: 1199
Total number of hosts missing: 71
Percentage of hosts installed: 94.00
```

**`gpumetrics_badhosts.sh`**
```
Hosts deallocated: 445
Hosts running Windows: 38
Hosts running Unknown OS: 34
Hosts running EOL Ubuntu: 93
```


# SSH Keyvault Service
[SSH Keyvault Service Dashboard](https://sesameservices-fqf5dvcag4fdftcq.wus2.grafana.azure.com/d/5EgLH1l4z/ssh-keyvault-service-metric?orgId=1)
- Running genmgmtchain to convert a list of aliases to a management report.
  - Check out the repo [genmgmtchain](https://dev.azure.com/msresearch/MSR%20Engineering/_git/genmgmtchain)
  - Follow the instructions in the READMEk