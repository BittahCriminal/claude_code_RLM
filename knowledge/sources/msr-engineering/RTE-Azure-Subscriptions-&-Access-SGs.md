## Azure

When hosting in Azure you need to understand the scope of your deployment.  Are you just testing?  Do you know you'll be deploying for others?  These can impact how you execute your deployments.  If you are contributing to an already existing service (like GCR) this will define what subscriptions you use to deploy.  For those that are net new you will need to create.  Below we'll cover those that have general usecases and could be used for testing or services that are for our team only.

This list of RTE Azure subscriptions is organized by access group and is current as of 11/6/19. Please contact @<5CAC31D0-D85D-4056-A4D3-F252E353DDC5> if you need changes/updates to this page content.

If you need administrative access to a subscription on this list and are not part of the associated security group, please use the links below.

- **[RTE-GCR-RW](https://idwebelements/GroupManagement.aspx?Group=RTE-GCR-RW&Operation=join)**
- **[RTE-ENG-RW](https://idwebelements/GroupManagement.aspx?Group=RTE-ENG-RW&Operation=join)**

Please note: All members of the Research Technology Engineering team have Read Only access to the subscriptions listed below using their corporate credentials via the **[RTE-ALL-RO](https://idwebelements/GroupManagement.aspx?Group=RTE-ALL-RO&Operation=join)** security group.

##GCR
|Subscription Name| Subscription ID |IDWEB Security Group| Purpose|
|--|--|--|--|
| GCR Hadoop Subscription |75f42565-7909-4fe6-932a-a574105dffa0| RTE-GCR-RW | Hadoop Production GCR |
| Grand Central Resources Production | fade1c90-3738-444a-874a-0d0005fb376d |RTE-GCR-RW| Production GCR |
| GCRProdEx1 |7ccdb8ae-4daf-4f0f-8019-e80665eb00d2| RTE-GCR-RW | Production GCR |
| Grand Central Resources Production 2 |40641f8d-33f8-4948-b0ae-3df7e85e94e9|RTE-GCR-RW| Production GCR |
|GCR Prod Europe  | cdc34588-3faf-48be-bf23-f91de2fdbc53| RTE-GCR-RW | GCR Europe |
| GCR Team Drive |8a6181dc-340c-4f49-9566-385a9ce80b39  | RTE-GCR-RW | Team Drive project |
|AI Platform GPU 37 - MSR  | db9fc1d1-b44e-45a8-902d-8c766c255568 |  RTE-GCR-RW| GPU Hypercluster |
|GCR Dev-Test|d8cfeb0b-7ef3-48db-9f78-fd34cf307d3b|RTE-GCR-RW|For GCR testing only|


##RTE Engineering
|Subscription Name| Subscription ID |IDWEB Security Group|Purpose|
|--|--|--|--|
|AIREng Service Tree Integration Testing  | 78a6ff9d-faa3-4a8e-80c9-1d30049625d1 | RTE-ENG-RW |Used for Service Tree and related testing scenarios|
|  AzSecPack Testing Two | 12ca06db-e309-4816-824e-48d5817de3ca | RTE-ENG-RW |Used for AzSecPack testing and development|
|  AzSecPack Testing Three | 0a94b383-2743-4577-b231-801ff887989f | RTE-ENG-RW |Used for AzSecPack testing and development|
| TnR Engineering External test account | a5224fa9-985e-4c4a-9636-738af9bc5e82 |  RTE-ENG-RW|Used for general testing of azure services|
| AIRCHEF  |41b1c73f-b85c-4a0b-a735-8df6648353b7  | RTE-ENG-RW |Used for divisional Chef server and artifacts, key rotation|
|  MSRSupp_CorpNet_Resources | e82dbbc9-6196-4755-8bbb-9ce911a2072c | RTE-ENG-RW & RTE-GCR-RW  |General sandbox subscription to test out Azure services. Subscription is Express Route enabled in WUS2 |
|   MSR Central Corpnet Resources| 4bea013c-d8f3-41a0-97e0-e448ba6bee8a | RTE-ENG-RW | Used by MSR Central team. Not for RTE use |
| AIR Core Platform Infrastructure  | 0561c8bc-9b6c-4951-a151-f946b9e72049 | RTE-ENG-RW |Intended for 'production' related infrastructure services - Express Route Enabled in WUS2|
| Spare Subscription 1 |  736a7445-44fd-4aa4-ae9d-c9d91a97dd6f|RTE-ENG-RW  | Available for project use. Rename before using |
|  Spare Subscription 2	 | 8f192c3e-20a5-4b38-85d8-aceb7fcd74b6 | RTE-ENG-RW |Available for project use. Rename before using |
|  AIRSYS Testing Subscription	|  5491fd1d-3d0a-4ea4-83d1-7e0f3a375a69| RTE-ENG-RW | For use by AIRSYS PM only |
|  Microsoft Research Engineering | 7bdcf9ec-4326-408b-a69b-c7235c63b5e8 | RTE-ENG-RW | Actively used but we don't know who or why |
|  AIR Geneva | abbe90e4-9474-4949-9a39-523530af925e | RTE-ENG-RW |Used for AzSecPack testing and development |
|  MSR GDPR Production | f987903a-7c27-489d-8b59-eb187b7fc04e | RTE-ENG-RW | Under review for potential deprecation|
|  MSR GDPR Development | ff1c8e3d-7cc5-4f02-a3e1-0d58b4e7ad19 |  RTE-ENG-RW|Under review for potential deprecation|
|  AIRENG-AME-Resources |  4640eca2-d351-47c9-acfc-924f8a96d5b9|  RTE-ENG-RW| Testing for AME environment only |
|  Katie Test |e1baa2c9-ba10-470b-ab7b-8369fdbe1b0c  | RTE-ENG-RW | Testing Only. Not for use by anyone else |
|  Katie Test Sub 2 | d7925fdb-d6aa-4f15-bad2-bc6650e7402e |RTE-ENG-RW  | Testing Only. Not for use by anyone else |
| TempHolding-Policy-Canary | 8b1ab931-f6a8-4ecc-a281-893ef3a69d52 |  RTE-ENG-RW |Azure Governance Testing Only |
| Nested-NonProd-Policy-Canary | 006f942d-905d-466a-a07b-a3276a50b33b |  RTE-ENG-RW| Azure Governance Testing Only |
| NonProd-Policy-Canary |8c233970-db59-4363-b061-aa11a5411464  | RTE-ENG-RW |Azure Governance Testing Only |
|Nested-Prod-Policy-Canary  | 11464697-15de-4e02-98c7-490f037b1584 |RTE-ENG-RW  |Azure Governance Testing Only |
| Prod-Policy-Canary | f369393e-b64b-4ead-82cb-e4b4709bca09 | RTE-ENG-RW | Azure Governance Testing Only |
| RTE-GPU (Azure Management Group) |  | MSR-GPUMig-SCALT & MSR-GPUMig-RO | AMG for MSR subs migrated to RTE |
|  |  |  |  |
|  |  |  |  |

##Sesame
|Subscription Name| Subscription ID |IDWEB Security Group|Purpose|
|--|--|--|--|
|[Sesame GCR](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/923239b9-27ca-40bb-9868-3932f1fb42a2/overview)|923239b9-27ca-40bb-9868-3932f1fb42a2|RTE-SESAME-RW|Hosts Services for the GCR program
|[Sesame Dev/Test](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/0d83bec5-5c98-45a6-a26a-a754a03afcae/overview)|0d83bec5-5c98-45a6-a26a-a754a03afcae|RTE-SESAME-RW|Used by Sesame team for development, testing, and exploration of Azure solutions

The following subscriptions do not have centralized access control. Please work with the subscription owners for access

##LOB Tools Dev Team
|Subscription Name| Subscription ID |Contact|
|--|--|--|
| Centerstage | f732445c-e086-4f7d-acb3-e1852ea9989a |Matej Ciesko|
|  MSRN Dev Core Subscription| e5a3e210-7397-49c2-ba9a-d75d63c08a96 | Matej Ciesko|
| Intern Tool | e0e314e5-e68f-45da-9cf5-a404608fd680 | Matej Ciesko|
| TnR Shared Services | b283975d-64d3-4070-8693-b90f0137424f |  Matej Ciesko|
| Release Tracker Production | ca0e97dc-451e-45c7-9364-44c5b67fc758 | Matej Ciesko|
| Resnet | 277f3171-565d-4a1e-9f32-fd74153aafba | Matej Ciesko|
| Space Tool | 8b501d37-f25e-445a-b5d7-32082bd3adea | Matej Ciesko|
| MYAccess | 3985ec10-4599-4a9a-b503-d554bfdd9853 | Matej Ciesko|
| TnR Shared Services |b283975d-64d3-4070-8693-b90f0137424f  |Matej Ciesko|
