

#Overview of AI+R Divisional Distribution Group and Secure Group design.
AI+R currently uses automatically maintained DGs (referred to as "Auto Group" in the table below) that are managed via IDWEB (also called FIM).  We also have manually maintained DGs in IDWEB that are sometimes used to collect the "All" groups of both FTE and NonFTE.  These are also listed in the table below.  With these DGs, one can reach all FTEs reporting to a top level manager, all NonFTEs reporting to that manager, or every reporting to that top level manager.  In addition to the Auto and Manual DGs, we maintain Secure Groups (SGs) with their membership based off of the "Auto" DGs from IDWEB.  The information flow for these groups runs like this:
Employee information is updated in HeadTrax (and/or other HR tools), IDWEB scans the changes in the HR tools to re-populate the "Auto" DGs, Our internal tooling (hosted on MSR-SCRIPT) runs (at least) ever hour to synchronize changes in the DGs to the SGs (which we "own" directly in Active Directory - not in IDWEB).

|**Top Level Leader**|**Leader Alias**|**FTE Auto Group Name**|**FTE Auto Group Alias**|**NonFTE Auto Group Name**|**NonFTE Auto Group Alias**|**"All" Manual Group Name**|**"All" Manual Group Alias**|**FTE SG**|**NonFTE SG**|**Notes**|
|--|--|--|--|--|--|--|--|--|--|--|
|Kevin Scott|KvnScott|Kevin Scott's Organizaion (FTE)|KvnScott_org_fte|Kevin Scott's Organization (NonFTE)|KvnScott_org_nonfte|Kevin Scott's Organization (ALL)|KvnScott_org_all|TBD|TBD||
|Peter Lee|PeteLee|Peter Lee (MSR)'s Organization (FTE)|PeteLee_org_fte|Peter Lee(MSR)'s Organization (NonFTE)|PeteLee_org_nonfte|Peter Lee (MSR)'s Organization (ALL)|PeteLee_org_all|TBD|TBD||
|Michael Schwarz|MSchwarz|Michael Schwarz's Orgnaization (FTE)|MSchwarz_org_fte|Michael Schwarz's Orgnaization (NonFTE)|MSchwarz_org_nonfte|Michael Schwarz's Orgnaization (ALL)|MSchwarz_org_all|TBD|TBD||
|Vijay Mital|VijayMi|Vijay Mital's Organization (FTE)|VijayMi_org_fte|Vijay Mital's Organization (NonFTE)|VijayMi_org_nonfte|Vijay Mital's Organization (All)|VijayMi_org_all|TBD|TBD||
|Gurdeep Paul|Gurdeep|Gurdeep Paul's Organization (FTE)|Gurdeep_org_fte|Gurdeep Paul's Organization (NonFTE)|Gurdeep_org_nonfte|Gurdeep Paul's Organization (ALL)|Gurdeep_org_all|TBD|TBD||


