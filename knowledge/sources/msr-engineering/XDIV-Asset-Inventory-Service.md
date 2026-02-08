

#XDIV Asset Inventory Service
XDIV is an asset inventory service that is consolidating all system information for Microsoft internal assets. It covers both Azure and on-premise assets. This team was formed in response to events like WannaCry, Spectre, and Meltdown when Microsoft needed to rapidly identify and mitigate the impacted systems and our disorganized asset tracking caused many delays and false positives.

Existing asset systems like OneAsset are consumed by the XDIV service to provide a single source of asset identification. The complete list of 38 sources are on the wiki linked below. Please take time to become familiar with this service and get permissions to the reporting in case you need it in the future.

•[XDIV Wiki](https://osgwiki.com/wiki/XDiv) – wiki plus Kusto query information
•[XDIV PowerBI](http://aka.ms/xdiv) - Asset information. Permission must be requested to access.

-----------------------
Here are the XDiv sources and counts per source as of November 2019

Execute: [Web] [Desktop] [Web (Lens)] [Desktop (SAW)] https://conflux.kusto.windows.net/XDiv 
XDiv_Source
| summarize Ct=count() by DataSource


|  Source| Count |  
|--|--|
|AZUREGRAPH.INTERNAL.RAW.LOGICALCOMPUTE.VIRTUALMACHINEV	|4602202|
|CDG_ARCSIGHT|567059|
|CDG_AZURE_ENDPOINTSRANGE|1905720|
|CDG_MASTERDATA|3409|
|CDG_PX_NIX|6768|
|CDG_PX_WIN|889156|
|CDG_TVM|171571|
|CDG_TVM_SCANNER|606|
|CDGSEC_AD|1813071|
|CDGSEC_ATP|69535|
|CDGSEC_AWS|1921|
|CDGSEC_AZURE	|4400086|
|CDGSEC_CONFLUX	|601227|
|CFLXPRISM_GBL_PAT_MACHINES|10637679|
|CONFLUX_IP_ACTIVEDIRECTORY|237906|
|CONFLUX_IP_APGOLD|4122|
|CONFLUX_IP_APGOLDV2|68804|
|CONFLUX_IP_ARCSIGHTLIVEHOSTLIST|148479|
|CONFLUX_IP_AZURE_ARM_IAAS|94020|
|CONFLUX_IP_MASTERDATA|2603|
|CONFLUX_IP_MIXERINVENTORY|1471|
|CONFLUX_IP_TVMQUALYS|88089|
|CONFLUX_IP_UST_PAT_MACHINES|101499|
|CONFLUX_IP_UST_PAT_NETWORKDEVICES|1624|
|CONFLUX_IP_WDGNETDEVICE|1237|
|CSEO_SIGNAL|748353|
|LINKEDIN|165533|
|MICROSOFT.CLOUD.AZNWNETMON_AZNWMDSDEVICESTATIC	|3551111|
|MICROSOFT.CLOUD.AZURESLAMCOVERAGEHEALTHDETAILV1|4368695|
|MICROSOFT.CLOUD.CEINVENTORY.MAIN.AUTOPILOT|814311|
|MICROSOFT.CLOUD.CEINVENTORY.MAIN.BAREMETAL|679716|
|MICROSOFT.CLOUD.CEINVENTORY.MAIN.HOST|	1691262|
|MICROSOFT.CLOUD.CEINVENTORY.MAIN.INFRAGUEST|4478513|
|MICROSOFT.CLOUD.CEINVENTORY.MAIN.NATIVE|441689|
|MICROSOFT.CLOUD.CEINVENTORY.MAIN.PILOTFISH|2869705|
|MICROSOFT.CLOUD.SSEVULNERABILITYMANAGEMENT_DETAILOFFNODE_V01|	7101513|
|ONEASSETVEGA|	9020530|
|ONEASSETVEGAV3|8653760|
|OPG|1013333|
|TWCNSALLFEEDS.PROD.CORPNET.WEF.LOGON|	174029|
|TWCNSALLFEEDS.PROD.IPTOHOSTNAME|345155|
|UNIVERSE|1682935|
|US PRISM|210108|
|WDGIS TELEMETRY|3134816|
|WINES PRISM|676906|
