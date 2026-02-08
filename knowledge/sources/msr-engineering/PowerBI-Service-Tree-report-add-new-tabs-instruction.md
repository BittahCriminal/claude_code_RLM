This page is a instruction of how to add new tabs into [Service Tree power bi report](https://msit.powerbi.com/groups/fd26e2e0-b498-478b-ac30-039597e1c8b7/reports/523ed663-169f-4407-aa27-323a2f549845/ReportSection7314d7dbeb0890dbb606). 

### Content
- Edit on cloud or download
- Choose Hierarchy level 
- Work on new tab 
- Save 

### Detail steps

1. Open the report, click on Edit. 
** You can also do this on your desktop by downloading the report, you may need access to [Genevareference](https://genevareference.westcentralus.kusto.windows.net) and [Xdiv](https://xdiv.westcentralus.kusto.windows.net) kusto clusters. **For better version control, if you want to edit in pbix local file, please always download it from web portal and do not use the existing one on your local machine (which maybe not the latest version).**  

![image.png](/.attachments/image-c3a81173-632d-4ec1-98fb-fd263479392d.png)

2. Duplicate existing tabs as template by right clicking tab name, before duplicate you need to figure out the top level of the new tab is Division, Organization or Service Group. 
- If it is division, you can duplicate 'Whole Org' tab
- If it is organization, you can duplicate 'Research'/'Incubation'/'R&I Services' tabs
- If it is service group, you can duplicate any the rest tabs

![image.png](/.attachments/image-8010629b-e7ae-48af-9633-234b9caad2ea.png)

3. After duplication, we will revise the tab to include what we want in the new tab. 
- Update filters
Click on blank area inside hierarchy chart, you will see the applied filters in filter tab. Please notice, the chart include all subscriptions and we filter root element (upper level) to control what we see in the chart. Click on 'Item', only select the top level (in the example it is ServiceGroup) - Click on 'Name' - Deselect the template option and select the name that needed in new tab. 
** If you want to filter more than one level, repeat this step but select the next lower level in 'Item' then select needed name in 'Name'.
 
![image.png](/.attachments/image-51bde1f2-2587-45ef-ae8b-81f1e6e95db9.png)

After applied all filters, click on 'Item' again and check 'Select all' to select all Items. Then you will see the hierarchy chart already change to new 

![image.png](/.attachments/image-35ede6bc-7ad1-499e-b29b-bd3ab4438ddb.png)

- Update color
Due to feature of the visualization, its color will go back to default once the chart is changed. So we need to change the color manually. Still select the hierarchy chart, select formats under Visualizations tab. Select 'Type Colors' then change color of any level. 
![image.png](/.attachments/image-f61f9cb7-8de0-4d4a-9624-5cde0e508244.png)

- Update title

At the same place of update color, select 'Title' and change it. 

- Adjust default look
By selecting Item filter visualization, you can adjust the default look of hierarchy chart. Here in the example, it deselects subscription. 

![image.png](/.attachments/image-ce9bd3f7-163f-49de-b571-cf7009e87f9d.png)

- Update 'Subs under Services' table
We also need to adjust the table's filter. Click blank area of the table or lower right corner of table. Apply filter to corresponding hierarchy level. 

![image.png](/.attachments/image-0552b57a-2867-4eee-acf1-4dff38e2ebb0.png)

4. Save the report, it is all done. 
