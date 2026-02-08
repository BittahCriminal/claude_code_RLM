OtterBrass is a PR assignment tool created by [Vidal Guillermo Diazleal Ortega](mailto:vidorteg@microsoft.com). Below is a quick start guide and notes about its limitations. 

Quick start:

- Find the next person in line with the **@otterbrass [next] $PR_link $description** command. This gets the next person in line and provides details to enable their understanding.
- You then need to assign the PR to the next in line with the **@otterbrass [assign] @user** command.  This credits them with the PR and puts them at the bottom of the list.

Other helpful commands:

- Before you can do the above you must add users to the rotation by leveraging the **@otterbrass [add] @user** command. This has already been done but may need updates at a certain point.
- If you are out of office you can set this with **@otterbrass [OOF] @user**.  This will avoid the user in the assignment rotation.  Use **@otterbrass [!OOF] @user** to put the user back in rotation. 

Limitations:
- Otterbrass only supports one project team.  This could be an issue if you have specific teams that manage different projects in the same teams team. 

Installation: 
- Currently this is a custom app you'll need to side load.
- Zip file located at \\\research\msrsupp\Software\OtterBrass
- Open teams and select manage team. 
![image.png](/.attachments/image-2d1492c3-c0db-4538-8c35-8e7b53dced82.png)
- Under apps select upload custom app
![image.png](/.attachments/image-31827a4a-fd5e-4173-91a7-5ea145f30a6c.png)
- Point the file explorer to the zip file.