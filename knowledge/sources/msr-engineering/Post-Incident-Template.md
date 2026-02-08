# How to use this page

- Copy the text below and move it to a work item under the area it applies
- Fill out the required details from your perspective
- Ask others that participated to do the same (you may need to drive conversations if outside of RTE)
- Share work item with stakeholders and possibly customers
- Create work items for committed work to prevent from happening again

------------------------------------


# {DateHere} - {SummaryTitleHere}

This is a blameless post incident document that outlines the timeline, the contributing factors, the mitigations steps take and any action items or learnings from the incident.

[Please fill in the following sections as part of post incident meeting]

## Timeline

[A third person account with exact times of all the events that doesn't include any names. Please replace the example below]

- [~2022-08-01 10:05am] engineer 1 logged into ASI and tried to load the managed cluster page but it was not loading
- [~2022-08-01 10:05am] Engineer 1 began investigating the log output on the server
- [~2022-08-01 10:15am] Engineer 1 noticed that there were an unusual number of 401 requests coming from Kusto
- [~2022-08-01 10:20am] Engineer 1 identified a bad release that had misconfigured the AAD settings for Kusto access
- [~2022-08-01 11:00am] Engineer 1 created a PR to resolve the issue
- [~2022-08-01 11:05am] The PR was merged into master
- [~2022-08-01 11:10am] The release was deployed to all regions and the issue mitigated

## Contributing factors

[A concise list of the key contributing factors that lead to the incident. Pleas replace the example below].

1. Lack of e2e testing validating high value transactions in the app including viewing a page that queries Kusto.
2. Insufficient alerting of failure to authenticate against Kusto

## Mitigating steps

[Specific steps that were taken to resolve the incident]

- Created a PR to revert the bad changes

## Action items and learnings

[Specific actionable tasks with assigned owners that would prevent this issue from occurring in the future]

1. Create e2e test that views a page with Kusto queries on it
2. Create a specific alert for Kusto authentication issues.

## Linked work items
- Item 1