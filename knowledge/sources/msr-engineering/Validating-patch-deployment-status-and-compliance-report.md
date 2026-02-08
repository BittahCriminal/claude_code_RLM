**Check deployment status**

After your scheduled deployment starts, you can see its status on the History tab under Update management. The status is In progress when the deployment is currently running. When the deployment ends successfully, the status changes to Succeeded. If there are failures with one or more updates in the deployment, the status is Failed.

**Note:** If you see overall status after patching says failed! don't panic it doesn't mean your patch deployment went wrong, most of the times you see the overall status as failed, the reason is even if a single package out of thousands of packages fails to update, the overall status turns to failed. this is a bug with Azure. As long as you take care of the nodes which has failed status in front of them and patch them manually it means your patch deployment were successful. 

There are always some manual patching needed historically we have nodes that doesn't get patched all the time even using batchpatch and need to manually login to the node and patch them manually. Same scenario here in Azure patch management, difference is Azure tells you exactly why your patch deployment failed on a node and gives you plenty of information  

**How to validate patch deployment status**

- Under update management in gcr-automation click on history then navigate to your latest patch deployment which you scheduled earlier. 
![image.png](/.attachments/image-cd344f9a-a5ae-4f67-b005-def8dcb7d030.png)

- Click on the one you scheduled to deploy and then go through the lists you will see the status in front of each nodes says succeeded which means your patch deployment has been competed successfully on those machines. Look for the one that has failed status and click on them to get more logs and information about why it failed.

![image.png](/.attachments/image-16ed6ed5-eeef-4c90-aea8-ffa67dc8f7c5.png)

- If you see patch status failed on a node then you must manually RDP to the node and patch them manually and reboot. Once you reboot the compliance scan will run  again within 15 minutes and you will get a new compliance report for the node you just manually patched 


![image.png](/.attachments/image-f86dc748-1531-4d60-a2cc-426b556bcd74.png)