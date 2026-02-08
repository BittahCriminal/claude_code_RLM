The following steps is to be able to add a PME account to MSResearch ADO as a guest to setup Service Connection without inviting as an external user to the tenant. 

Sign in to PME tenant
•	create a service principle that will be used by the ADO Service connection – don’t forget to add a co-owner.
•	Create an ‘ADO’ secret for the service principle.
•	Grant this PME service principle the required access to the target AMG/Subscription/Resource group.

Sign in as a regular Admin account in MS ADO
•	Go to project, create new connection.
•	Select ARM connection – Manual
[ado.png](/.attachments/ado-a33507fe-adb1-48f8-8355-63456777c5f3.png)
 
•	In the next screen you can paste in the service principal id and the ‘secret’ you created, and ‘voila’ the connection in made.
