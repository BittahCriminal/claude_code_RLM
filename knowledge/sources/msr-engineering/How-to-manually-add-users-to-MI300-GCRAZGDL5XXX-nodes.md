If you want to add users to GCRAZGDL5XXX series do the following

*   Just go to Azure find the node in question and add the person to the `Chronos:Usernames` tag.
*   Since MI300 GCRAZGDL5XXX VMs weren’t part of Chronos, so the tag didn’t exist. I manually applied the required tags.
*   Once the tag is in place, the `gcr_reservation` binary will automatically update the reservation.
you can also run the following manually but you still need to add users to chronos tag otherwise, gcr_resrvation binary assumes the user does not exist and delete it from the node

    add_sandbox_user.sh useralias@microsoft.com

Then, verify the user was added correctly by checking `/etc/sudoers` and `/etc/group`.


![image.png](/.attachments/image-493a86e3-6717-46d6-8212-c1718fad5b53.png)