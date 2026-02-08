# Introduction
When you have an internet first network with no Load Balancer, and no Public Ips, Azure will assign a random ip address for SNAT, as documented [here](https://docs.microsoft.com/en-us/azure/load-balancer/load-balancer-outbound-connections) in Scenario 3. This will prevent hosts in the network to getting to other resources on other networks since there's no way to whitelist their assigned addresses.
 

>When the VM creates an outbound flow, Azure translates the source IP address to a dynamically allocated public source IPaddress. This public IP address isn't configurable and can't be reserved. This address doesn't count against the subscription's public IP resource limit."

The solution is to create a NAT gateway, This requires a dedicated IP Address, which doesn't seem to get used, and an IP Prefix, which the network does seem to use. The one gotcha with creating the NAT gateway is that, for the IP Prefix portion. you need to create a /29 (8 addresses) or smaller. If you create a /28 (16 addresses), you will get an error of creating a network with too many addresses.

# Creating a NAT Gateway
- From the Resource group, Click Add
- You should find the NAT gateway product like so
 ![image.png](/.attachments/image-ac223013-18f1-42dd-90fa-20574de8ad1d.png)
- You'll want to define the correct region, and give the NAT gateway a name.
 ![image.png](/.attachments/image-ff8f7c73-ba1a-43d6-9f98-aa5eba5e2ed3.png)
- You'll define your addresses. The prefix seems to be the one that matters. In this example I created new ones. You'll need to create a /29 (8 addresses) or smaller. If you create a /28 (16 addresses), you get an error of creating a network with too many addresses.
![image.png](/.attachments/image-49c89f69-9ff5-4466-a61a-7c6167aae3fd.png)
- Define the VNET this will be attached to. Ensure this VNET has no public ip addresses or load balancers, or you'll get an error when it tries to create everything.
![image.png](/.attachments/image-0696d42a-6bc8-45eb-ba9a-d9f74a3c13ef.png)


Once you've done this, you'll want to reboot any hosts on the VNET for the new settings to take effect.
# Workaround
Currently, we have an Azure Function that adds ip addresses to the necessary NSG to ensure hosts can get to the PGSQL host. However, it doesn't currently add ip-prefixes. For now, prefixes will need to be added to the [MSREngInfraExt-NSG](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/MSREngInfraExt/providers/Microsoft.Network/networkSecurityGroups/MSREngInfraExt-nsg/overview). For prefixes in GCRProdEx1, there is a rule `GCRProdEx1-prefixes` that can be used.