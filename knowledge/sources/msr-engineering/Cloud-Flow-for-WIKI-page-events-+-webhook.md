**Step 1: Create a Cloud Flow for Wiki Page Events**

Log in to Power Automate:
- Go to [Power Automate](https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fflow.microsoft.com%2F&data=05%7C02%7Cv-ahuetson%40microsoft.com%7C318b6684d9774240980d08dd1927046b%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638694377565036997%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=LDOe32z1a09VrDvrVIEGqGd5X4F59QiOvBMLguIZN%2Fk%3D&reserved=0 "Original URL: https://flow.microsoft.com/. Click or tap if you trust this link.").

Create a New Cloud Flow:
- Select “Automated cloud flow”.
- Name the flow (e.g., Wiki Page Notifications).

Set the Trigger:
- Trigger: Use the Azure DevOps connector.

Select:
- Event: When a work item is created or updated (closest option; Azure DevOps doesn’t natively have a wiki-specific trigger).

Conditions: Filter for work item types related to wiki updates (if applicable).
- Add an Action: Send Email:
- Use the “Send an email (V2)” action.

Configure:
- Recipients: Specify stakeholders (dynamic email IDs or fixed recipients).
- Subject: “New Wiki Page Created” or “Wiki Page Updated.”
- Body: Include relevant details, e.g., page title, last modified date, and a link.

**Step 2: Schedule Flows for Page Reviews**

Create a Scheduled Flow:
- Select “Scheduled cloud flow”.

- Name the flow (e.g., Wiki Page Review Reminder).
- Set the frequency (e.g., weekly, monthly).

Add Azure DevOps Action:
- Use the Azure DevOps Get Wiki Pages action (or Get Work Items if wiki-specific pages aren’t listed).
- Fetch pages modified within a specific time range.

Send Reminder Emails:
- Add “Send an email (V2)” action.

Configure:
- Recipients: SMEs or contributors responsible for review.
- Subject: “Wiki Page Review Due.”
Body: Include a list of pages due for review, with links.

**Step 3: Share the Flow**
Access the Flow:
- Go to the flow’s details in Power Automate.
- Add Co-Owners:
- Click “Share”.
- Add the SMEs as co-owners (they need a Power Automate license to edit/monitor the flow).
- Send Notification to SMEs:
- Inform SMEs about the shared flow and how to access it.

Notes:
Azure DevOps Wiki-Specific Triggers:
If Azure DevOps lacks direct support for wiki page events, consider using:
Azure DevOps REST API for custom triggers.
Integrate webhooks from Azure DevOps to trigger flows.

Testing:
- Run test cases for the flow to ensure emails and triggers work correctly.

Would you like more details on Azure DevOps integration or using REST APIs?

# **To create a backend webhook for Azure DevOps to trigger events like wiki page creation or updates, follow these steps:**

**Step 1: Set Up an Azure DevOps Webhook**
- Go to Azure DevOps Project Settings:
- Open your Azure DevOps project.
- Navigate to Project Settings (gear icon in the lower-left corner).
- Create a Service Hook:
- In Project Settings, go to Service Hooks.
- Click Create Subscription.
- Choose an event type. Unfortunately, Azure DevOps doesn’t provide a native Wiki page trigger, but you can select:
- Work item updated (if linked to a wiki page).
- Code pushed (if wikis are managed as markdown files in repositories).
- Configure Trigger Details:
- Set up filters to refine the trigger (e.g., specific branches or work item types).
- Add any conditions required for wiki-related changes.
- Set the Webhook URL:
- Enter the Webhook URL of the backend service that will handle the event (this service needs to be built—steps below).

**Step 2: Build the Backend Webhook Listener**
- Use Azure Functions (serverless option for Azure).
- Create the Webhook Endpoint:

Deploy the Webhook Listener:
- Deploy your webhook listener to a publicly accessible environment (e.g., Azure App Service, AWS Lambda/API Gateway, or Heroku).
- Secure the Webhook:
- Validate incoming requests:
- Check the shared secret token (set in the Azure DevOps Service Hook).
- Process the Event:
- Parse the payload from Azure DevOps.
- Trigger actions, such as:
- Sending an email.
- Forwarding the event to Power Automate (via an HTTP Request action).

**Step 3: Integrate with Power Automate**
- Create a Flow with HTTP Trigger:
- In Power Automate, create an Instant flow.
- Use the “When an HTTP request is received” trigger.
- Copy the generated HTTP URL.
- Forward Events to Power Automate:
- Modify your backend webhook to forward processed events to the Power Automate HTTP trigger URL.
   
