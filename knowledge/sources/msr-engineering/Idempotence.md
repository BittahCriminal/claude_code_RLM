# Background - What is Idempotence and why is it important?

Idempotence "is the property of certain operations in mathematics and computer science whereby they can be applied multiple times without changing the result beyond the initial application."  It is frequently a desirable quality in scripts and applications which will make them more robust in an operational environment.

Writing scripts to be idempotent is particularly useful when interacting with remote services such as Azure, where the service may have latency, fail, or unpredictable timing of events in the remote service.  When provisioning complex deployments in azure, some resources will have dependencies which must exist before they can be created.  If a script or deployment fails halfway through the process, an idempotent script will be able to be restarted and pick up where it left off, creating only the new assets that are missing.  Another way of thinking of idempotence is that an idempotent script will seek a "desired state", given certain parameters.

You'll see in the examples below that writing idempotent scripts successfully requires breaking down the problem at hand and carefully analyzing the relationship between data and state.  Carefully selecting the order of operations can have a significant impact on the readability and maintainability of your code as well as reducing the number of branches and duplication.

# Examples

## Checking if a resource exists, and then creating it if necessary

This is a simple exercise:  do exactly as described in the title!  :-)  In this example we check for an identity, and create it if it is missing.

```
$existingIdentities=$(az identity list --resource-group $resourceGroup --query '[*].name' --output tsv)
if($identityName -notin $existingIdentities) {
  az identity create `
    --resource-group $resourceGroup `
    --name $identityName
}
```

## Keeping state between deployed resources and a configuration database

Scenario:  You have a configuration database with data about desired and existing deployments.  You need to keep state between the database and a deployment to an external service which may be unreliable.

In this example we have a table store to keep track of the number of deployments, which is important because the row number is used to calculate a unique IP range for each VNET.  However, the actual deployment could fail, leaving records in the table for VNETS which do not actually exist - there are several checks which need to be completed in order to achieve our desired state.

Most will start off with the following algorithm:

```
# Test for the VNET
$existingVNETAssignment=$(az storage entity query --account-name $storageAccount --table-name deployments --output tsv --query 'items[*].RowKey' --filter "Name eq '${VNETName}'")
if(!$existingVNETAssignment) {
  # Calculate the IP address and create the VNET
} else {
  $existingVNETDeployment=$(az network vnet subnet show --resource-group $resourceGroup --name "${VNETName}-subnet" --vnet-name $VNETName --query 'id' --output tsv)
  if(!$existingVNETDeployment) {
    # Calculate the IP address and create the VNET
  }
}
```

This will achieve the desired outcome, but it has some disadvantages:  the code to calculate the IP address assignment and create the VNET is duplicated, which can cause maintenance problems in the future because the code has to be updated in more than one place.

A better alternative is to remove the IP-address calculation code to a function so that it exists in only one place.  However, in this case we can do even better by re-ordering our condition checks, resulting in code which eliminates the multiple paths into the "new-vnet" function (and thus rendering it obsolete).  See what happens when we check for the existence of the VNET first, rather than checking the configuration database (Some code omitted for brevity):

```
$existingVNETDeployment=$(az network vnet subnet show --resource-group $resourceGroup --name "${VNETName}-subnet" --vnet-name $VNETName --query 'id' --output tsv)
if(!$existingVNETDeployment) {
  $existingVNET=$(az storage entity query --account-name ${storageAccount} --table-name deployments --output tsv --query 'items[*].RowKey' --filter "Name eq '${VNETName}'")
  if($existingVNET) {
    $VNETAddressSpace="10.7.$(8*${existingVNET}).0/21"
  } else {
    # Read all rowIDs from the storage account, set $i to 1 greater than the maximum
    $VNETAddressSpace="10.7.$(8*$i).0/21"
    # Insert the network details into the configuration database
    # (this reserves the IP range against future deployments)
    az storage entity insert ...
  }
  # Create the network
  az network vnet create ...

  # We always enter this loop and execute at least 1 sleep, giving the VNET time to provision and data to replicate
  # Then we make sure that it has finished before we move on with the rest of our script
  while(!$existingVNETDeployment) {
    Start-Sleep -Seconds $sleepInterval
    $existingVNETDeployment=$(az network vnet subnet show --resource-group $resourceGroup --name "${VNETName}-subnet" --vnet-name $VNETName --query 'id' --output tsv)
  }
}
```

Because the configuration database is updated _before_ the VNET is created, it is safe to assume that the presence of a VNET implies the presence of the configuration data.

This structure eliminates the repetition of New-VNET function calls, but it does add a repetition of the VNET existence check.  In this case, it is still a net-positive.  the existence check is less likely to have substantive changes over time, but if that was a concern it could be extracted into a function to ensure that the different invocations do not drift from each other.  The reason it is still a net positive, however, is that (especially when working with Azure) the resource-creation APIs can return before, during, _or_ after the resource is actually query-able by other APIs - your new VNET may exist, but without the resource ID you cannot reference it or create other resources which depend on it.  This means that you frequently have to include these loops in your script _anyway_ in order to wait for the resource ID to become available so that you can proceed with creating and configuring other entities.
