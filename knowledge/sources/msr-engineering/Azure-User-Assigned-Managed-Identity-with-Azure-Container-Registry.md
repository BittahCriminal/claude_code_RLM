# Azure User Assigned Managed Identity with Azure Container Registry

## Getting a cluster and it's members to connect to a user assigned MSI

### Create a user-assigned identity

These are best done per resource group. So if you have many VMs in an RG, you can make on UAI, assign the VMs to it, and then give that UAI permissions to the ACR.

```bash
az identity create --resource-group mycluster01 --name mycluster01MI
```

You'll want to get some of the Identity properties so we can assign to VMs and assign permissions to the Azure Container Registry

```bash
# Get resource ID of the user-assigned identity

userID=$(az identity show --resource-group myResourceGroup --name mycluster01MI --query id --output tsv)

# Get service principal ID of the user-assigned identity

spID=$(az identity show --resource-group myResourceGroup --name mycluster01MI --query principalId --output tsv)
```

### Assign VMs to the user assigned identity

For a single VM:

```bash
az vm identity assign --resource-group myResourceGroup --name myVM --identities $userID
```

For all VMs in an RG

```bash
for node in  $(az vm list -d -g myResourceGroup --query "[].{ name: name}" -o tsv);do
  echo "Assigning Identity: mycluster01MI to $node"
  az vm identity assign --resource-group myResourceGroup --name $node --identities $userID
done
```

The above operations are additive, and won't clobber existing identity memberships.

### Allow this identity to access the container repo

There is a [matrix of capabilities](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-roles) on the container repo. You'll want to be sure you select the right one(s). This works across subscriptions.

```bash
# Get the ID of the ACR
resourceID=$(az acr show --resource-group myResourceGroup --name myContainerRegistry --query id --output tsv)

# Assign permissions
az role assignment create --assignee $spID --scope $resourceID --role acrpush
```

## Using the identity to access the ACR

Here's basic stops for logging into the repo and pulling an image:

```bash
az login --identity
az acr login --name myContainerRegistry
docker pull mycontainerregistry.azurecr.io/helloworld:latest
```

Push and delete operations will work here too.

## References

[Use an Azure managed identity to authenticate to an Azure container registry](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity)

[What is managed identities for Azure resources](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)  

[Pull container images in Azure Container Registry (ACR) from Azure VM with managed service identity (MSI)](https://medium.com/@maninder.bindra/pull-container-images-in-azure-container-registry-acr-from-azure-vm-with-managed-service-identity-d490dab6eb5a)  

## Script to apply MSI to an RG

```bash
#!/usr/bin/env bash

if $(az account show 2>&1|grep -q "Please run");then
  echo "Please log into Azure with: az login"
  exit 1
fi

# User Assigned Identity Subscription
UAISUB="c82abd13-0681-4244-961a-4a5ddd45a54a"
# User Assigned Identity Resource Group
UAIRG="GCRGPUNC"
# User Assigned Identity Name
UAI="GCRGPU07MI"
# Azure Container Registry Subscription
ACRSUB="7ccdb8ae-4daf-4f0f-8019-e80665eb00d2"
# Azure Container Registry Resource Group
ACRRG="gcrcontainers"
# Azure Container Registry Name
ACR="gcrmembers"

az account set --subscription $ACRSUB
ACRID=$(az acr show --resource-group $ACRRG --name $ACR --query id --output tsv)

az account set --subscription $UAISUB

# Ensure UAI exists, if not create it
if [ -z "$(az identity list --resource-group $UAIRG --query "[].{ name: name}" -o tsv)" ];then
  echo "No identity found in RG: $UAIRG. Creating: $UAI"
  az identity create --resource-group $UAIRG --name $UAI
else
  UAI=$(az identity list --resource-group $UAIRG --query "[].{ name: name}" -o tsv)
fi
echo "Using UAI: $UAI"

userID=$(az identity show --resource-group $UAIRG --name $UAI --query id --output tsv)
spID=$(az identity show --resource-group $UAIRG --name $UAI --query principalId --output tsv)

# Assign roles to container registery
az role assignment create --assignee $spID --scope $ACRID --role acrpush
az role assignment create --assignee $spID --scope $ACRID --role acrdelete

# serial method
#for node in  $(az vm list -d -g $UAIRG --query "[].{ name: name}" -o tsv);do
#  echo "Assigning Identity: $UAI to $node"
#  az vm identity assign --resource-group $UAIRG --name $node --identities $userID
#done

# parallel method
az vm list -d -g $UAIRG --query "[].{ name: name}" -o tsv| parallel -j30 "az vm identity assign --resource-group $UAIRG --name {} --identities $userID"
```