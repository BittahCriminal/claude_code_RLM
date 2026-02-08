In this [page](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4738/AKS-Patching-service) we explained how to manually upgrade your AKS instances. Now we explain how to upgrade your AKS automatically with planned maintenance schedule.

for running all commands below you must first login to your AKS instances with PIM into the subs that you AKS reside as follow for example:

`az account set --subscription 0d83bec5-5c98-45a6-a26a-a754a03afcae`
`az aks get-credentials --resource-group AKS-VMss-patching-effort --name AKS-cluster-for-patching-test`


Now that you logged into you AKS you can Run below command will add auto upgrade to your existing cluster:

`az aks update --resource-group myResourceGroup --name myAKSCluster --auto-upgrade-channel stable`

If you are creating new AKS instances , you can run below command to enable auto upgrade during AKS provisioning:


`az aks create --resource-group myResourceGroup --name myAKSCluster --auto-upgrade-channel stable --generate-ssh-keys`

You can use one of these **Auto upgrade channel** for above parameter depend on your patching need.

![image.png](/.attachments/image-b19788df-b497-478e-99f2-2141bc2bbb92.png)

**Using Cluster Auto-Upgrade with Planned Maintenance**

Now that we set our AKS cluster to be upgraded automatically, we can schedule planned maintenance and the auto upgrade happens on your planned maintenance date.

Lets add the maintenance extension to your AKD cluster first:

`az extension add --name aks-preview`
`az extension update --name aks-preview`

Now that you have added the extension lets schedule the maintenance. below example will schedule maintenance on your AKS cluster on every Tuesday at 11 AM:

`az aks maintenanceconfiguration add -g MyResourceGroup --cluster-name myAKSCluster --name default --weekday Tuesday  --start-hour 11`

In real word it would be something this:

`az aks maintenanceconfiguration add -g AKS-VMss-patching-effort --cluster-name aks-auto-upgrade-testing --name default --weekday Tuesday  --start-hour 11`

You will then get the confirmation after you run the command successfully as follow: 

![image.png](/.attachments/image-06e2c700-996d-47bc-924f-f71aae4aad15.png)

This is it. you now have scheduled your AKS auto upgrade to happen every Tuesday at 11 AM.

**Below our some useful command for schedule maintenance:**

Update existing maintenance window:

`az aks maintenanceconfiguration update -g MyResourceGroup --cluster-name myAKSCluster --name default --weekday Monday  --start-hour 1`

List all the existing maintenance windows in AKS cluster:

`az aks maintenanceconfiguration list -g MyResourceGroup --cluster-name myAKSCluster`

![image.png](/.attachments/image-bff1db3d-27d5-4e6b-b7f1-7b84f79dc97b.png)

References:

https://docs.microsoft.com/en-us/azure/aks/planned-maintenance
https://docs.microsoft.com/en-us/cli/azure/aks/maintenanceconfiguration?view=azure-cli-latest
https://docs.microsoft.com/en-us/azure/aks/upgrade-cluster




