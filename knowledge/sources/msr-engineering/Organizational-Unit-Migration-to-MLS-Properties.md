<H1>Updated Active Directory Structure - Worldwide</H1>

DSRE has tasked MLS with sunsetting the "Labs" OU structure in Active Directory. They have also made MLS accountable for server compliance for all "lab" machines, which includes much of the infrastructure in the Legacy MSR OUs (Research-xx in each global corp domain where we have MSR assets, where the "xx" is replaced by a site designation, NE, NY, UK, SVC, MTL, etc).

For this project we're addressing each domain and site separately to ensure that the needs of our business are met first, then the needs of MLS and DSRE are addressed within our business needs.

As of **November 2019**, the status is:
**================================================================================**
**Domain:  Redmond**
**Old OU Root:**  Redmond\Research-RED
**New OU Root:**  Redmond\MLS\NoSync\MSR

Migration of computer accounts to new structure is under way.

There are 3 sub OUs under the new root:
**MSR_Exception
MSR_Infrastructure
MSR_Projects**

**MSR_Exceptions** is only intended to be used for short term needs (of which there aren't currently any) when a project requires the quick addition of Active Directory objects, but none of the existing containers meet the exact need.

**MSR_Infrastructure** is intended to hold all of the computer objects that are owned/managed by the RTE team in the Redmond domain.  This includes all Active Directory joined/affiliated GCR assets, in the "GCR" sub OU.  Other sub OUs may be created in the future, but no current needs for other separate sub OUs have been identified.

**MSR_Projects** is intended for use by Research groups with large sets of computer accounts that should not be placed in the corporate "workstations" OU, nor directly co-managed by MLS and that team, but should be owned/maintained by the RTE Engineering and/or Operations teams.  This generally will require some formal agreement between RTE and the owning team to outline support requirements and obligations.

**================================================================================**
**Domain:  NorthAmerica**
**Old OU Root:**  NorthAmerica\Research-MTL
**New OU Root:**  NorthAmerica\MLS\NoSync\MSR
**Old OU Root:**  NorthAmerica\Research-NE
**New OU Root:**  NorthAmerica\MLS\NoSync\MSR
**Old OU Root:**  NorthAmerica\Research-NY
**New OU Root:**  NorthAmerica\MLS\NoSync\MSR

Migration of computer accounts to the new structure is under way, and nearly complete.

There are no sub OUs under each site OU, as the infrastructure and project requirements for all three current NorthAmerica sites are small and do not call for separate policies/permissions to be applied at the site level.

**================================================================================**
**Domain:  Europe**
**Old OU Root:**  Europe\Research-UK
**New OU Root:**  Europe\MLS\NoSync\MSR

Migration of computer accounts to new structure is under way.

There are 3 sub OUs under the new root:
**Exception
Infrastructure
Projects**

**Exception** is only intended to be used for short term needs (of which there aren't currently any) when a project requires the quick addition of Active Directory objects, but none of the existing containers meet the exact need.

**Infrastructure** is intended to hold all of the computer objects that are owned/managed by the UK engineering and operations team.  No current needs for separate sub OUs have been identified.

**Projects** is intended for use by Research groups with sets of computer accounts that should not be placed in the corporate "workstations" OU, nor directly co-managed by MLS and that team, but should be owned/maintained by the UK Engineering and/or Operations teams.  

**================================================================================**
**Domain:  FarEast**
**Old OU Root:**  FarEast\Research-IN
**New OU Root:**  FarEast\MLS\NoSync\MSR\India
**Old OU Root:**  FarEast\Research-CN
**New OU Root:**  FarEast\MLS\NoSync\MSR\China

Migration of computer accounts to new structure is under way.
There is currently 1 sub OUs under the new **India root**:
**MSR_Infrastructure**

**MSR_Infrastructure** is intended to hold all of the computer objects that are owned/managed by the India team in the FarEast domain.  No current needs for separate sub OUs have been identified.

The engineering team in China is currently mapping out their existing OU structure and identifying the business requirements for the new MLS root structure.  

**================================================================================**
