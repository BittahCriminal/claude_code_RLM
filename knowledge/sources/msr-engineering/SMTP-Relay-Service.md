This page is to provide a template for the questions we want to answer so we can understand the cost benefit ratio of our services.

# Service details

Service Name: SMTP Relay service
Service Description: The SMTP relay service allows IOT devices like Disk Controllers, NAS appliances and other non-windows devices to send emails without Auth Info. Main requirement is that the IP address was registered. 
Service Requirements: OnPrem VM

# Costs
- Infrastructure costs per month. OnPrem VM
- 3rd party software review. 
- SES hours per month 1 hour: Confirm MSR-tools is patched.
- risks (public endpoint)
-- Accessible from Corp Address only. Meant for labs only. It only allows "@microsoft.com" recipients. 
-- Sender cannot be tracked (Only IP address source)
-- Software package used is Surgemail. We switched to it around 3 years ago due to minimal logging capabilities available in IIS SMTP. Switching back to IIS is possible. 

#Benefit 
How do you quantify the benefit of the service 
- Changes in server infrastructure are made only on SMTP Relay.
- Password changes not needed on clients (No password needed)
- Ip registration only requirement.

- Time saved: Clients do not need make modifications due to password changes, Infrastructure changes. 

# Dependencies
- 3rd party software review for Surgemail.
- 2FA exception required for System account 

# Assessment
State the case on what you feel we should do to this service. 

- Decommission - Remove the service from our portfolio. Redirect them to use O365 DirectSend or Microsoft Graph. The population of Disk Controllers and IOT devices needing the service has been declining and going towards 0 as SuperMicro systems get recycled. 

# Result

Decomm SMTP Relay Service