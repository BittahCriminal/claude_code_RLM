# This is currently a draft and subject to change

[[_TOC_]]


#Why 

Gathering customer feedback is a critical area in any service maintaining a focus on the customers perspective. Not ensuring your intent is aligned with the outcomes your customers' need mean that you're leaving opportunities on the table. The inverse of this is unactioned feedback is worse than no feedback at all. For us to succeed we not only need the models and tools but culture and commitment.

This page is to help outline the models and tools you can use to simplify collecting customer feedback.

# Model

Choosing the right model is the first step to closing the customer loop.The most common model leveraged in Microsoft is CSAT or Customer SATisfaction Surveys. There are huge groups internal to Microsoft that have provided a wealth of information and tools. Our services do not necessitate this large of an investment, but we can benefit from their learnings. 

### Questions
To start off we need a consistent model to ensure we can evaluate dissimilar services. To do this we take learnings from others:

- Keep It Short, Keep It Simple – The average customer will devote around 90 seconds to completing a survey. That’s enough for a general CSAT question and a question about their specific experience. 
- Use an Odd-Numbered Scale – A good survey should have an odd-numbered scale because an odd number of scale points gives participants a middle-ground or neutral response option.
- Include an N/A Option in the Answers – A major annoyance for customers completing surveys is finding that they are obliged to answer questions which are not relevant to their experience. Offering an N/A or a “I don’t know” option is important for this reason.
- Keep Your Surveys Consistent to Track Change – If you’re changing your survey questions you’re not getting consistency. You might be able to add something in or tweak it slightly, but you’re not going to get long-term quality data if you keep changing what you’re asking.

To facilitate the above we will leverage a 1-5 score with 1 being low and 5 high. We will also provide a text field to capture the nuance in the engagement. 

An example is as follows:

![image.png](/.attachments/image-aeb60990-af64-4b12-b719-65eb1f5a74ea.png)

### Scoring 
For our purposes we will start with the simplest formula for calculating our percentage. 

![image.png](/.attachments/image-146a4ccb-1683-46dc-a9fa-9fff61ad0034.png)

