Service details
##Service Name:
SSL Administration and certificate management
##Service Description:
MSR Currently manages multiple certificates for researchers and administrative functions. Currently we utilize multiple Certificate providers, with multiple capabilities. 
With our compliance initiatives ramping up, additional KPI's are being added in S360 that can/will effect how this service is currently being used.

##Service Requirements:
Certificate Issuer(s)- Onecert, DSMS, SSLADMIN
SAW (Potentially)
Certificate secured asset/service
Azure Key Vault


##Costs
###Infrastructure costs per month
~$100 for Key Vaults
###Engineering Time
SES hours per month
10-20

#Risks 
LifeCycle management (Expired Certs) 
Leaked secrets

##Benefit
Many of our researchers do not understand certificate hygiene, management or installation. Currently we utilize SSLAdmin to help request and install these certificate however this service will be deprecated in the near future. Microsoft IRMC is also adding many new KPI's in S360 regarding certificates (Auto-rotation, 30/60/90 day expiration, Issuer/Intermediate Chain, etc.). Having a more centralized service may help us quickly, and easily get our services compliant

##Audience
Division
Active Customer count (Year, Month of Month if possible)
20-30
Active Customer list (year if you can)
In progress
Time saved
Estimated 50-100 hours per year. 

##Dependencies
What other services does this depend on- 
OneCert
SSLAdmin
Keyvault
DSMS 
Secured Resources
SAW


Assessment
State the case on what you feel we should do to this service. Options are:
I feel that we should Investigate, and then possibly enhance this service. I believe we might be able to invest a small amount of engineering time to provide a more centralized, semi-self sustainable service. 

Enhance - Make the service better
Sustain - Keep this online with minimal effort
Migrate - Move this to another solution/technology
Decommission - Remove the service from our portfolio
Result
This is after the case has been made and the decision of the team.