# Creating an Agent Pool
Agent pools cannot be created directly:  instead, you will need to contact MSR-ADO and an administrator will create the agent pool on your behalf.

Send an email to [msr-ado](mailto:msr-ado@microsoft.com&subject=Agent%20Pool%20Creation%20Request&body=Hello%0D%0A%0D%0AI%20would%20like%20an%20agent%20pool%20created%20to%20support%20my%20ADO%20pipelines%20according%20to%20the%20following%20information%0D%0A%0D%0ARequested%20name%20-%20%0D%0ASecurity%20group%28s%29%20to%20which%20administration%20should%20be%20delegated%20-%20%0D%0ASecurity%20group%28s%29%20which%20should%20be%20granted%20permission%20to%20utilize%20pool%20assets%20-%20%0D%0A%0D%0AThank%20you%0D%0A%0D%0A) with the following information:
- Requested name of the agent pool
- Security group(s) to which administration should be delegated
- Security group(s) which should be granted permission to utilize pool assets

Once this email is received your pool will be created and instructions for any additional steps will be provided.

# Adding agents to an agent pool
Once your agent pool has been created, you need to add agents to it so that work can be processed.  To do this, navigate your "Project Settings" page, and then select "Agent Pools" from the configuration menu.

 ![ado_agent_pool.png](/.attachments/ado_agent_pool-a4f95204-e8ad-49cd-b7a5-421f1b934ac4.png)

Select your agent pool from the list of available pools.  Then Select "Download Agent".  Follow the on-screen instructions for installing and configuring your agent according to the operating system and architecture in use.

# Assigning work to an agent pool
Once agents have been assigned to your pool, you can assign work to them.  From the pipelines category in your project portal, select the pipeline which you wish for the agents to process.  Select 'Edit', and then select your agent pool from the drop-down menu.

If you have not yet created a pipeline, you may assign your agent pool to a new pipeline during the creation process.