#Technical Details for the DG to SG Sync serice:
|Script Name|From Group(s)|To Group(s)|Business Owner|Notes|
|--|--|--|--|--|
|02_KvnScott_org_fte___to___TnR_FTE_SG.ps1|KvnScott_org_fte|TnR_FTE_SG|Jennifer Janzen||
|03_KvnScott_org_nonfte___to___TnR_Non-FTE_SG.ps1|KvnScott_org_nonfte|TnR_Non-FTE_SG|Jennifer Janzen||
|04_redmondlab_fte___to___TnR_MSR_RED_FTE_SG.ps1|petelee_org_fte|TnR_MSR_RED_FTE_SG|Katy Halliday||
|05_petelee_org_fte___to___TnR_NeXT_FTE_SG.ps1|petelee_org_fte|TnR_NeXT_FTE_SG|Katy Halliday||
|07_petelee_org_fte___to___MSR_Labs_FTE_SG.ps1|petelee_org_fte|MSR_Labs_FTE_SG|Katy Halliday||
|08_petelee_org_fte___to___MSR_FTE.ps1|petelee_org_fte|MSR FTE|Katy Halliday||
|09_petelee_org_nonfte___to___MSR-NonFTE.ps1|petelee_org_nonfte|MSR NonFTE|Katy Halliday||
|13_desney_org_nonfte__to__CliniSeAn-nonFTE.ps1|desney_org_nonfte|CliniSeAn-nonFTE|Desney Tan||	
|15_CmBishop_org_all___to___USG-MSRCALL_SG.ps1|CmBishop_org_all|USG-MSRCALL|Nathan Jones||
|17_DonaldK_org_fte__to__MSR_Redmond_Lab_FTE_SG.ps1|DonaldK_org_fte|MSR Redmond Lab FTE SG|Sierra Mulkin||
|18_PeteLee_org_all__to__MSR_Labs_All_SG.ps1|petelee_org_all|MSR_Labs_All_SG|Katy Halliday||
|18_DonaldK_org_all__to__MSR_Redmond_Lab_All_SG.ps1|DonaldK_org_all|MSR Redmond Lab All SG|Sierra Mulkin||
|3DTeleMedBetavTeam__to__3DTeleMedBetavTeam_SG.ps1|3DTeleMedBetavTeam|3DTeleMedBetavTeam_SG|Spencer Fowers| ||
|johannes_org_fte-TO-johannes_org_fte_SG.ps1|johannes_org_fte|johannes_org_fte_SG|Stacy Grover| ||
|KMAll_to_KMAll_SG.ps1|KMALL|KMALL_SG|Kendall Martin | ||
|KMFull_to_KMFull_SG.ps1|KMFULL|KMFULL_SG|Kendall Martin| ||
|MSR-Green_to_MSR-Green_SG.ps1|MSR-Green|MSR-Green_SG|Trevor Eberl| ||
|MsrTech_to_MSR-DHCP.ps1|MsrTech|MSR-DHCP|Mike Shepperd| ||
|sblyth_org_fte-TO-sblyth_org_fte_SG.ps1|sblyth_org_fte|sblyth_org_fte_SG|Roy Zimmerman| ||
|tnr_org_us_fte___to___TnR_ORG_US_FTE_SG.ps1|tnr_org_us_fte|tnr_org_us_fte_SG|Jennifer Janzen| ||

Each individual script runs as a scheduled task on MSR-SCRIPT each morning, under the “Redmond\TnRMon” account.  The scripts are located in the “C:\Scripts\GroupSync” folder, and only active scripts live in that root folder.  All other files/notes/retired scripts live in the “Misc” folder inside “GroupSync”.

# Source Code Repository: 
https://dev.azure.com/msresearch/MSR%20Engineering/_git/MSR%20Engineering?path=%2FResearchEngineeringTools%2FGroupSync&version=GBmaster
 
# Background
IDWEB supports "Manager Based Distribution Groups" for FTEs and NonFTEs, which effectively capture everyone who rolls up to the specified manager.  Unfortunately, the technology used in IDWEB does not (effectively) support "Manager Based Secure Groups" at Microsoft, because of our multi-domain, multi-forest, Active Directory architecture.  

In order to fill the gap in the available IDWEB automation tooling, the Research Technology Engineering (RTE) team manages and supports a set of automation tooling that synchronizes Secure Group membership, based on IDWEB Distribution Groups.  For example, if a manager, Barbara Smith, needs to set permissions to a Sharepoint site for her team, she might have (or have the RTE team create) a pair of Manager Based DGs in IDWEB for her FTEs and her NonFTEs.  The RTE team can use the members of those two DGs to create a single, flat (no nested groups) Secure Group which can be used to apply permissions to Sharepoint (or other corporate tools and platforms).

The only other way to accomplish this is by someone on the manager's team manually updating a flat Secure Group in IDWEB every time team membership changes.  This manual process tends to be cumbersome, and the process is often lost or forgotten with staff changes and reorganizations.  At that point, the permissions are often in a mixed or unknown state with people who need access not having it, and people who should no longer have access still having it.

# Lifecycle management of DLs
In the lifecycle management of DLs you'll often find the need to setup an auto response to notify users of service status. This can be a deprecation of the service or a new interface for support. To do this internally you'll need to create a service account and create an auto response. RTE Engineering maintains an account to help facilitate this. The account is **TnRRedir** and instructions on how to configure this can be found [HERE](https://microsoft.sharepoint.com/sites/Identity_Authentication/SitePages/IDWeb/Add-Remove-Modify-Auto-Reply-for-a-Distribution-Group.aspx). You will need to be an account owner to modify the auto-response.
