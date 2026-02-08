Sometimes we receive request to exclude some nodes from monthly patching. If this happens, do the following:

- PIM into Sub "Grand Central Resources Production 2"
- We'll assume the nodes we want to exclude are GCRAZGDL0389 and GCRAZGDL0272 
- Navigate to the "GCR-patching" Log Analytics workspace and click on Logs to create a new query where you'll look for all available GCRAZGDL excluding the above two nodes 

`Heartbeat | where Computer contains "GCRAZGDL" | distinct Computer
| where Computer <> "GCRAZGDL0389"
| where Computer <> "GCRAZGDL0272"`
 
- Run the above query and save it as a function, checking box for "Save as computer group". This will exclude two above nodes from list of GCRAZGDL nodes. 

![image.png](/.attachments/image-9404e182-8ed8-4877-bc9e-677d2823ac83.png)

- Now navigate to "gcr-automation" Automation Account and start your scheduled deployment but instead of using the "Groups to update" tool selecting by Sub and RG, use the "Machines to update" tool to select the Saved search function group you just created above. 

![image.png](/.attachments/image-919f4df2-234c-4046-8714-c084b54672b5.png)
![image.png](/.attachments/image-53849ec3-bd6c-4ce2-ba1a-53063859edaf.png)

![image.png](/.attachments/image-81fbf3ba-fe81-4456-8dcb-47934546245d.png)