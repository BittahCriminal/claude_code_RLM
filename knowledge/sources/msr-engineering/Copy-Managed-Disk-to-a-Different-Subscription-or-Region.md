# Purpose
This shows how to take a managed disk, and clone it, and copy it to a different subscription/location.

# Create a Snapshot

Source: https://docs.microsoft.com/en-us/cli/azure/snapshot?view=azure-cli-latest
```bash
az snapshot create -g MyResourceGroup -n MySnapshot2 --source MyDisk
```

# Copy this snapshot to a different subscription
*This only works if you're copying to the same region, otherwise you'll need to copy to a storage account*

See ALTERNATIVE below

Source: https://docs.microsoft.com/en-us/azure/virtual-machines/scripts/virtual-machines-linux-cli-sample-copy-snapshot-to-same-or-different-subscription

```bash
#Provide the subscription Id of the subscription where snapshot exists
sourceSubscriptionId=dd80b94e-0463-4a65-8d04-c94f403879dc

#Provide the name of your resource group where snapshot exists
sourceResourceGroupName=mySourceResourceGroupName

#Provide the name of the snapshot
snapshotName=mySnapshotName

#Set the context to the subscription Id where snapshot exists
az account set --subscription $sourceSubscriptionId

#Get the snapshot Id
snapshotId=$(az snapshot show --name $snapshotName --resource-group $sourceResourceGroupName --query [id] -o tsv)

#If snapshotId is blank then it means that snapshot does not exist.
echo 'source snapshot Id is: ' $snapshotId

#Provide the subscription Id of the subscription where snapshot will be copied to
#If snapshot is copied to the same subscription then you can skip this step
targetSubscriptionId=6492b1f7-f219-446b-b509-314e17e1efb0

#Name of the resource group where snapshot will be copied to
targetResourceGroupName=mytargetResourceGroupName

#Set the context to the subscription Id where snapshot will be copied to
#If snapshot is copied to the same subscription then you can skip this step
az account set --subscription $targetSubscriptionId

#Copy snapshot to different subscription using the snapshot Id
az snapshot create --resource-group $targetResourceGroupName --name $snapshotName --source $snapshotId
```

# Create a disk from snapshot
Source: https://docs.microsoft.com/en-us/azure/virtual-machines/scripts/virtual-machines-linux-cli-sample-create-managed-disk-from-snapshot

```bash
#Provide the subscription Id of the subscription where you want to create Managed Disks
subscriptionId=dd80b94e-0463-4a65-8d04-c94f403879dc

#Provide the name of your resource group
resourceGroupName=myResourceGroupName

#Provide the name of the snapshot that will be used to create Managed Disks
snapshotName=mySnapshotName

#Provide the name of the new Managed Disks that will be create
diskName=myDiskName

#Provide the size of the disks in GB. It should be greater than the VHD file size.
diskSize=128

#Provide the storage type for Managed Disk. Premium_LRS or Standard_LRS.
storageType=Premium_LRS

#Set the context to the subscription Id where Managed Disk will be created
az account set --subscription $subscriptionId

#Get the snapshot Id
snapshotId=$(az snapshot show --name $snapshotName --resource-group $resourceGroupName --query [id] -o tsv)

#Create a new Managed Disks using the snapshot Id
#Note that managed disk will be created in the same location as the snapshot
az disk create --resource-group $resourceGroupName --name $diskName --sku $storageType --size-gb $diskSize --source $snapshotId
```

# ALTERNATIVE: Copy this snapshot to a different subscription, then create a disk from the VHD
Source: https://docs.microsoft.com/en-us/azure/virtual-machines/scripts/virtual-machines-linux-cli-sample-copy-snapshot-to-storage-account

```bash
sas=$(az snapshot grant-access --resource-group $resourceGroupName --name $snapshotName --duration-in-seconds $sasExpiryDuration --query [accessSas] -o tsv)

az storage blob copy start --destination-blob $destinationVHDFileName --destination-container $storageContainerName --account-name $storageAccountName --account-key $storageAccountKey --source-uri $sas

# Check the status of the blob (see the "copy" section of json):
az storage blob show --name $destinationVHDFileName --container-name $storageContainerName --account-name $storageAccountName --account-key $storageAccountKey

# Then create a disk from the VHD Snapshot:
# https://docs.microsoft.com/en-us/azure/virtual-machines/scripts/virtual-machines-linux-cli-sample-create-managed-disk-from-vhd

# Ensure that resource group is already created
resourceGroupName=myResourceGroupName

# Provide the name of the Managed Disk
diskName=myDiskName

# Provide the size of the disks in GB. It should be greater than the VHD file size.
diskSize=128

#Provide the storage type for Managed Disk. Premium_LRS or Standard_LRS.
storageType=Premium_LRS

#Provide the URI of the VHD file that will be used to create Managed Disk.
# VHD file can be deleted as soon as Managed Disk is created.
vhdUri=https://contosostorageaccount1.blob.core.windows.net/vhds/contosoumd78620170425131836.vhd

#Create the Managed disk from the VHD file
az disk create --resource-group $resourceGroupName --name $diskName --sku $storageType --location $location --size-gb $diskSize --source $vhdUri
```