**Adding more than 4 users to a GCR sandbox** 

GCR reservation chronos portal allows up to 4 users maximum to be added to the GCR sandbox using the GCR-reservation portal.

In some cases we get request to add more than 4 users to a system. In order to add more than 4 users do the followings:

- login to the node you want to add user to. 
- Modify /etc/group and add the user for example REDMOND.v-obalouchi to msrsupp group like this 

![image.png](/.attachments/image-626567d1-4eb3-4c97-b539-5a6f071d272a.png)

- Once the group is added add group_msrsupp under /etc/sudoers.d by doing :

cd /etc/sudoers.d 
vim group_msrsupp
and add the following: 

`%msrsupp ALL=(ALL) NOPASSWD:ALL`

![image.png](/.attachments/image-47786218-abf9-4768-ab24-a658a4d4c6ea.png)

![image.png](/.attachments/image-f3c18301-f0d9-47eb-b1c7-5230044cbb1c.png)

![image.png](/.attachments/image-8a71799e-4bd7-4953-8561-dfc5036ff80f.png)

This is it now the user should have access to the node and use their SSH key to login. **Note that this will give user permanent access to the node even when the reservation is closed if the node does not get re-imaged. so the user needs to be manually removed from above to revoke access.** 