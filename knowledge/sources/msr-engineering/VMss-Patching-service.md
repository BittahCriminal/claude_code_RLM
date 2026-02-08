This Wiki pages explains how to Update/Upgrade Azure VMss( virtual Machine Scale Set)

Lets first look at how the upgrade perform in VMss world.

1. Before beginning the upgrade process, the orchestrator will ensure that no more than 20% of instances in the entire scale set are unhealthy (for any reason).

2. The upgrade orchestrator identifies the batch of VM instances to upgrade, with any one batch having a maximum of 20% of the total instance count, subject to a minimum batch size of one virtual machine. There is no minimum scale set size requirement and scale sets with 5 or fewer instances will have 1 VM per upgrade batch (minimum batch size).

3. The OS disk of every VM in the selected upgrade batch is replaced with a new OS disk created from the latest image. All specified extensions and configurations in the scale set model are applied to the upgraded instance.

4. For scale sets with configured application health probes or Application Health extension, the upgrade waits up to 5 minutes for the instance to become healthy, before moving on to upgrade the next batch. If an instance does not recover its health in 5 minutes after an upgrade, then by default the previous OS disk for the instance is restored.

5. The upgrade orchestrator also tracks the percentage of instances that become unhealthy post an upgrade. The upgrade will stop if more than 20% of upgraded instances become unhealthy during the upgrade process.

6. The above process continues until all instances in the scale set have been upgraded.

Now that we understand how VMss upgrade works, let start with upgrading VMss instances manually and then automatically. 

# **Manually trigger OS image upgrades**


First make sure you PIM into your sub where your VMss reside and make sure to set your azure cli to your sub as follow for example:

`az account set --subscription 0d83bec5-5c98-45a6-a26a-a754a03afcae`


Use az vmss rolling-upgrade start to check the OS upgrade history for your scale set. Use Azure CLI 2.0.47 or above. The following example details how you can start a rolling OS upgrade on a scale set named myScaleSet in the resource group named myResourceGroup:

`az vmss rolling-upgrade start --resource-group "myResourceGroup" --name "myScaleSet" --subscription "subscriptionId"`

![image.png](/.attachments/image-ad7add62-1cc7-43fa-b3de-fcda07f77ea8.png)

Now lets see how we ca configure VMss to automatically upgrade OS image for us. 

# **Configure automatic OS image upgrade**

To configure automatic OS image upgrade, ensure that the automaticOSUpgradePolicy.enableAutomaticOSUpgrade property is set to true in the scale set model definition.

Use az vmss update to configure automatic OS image upgrades for your scale set. Use Azure CLI 2.0.47 or above. The following example configures automatic upgrades for the scale set named myScaleSet in the resource group named myResourceGroup:

`az vmss update --name myScaleSet --resource-group myResourceGroup --set UpgradePolicy.AutomaticOSUpgradePolicy.EnableAutomaticOSUpgrade=true`



