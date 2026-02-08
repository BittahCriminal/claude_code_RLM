# Service details

**Service Name:** Linux AuthN／AuthZ Service
**Service Description:** 
This service has two main components:
- Flat files (passwd, group and shadow) with users synced from specified groups from AAD
- An ssh public key database for the above users

These two components allow users to ssh into Linux systems using an ssh keypair of their choice that they managed via a portal. Th user/group database is synchronized regularly from AAD, which allows automated user onboard and offboarding.

## Service Requirements
### Backend
- Azure Key Vault - Storage of public keys
- Azure Portal - Portal for ssh public key management

### Client Side
- Ubuntu Linux
- Modification of several configuration files on the Linux host

# Costs
- Infrastructure costs per month
  - $15/month
- SES hours per month
  - Patching 1 hr
- Risks (public endpoint)
   - Public Azure Portal endpoint
      - Secured with Azure App Service Auth
   - SSH keys are single factor authentication

#Benefit 
How do you quantify the benefit of the service 
- Audience - Division
- *Active Customer count (Year, Month of Month if possible)* - TBD
- *Active Customer list (year if you can)* - TBD
- *Time saved*
- Security: Removes the use of passwords on Linux systems
- Allows consistent user ids, group ids, and authentication components on clustered systems.

# Dependencies
* _See service requirements_
* GCR Sandbox depends on this service
* ITP cluster depends on this service
*  #150675 one off instances depend on this service (not tracked)

# Assessment
State the case on what you feel we should do to this service. Options are:

- Enhance - Make the service better
  - Make this more security compliant by making this use some sort of corporate 2FA (Windows Hello, Yubikey, Microsoft Authenticator).
  - Use ssh certificates with AKV. Some ideas [here](https://smallstep.com/blog/use-ssh-certificates/)

# Result

This is after the case has been made and the decision of the team.

# References
[Linux user+group service](https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/3751/Linux-user-group-service)
## Competing but incomplete product
[Preview: Login to a Linux virtual machine in Azure with Azure Active Directory using SSH certificate-based authentication](https://docs.microsoft.com/en-us/azure/active-directory/devices/howto-vm-sign-in-azure-ad-linux)