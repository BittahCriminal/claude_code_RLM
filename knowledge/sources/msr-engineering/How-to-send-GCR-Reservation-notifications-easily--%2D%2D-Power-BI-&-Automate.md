This page contains instruction of how to use GpuMetricsUtil Power BI report, and is consist of 

- instructions for GCR Support team on how to send bulk notifications to users through Power BI and Power Automate. Here we refer the [GpuMetricsUtil](https://msit.powerbi.com/groups/fd26e2e0-b498-478b-ac30-039597e1c8b7/reports/24d5493d-1c7e-4a1e-bcb6-fd0d7a330642/ReportSectioncca4a33fec86780a8d6d) Power BI table as the user contact lists.  
- how to exclude reservations from PowerBI warning/closing table.

[[_TOC_]]

##How to send bulk notifications

Due to the limitation of Power BI, if we want to use filterable Power BI tables as data source we have to achieve the above goal manually. To send bulk notifications, we need two steps. 


###1. Create/Update data source 

  - Go the [GpuMetricsUtil](https://msit.powerbi.com/groups/fd26e2e0-b498-478b-ac30-039597e1c8b7/reports/24d5493d-1c7e-4a1e-bcb6-fd0d7a330642/ReportSectioncca4a33fec86780a8d6d) Power BI report, you should have access if you are in TnrEng group or please apply access. 

  - Click on the second page which direct you to the "warning list". Hang over your mouse on the warning list table then you will see several options shows at the top right corner. Then click on 'Export data', and export the table to your local machine. 
![image.png](/.attachments/image-53cb739c-7e23-4756-9a2c-5f9c02ac4078.png)
  - Upload the file to SharePoint to update the latest information, currently they are saved in [TnrEng/Documents/GCR GPU Email notification](https://microsoft.sharepoint.com/:f:/t/TnREng7/Et84T0KcDUZIrvZ1XNRnaRUBhqtn3s_CHH4lvGdCugzkYQ?e=5gSp9N).

![image.png](/.attachments/image-6322bfb3-5f59-487a-926c-07763abb48cd.png)
  - Go back to Power BI report and select the third page to go to "Closing list". Repeat the export, upload process. 


###2. Trigger flow in Power Automate 
  - Go to [Power Automate](https://preview.flow.microsoft.com/en-us/) portal, go to my flows then go to shared with me. You should see two flows (with name as GCR-Reservation Warning/Closing Notifications), if not please contact v-zhohan@microsoft.com or v-stsatt@microsoft.com and add you as the owner. 
  - Then we need to click on the the 'start run' button for each of the flow. The default sender is GCRSupp@microsoft.com and any failure of sending email will be sent to this address. You can change the sender, file path and table name in the flows if needed.   


![image.png](/.attachments/image-6dcdba48-8371-442d-a06d-9d64f9150977.png)

##How to exclude reservations 
It is troublesome to remove reservations that we don't want to send email to every time from the downloaded spreadsheet. Thus we can exclude those reservations from Power BI table in advance. To do this: 
- Go to [GpuMetricsUtil.Reservation&VM Util_WarningList](https://msit.powerbi.com/groups/fd26e2e0-b498-478b-ac30-039597e1c8b7/reports/24d5493d-1c7e-4a1e-bcb6-fd0d7a330642/ReportSectioncca4a33fec86780a8d6d) tab (or ClosingList tab), here I use Warning tab as an example. 
- Enter Edit mode, click on anywhere of the 'Warning list' table, then you will see a filter bar shows up at right side. 
![image.png](/.attachments/image-8210cabd-9aa1-41ae-9c62-540a508081e3.png)

![image.png](/.attachments/image-5f009853-d597-4991-8874-1c25d188f3f7.png)
- 1.Expand 'ReservationId' column; 2.select Filter Type as 'Basic Filtering'; 3.then check 'Select All'(if not checked); 4.last uncheck those reservations that you want to exclude (here use 26561 as an example). You can also use other column to do the exclusion if needed, method is the same.

![image.png](/.attachments/image-377662e1-614c-45da-b3a4-f03675b7c39e.png)

- Last we need to save the report. Click on 'Save', then go back to Reading mode. 

![image.png](/.attachments/image-f3eeee59-f0cf-47f3-9564-ca59cf12a154.png)