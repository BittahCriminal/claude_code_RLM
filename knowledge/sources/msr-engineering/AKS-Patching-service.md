This Wiki page explains how to Update/Upgrade Azure AKS( Azure Kubernetes Service) manually using Azure cli. We have another article that explains [how to upgrade your AKS automatically with planned maintenance schedule](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/4752/AKS-patching-auto-upgrade).


**Upgrade an Azure Kubernetes Service (AKS) cluster**

Part of the AKS cluster lifecycle involves performing periodic upgrades to the latest Kubernetes version. It is important you apply the latest security releases, or upgrade to get the latest features. This article shows you how to upgrade the master components or a single, default node pool in an AKS cluster.

**Check for available AKS cluster upgrades**

The preferred method to run upgrade AKS cluster commands is to use cloud shell. In this article we assume our AKS cluster name is "AKS-cluster-for-patching-test" you must change details to your AKS name and resource group.

- PIM into the Subscription that you AKS service is located. 
- Open Cloudshell, this usually locates on top right side of Azure portal
![image.png](/.attachments/image-16436fdc-7827-4cf0-92fe-fe5a63ee7835.png)
- login to your AKS instance by running following command.

```bash
az account set --subscription 0d83bec5-5c98-45a6-a26a-a754a03afcae
az aks get-credentials --resource-group AKS-VMss-patching-effort --name myAKSCluster
```
![image.png](/.attachments/image-814863c6-feac-4736-aa44-e9ce0c50a79f.png)

- To check which Kubernetes releases are available for your cluster, use the az aks get-upgrades command.

```bash
az aks get-upgrades --resource-group myResourceGroup --name myAKSCluster --output table
```


![image.png](/.attachments/image-fe6c32dd-077a-42d9-9730-f92fd9cf235f.png)

If no upgrade is available, you will get the message:

`ERROR: Table output unavailable. Use the --query option to specify an appropriate query. Use --debug for more info.`

**Upgrade an AKS cluster**

**Note before you start upgrading:** When you upgrade a supported AKS cluster, Kubernetes minor versions **cannot be skipped**. All upgrades must be performed sequentially by major version number. **For example, upgrade between 1.14.x -> 1.15.x or 1.15.x -> 1.16.x are allowed, however 1.14.x -> 1.16.x is not allowed.**

Now that you get the latest upgradable version do the following to upgrade your AKS to the latest version.

```bash
az aks upgrade 
    --resource-group myResourceGroup 
    --name myAKSCluster 
    --kubernetes-version LATEST_KUBERNETES_VERSION_YOU_FOUND_ABOVE
```

something like this:

```bash
az aks upgrade --resource-group AKS-VMss-patching-effort --name AKS-cluster-for-patching-test --kubernetes-version 1.22.2
```

![image.png](/.attachments/image-aac519c3-c464-4de1-b295-035d58192011.png)

That is it. your AKS clusters with all the node pools have been upgraded to latest available version. To make sure your patching process were successfully completed, check for available AKS cluster upgrade command again. If you get the below Error message, it means you are up to date and there is no available upgrade at this time.

![image.png](/.attachments/image-0a512a30-4b6f-4aa8-8a62-4b67033b938b.png)

# Reference
https://docs.microsoft.com/en-us/azure/aks/upgrade-cluster