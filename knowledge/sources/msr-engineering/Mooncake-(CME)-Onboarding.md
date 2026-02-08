For a guided walkthrough, reference the [soverign cloud onboarding guide](https://msazure.visualstudio.com/One/_wiki/wikis/One.wiki/8650/Sovereign-Cloud-Onboarding) and particularly the [Mooncake specific guidance ](https://msazure.visualstudio.com/One/_wiki/wikis/One.wiki/8657/Direct-Access).

### Request CME Account
1. Submit [a request for your CME account](https://cdocicmrequest.corp.microsoft.com/ServiceNow/CMERequest/)

2. Once you submit the request, have your manager go into the ICM and add "I approve this request".

3. The request will be processed within 24 hours of manager approval and you'll receive email with credentials.

4. Instruction to get CME smart card should be included in the CME account detail email. Or you can submit a SmartCard request here  
    - This takes ~2 days if you are Redmond-based, at which point you'll get an email with instructions to pick up the card at Building 27.
    - This takes ~ 2 weeks shipping to your location if you are not Redmond-based.

5. Once you have your card, you need to unblock your PIN by contacting [21V-WAPHYNET@oe.21vianet.com](mailto:21V-WAPHYNET@oe.21vianet.com).

### Password Reset

1. Follow the steps in the _Access a jumpbox_ section to connect to the following machine: 
    - BJBAZUTLA05 - [Mooncake-BJBAZUTLA05-DIP.RDP](http://sharepoint/sites/CIS/eng/Security/compliance/SiteAssets/SitePages/Mooncake%20Access%20Control%20Wiki/Mooncake-BJBAZUTLA05-DIP.RDP)  
2. Press CTRL+ALT+END and choose Change a Password option
3. Proceed with standard Windows change password steps

**_Note the requirements for the CME Password:_**

- Cannot contain the user's CME account name or parts of the user's full name that exceed two consecutive characters.
- Must be at least 14 characters in length
- Must contain characters from three of the following four categories: 
    - English uppercase characters (A through Z)
    - English lowercase characters (a through z)
    - Base 10 digits (0 through 9)
    - Non-alphabetic characters (example: !,$,#,%)

### Access a jumpbox
1. Go to aka.ms/jit  and pick China
2. Sign in with your CME account
3. WorkItem Source: TFS: Mooncake and Workitem ID - ID of WI you should create in http://vstfrd:8080/Azure/Mooncake  .
4. Justification:
5. Resource Type: RDP(only Jumpbox)
6. Datacenter: BJB
7. Purpose: Debugging - Don't pick anything else, even if doing a deployment. It'll get rejected otherwise.
8. Jumpbox Name: BJBAZUTLA05
9. Access Level: Remote desktop
10. "Validate & Add Resource" button
11. "Submit Request" button
12. Once approved, RDP into the box. You'll be prompted for credentials twice: 
    - For the first prompt use your CME card + PIN
    - For the second prompt use your CME\youralias + Password

### Join CME Secure Group used for JIT
1. Send a mail to the 21Vianet team (21V-WAPHYNET@oe.21vianet.com) asking for your CME\alias that you've created to be added to **CME\RTE-CME-AZMGMT** secure group and CC Jordand@microsoft.com
2. Once you've been added to that SG, you can JIT into subscriptions that have a JIT policy setup to leverage that CME SG.
3. Currently (October 2019), only the SubsToBeDeleted service tree service has been enabled with a CME JIT Policy. Subscriptions you want to access need to be added to this service. 
    - To enable other services with the CME JIT Policy, reference the existing JIT policy on the SubsToBeDeleted service or reference [aka.ms/jit](https://aka.ms/jit) for general guidance or engage Jordan Dahl (jordand) for questions.

### Access an Azure subscription
**_VERY IMPORTANT: DO NOT GIVE YOURSELF STANDING ACCESS TO A SUBSCRIPTION. Make sure you always use JiT to access your team's CME subscriptions, otherwise you're violating the legal commitments Microsoft made to operate Azure China._**

1. Go to aka.ms/jit  and pick China
2. Sign in with your CME account
3. WorkItem Source: TFS: Mooncake and Workitem ID - ID of WI you should create in http://vstfrd:8080/Azure/Mooncake  .
Justification:
4. Resource Type: Portal
5. SubscriptionID:
6. "Validate & Add Resource" button
7. "Submit Request" button
8. Once approved, you'll have access to the subscription through the Azure portal, PS, CLI, etc.

### Access Azure portal (portal.azure.cn)
_Note: You'll first need to request JiT access to an Azure subscription, otherwise you won't see any subscriptions when you log into the portal._
1. Navigate to portal.azure.cn  
2. Sign in with youralias@cme.gbl
3. On Azure AD sign-in page, type in youralias@cme.gbl and your password
4. On the Certificate prompt, put your CME card, select your CME account from the "Other" (since it defaults to AME even after you input the CME card) and input your pin