### Learnings
- [Linkedin Courses](https://www.linkedin.com/learning/search?keywords=Customer%20Satisfaction&u=3322)
- [CSAT/NPS/CES](https://delighted.com/blog/choose-customer-satisfaction-metric-csat-nps-ces#:~:text=The%20main%20difference%20between%20CSAT%20and%20NPS%20is,built-in%20connotation%20of%20the%20words%20%E2%80%9Csatisfaction%E2%80%9D%20and%20%E2%80%9Crecommendation.%E2%80%9D)
- [Customer Experience Framework](https://microsoft.sharepoint.com/teams/CSS/SitePages/Customer-Experience-Framework---Trainings.aspx)
- [Calculating CSAT](https://www.callcentrehelper.com/how-to-calculate-customer-satisfaction-csat-109557.htm)

# Culture

To effectively close the loops with customers you must first change the culture of the environment and team. Below is a great PPT that covers how we can incentivize our customers to participate in our calibrations.

### Learnings

- [Promoting CSAT PPT](https://microsoft-my.sharepoint.com/:p:/g/personal/kwhitney_linkedin_biz/ERMLYstWxYtIgradmTPjYKkBxTMmplo7yUwJaWiZooO-Rg?e=3b4ifd)

# Tooling

For us to succeed we need to identify how to collect, report and respond to feedback. Thankfully Microsoft has a suite of tools available. 

One option is Dynamics 365 Customer voice. This is directly related to our goals but does not have broad extensibility. Many of the features are disabled by our tenant admins.

Another option is to leverage Power Automate. This has integrations into many other supporting services which makes managing feedback easier than it ever has been. The below documentation will cover this solution path as it is likely to be more supportable in the long term. 

There are a few components we need to succeed:

1. A Model
This is covered above
2. A intake interface
This will be [Microsoft Forms](https://forms.microsoft.com/)
3. A datastore
This will be a [SharePoint list](https://microsoft.sharepoint.com/teams/TnREng7/Lists/RTE%20Service%20Feedback%20List/AllItems.aspx?env=WebViewList). This also provides a way to co-manage the automation. 
4. A report
This will be [Power BI](https://msit.powerbi.com/sharepointlist?spListId=%7Bf3038d5f-24eb-411d-8f2c-3aca82a7498c%7D&spListUrl=https:%2F%2Fmicrosoft.sharepoint.com%2Fteams%2FTnREng7%2FLists%2FRTE%20Service%20Feedback%20List&spListUniqueId=30bf223a-eb7f-4432-8aeb-5a08cd276785f3038d5f-24eb-411d-8f2c-3aca82a7498c&culture=en-US)
5. An automation utility and run as accounts [Link](https://preview.flow.microsoft.com/en-us/)
This will be Power Automate an individual user accounts (for now)
6. A process to review and action responses
This will be a Rhythm of Business defined by individual teams. SES will be leveraging ADO and our team meetings for reviewing feedback. We will also leverage teams to post notices for others to review.

Another consideration is how to ensure we're not introducing single points of failure. To ensure we have broad coverage you should have multiple people with access to edit the flow. Another option is to only share [run-only rights](https://docs.microsoft.com/en-us/power-automate/create-team-flows#share-a-cloud-flow-with-run-only-permissions). The latter doesn't allow changing the accounts which could be problematic

### High level process

The high-level flow is as follows:
![image.png](/.attachments/image-0478e547-d059-4e30-aca0-61213e58a720.png)

### Detailed Process
#### Init
First step is to create a form that covers the intended question space. You can use the following template to start.

[RTE Engineering Feedback Template](https://forms.office.com/Pages/ShareFormPage.aspx?id=v4j5cvGGr0GRqy180BHbR76OrARN1BZPuO10ui1WIPZUOURLMzRLQjE2SjFITFg4REVGR1lLSlRJVC4u&sharetoken=CKIRXfqgLS094CcVsrvm)

#### When a request is submitted
Once you have the form you're ready to configure the power automation details. 

To start I like to use the first connector which would be Microsoft Forms and the first is 'When a new response is submitted'. Once created you'll need to select the form you want to initiate the action from.

####Get Response Details
The next step to add is getting the response details of the form. This is important as it will give you access to the form answers and other metadata.

####Create item (SharePoint)
This step takes the form response details and injects it into a SharePoint List. This could be adapted to update specific fields like Service. This allows us to keep a centralized location for all feedback. It also allows us to leverage the built in PowerBI report in SharePoint. 

**This list is currently specific to the form I used to create it. There will need to be effort to normalize this list so many forms can leverage it.**

An example of a configuration:

![image.png](/.attachments/image-c7caafd3-7bf9-4122-8f0a-6f7aad9f89b8.png)

#### Create a work item (ADO)

This step takes the form data and creates a work item in the backlog. There are many options you can leverage but the below is a good example of how and where to create.

**The important part of this is to get the Area Path set correctly. This will allow us to review all feedback as a team**. This variable is available under Advanced Options.

**Basic Options**
![image.png](/.attachments/image-57694ab7-08ce-4e73-b37d-46fc0c9ec8c3.png)

**Advanced Options**

![image.png](/.attachments/image-e9ddaa53-116a-443e-bb1f-e42a4acfb02e.png)

#### Post message in chat or channel (optional)

This step isn't required but a good way to drive immediate awareness to the feedback. Note that this feature does NOT work with private or shared channels. It does work with Private teams if the run as account has access to it. 

![image.png](/.attachments/image-54b527a6-ebc9-49f3-a9e8-df3e7d28e49d.png)

#### Final steps

You did it! You now have a flow that will create a trail of accountability to ensure we action our feedback. The last step is to test each action and ensure it creates the intended artifact.

If you used the SES Customer feedback Area path (required if in SES) you can use this query to validate work item creation.

[SES Customer Feedback Query](https://dev.azure.com/msresearch/MSR%20Engineering/_queries/query/39eb9e3d-20bf-4fa7-b4b0-514f50b3b98f/)

## To Do

- Clarify Power Automate workspaces
- Identify how we can simplify sharing
- Normalize SharePoint List to work for all forms
- Validate documentation supports team understanding
- Add more Power Automate details (support, accounts, permissions)
- Add details on ADO work item assignment standard
- Define Team touchpoints (Email signature, wikis, SharePoint, etc)

## Team Questions / Comments
Creating a section for people to stick comments / feedback 👇🏻
### Customer Feedback Intake Interfaces
What are the ways we currently receive feedback?
    - Email
    - Word of mouth
    - Teams
    - Tickets
    - Forms / Surveys (e.g. GCR Outreach / T+R Compliance / Pulse / others ?)

As we receive feedback from the above, how can we channel that into the right interface (e.g. the above process)?
- Research Support member can file the above feedback "on behalf of" the customer to our "#OneSupportForm
     - Does MSRSupp/Dev/PM/KMALL know how to channel this type of feedback appropriately across SES services?
     - Is there a feedback loop between Ops/Eng/PM/Customer and the hands off / interfaces between each?
     - Is there a lower overhead way to funnel this feedback?

- Educate customers on the value of #OneSupportForm leveraging our feedback interfaces 
         - If we're consistent with showing it across our wiki + RTE Depot + Signatures + etc and is reinforced, we may get traction of people using it

- Can we demonstrate transparency (key results) on how feedback is handled / actioned + allow for community to also contribute/self-service answer things? (e.g. +1 other issues to help us prioritize and allow others to discover)

- Are there other teams across MSR that are interested in helping us shape this or benefiting from it for their own efforts? (e.g. can we incorporate this in project tracker so people across MSFT can funnel feedback to teams in MSR? Teams in MSR can funnel feedback to other teams in MSR or "Throw it out" to the public in case they don't know how to get help?)

### Feedback Lifecycle Thoughts
When do we setup new "Feedback" loops? Just for critical services? For wiki entries? For "Team/individual" feedback? 

Where do I go to discover the various forms available to route any feedback I hear from customers to the right service?

If the overhead for initial setup for the forms is too high, there is a high likelihood nobody will do it.
- Can we make it trivial to submit something to a Form that will automate the powerautomate form creation process for <generic support need>?

### Feedback Review 
What is the rhythm for When we review and action feedback?
Should others across the team help others create/review surveys? (consistency / awareness / collaboration)

If people send in information and a service owner can't action it (but someone else might be able to), how do they loop in others? 

What if choose not to action it? Do services respond and inform the customer? Is this adding overhead? (could automate responses based on state changes)

Can we give the division actionable analytics from a #OneMSRFeedback dashboard?
- Support Needs (Is MSR operationally effective?)
- Internal sentiment (Is MSR useful?)
- External sentiment (Does anyone know about MSR?)

## Learnings
[Power Automate Team Flows](https://docs.microsoft.com/en-us/power-automate/create-team-flows)
[One Customer Voice](https://www.owiki.ms/wiki/OCV/Getting_Started_With_OCV)
