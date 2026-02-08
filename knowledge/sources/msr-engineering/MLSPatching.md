
https://aka.ms/mls/patching - This page 



[[_TOC_]]

# **Customer Patching Responsibilities and Objectives**
- Identify assets that should be patched
- MLS tool training
- How to opt into patching service
- How to perform an exception (postpone patch)
- Host machine Patch Readiness identification
- Windows vs Linux

**[Patching Dashboard](https://msit.powerbi.com/groups/me/reports/f8e2a637-7d60-4bc0-8358-c9c921aac786/ReportSectione2a31be271508d695ec7?experience=power-bi&bookmarkGuid=a7ee916f-15c2-403c-9444-66a8e491751f)** (shows both Linux & Windows compliance) - [Need Access?](https://microsoftit.visualstudio.com/DefaultCollection/OneITVSO/_wiki/wikis/OneITVSO.wiki/12879/MsD-Patching-Wiki)

## **Compliance Definitions**
- **Compliant**
Systems are fully patched(Ubuntu or Windows, IE, Edge, Chrome .Net, Java, SQL, Visual Studio)
- **Non-Compliant**
Systems are missing patches.
- **Schedules** - GCR Patch Monday(6am-5pm) - Division - Saturday(5am-1pm) / after Microsoft Patch Tuesday

GCR 2nd Patch Tuesday(6am-5pm) - Division - Saturday(5am-1pm) / after Microsoft Patch Tuesday

**Opt-In**
Instructions - https://aka.ms/MLSPatchingWiki
Linux/Windows SelfService Portal - https://aka.ms/mlspatchingservice 

**Linux**
Instructions - https://microsoftit.visualstudio.com/OneITVSO/_wiki/wikis/OneITVSO.wiki/29285/Opt-in-Linux-Patching-Service - Key is setting [attributes](https://microsoftit.visualstudio.com/OneITVSO/_wiki/wikis/OneITVSO.wiki/29139/Linux-Patching-Prerequisites-OneAsset-attributes)

**IcM Ticketing for MLSPatching Team**
https://portal.microsofticm.com/imp/v3/incidents/create?tmpl=c3Mt12
**MLSPatching Bug Portal**
https://microsoftit.visualstudio.com/OneITVSO/_dashboards/dashboard/d78ec657-d34f-4582-9dc0-c1575ffdd457

## **Common Patching Failures and remediation**
DNS registration failure or System Name Change
Invalid System Type in [OneAsset](https://oneasset.microsoft.com/)(such as Network Switch, Rack, Storage, PDU) classified as Server Device.
Systems in wrong OU ([Move OU](https://microsoft.service-now.com/mls?id=sc_cat_item&sys_id=73f399351316e6009317b1e32244b045))

## **Query Tools**
```
**Redmond**
#Port Scanner(this helps discover why nodes are not reachable?  Are they Windows(Port 3389) or Linux(Port 22) or fail DNS
Install-Module -Name PSnmap
$Servers = GC c:\temp\99.4349Servers.txt
Invoke-PSnmap -ComputerName $Servers -Port 22,3389 -PortConnectTimeoutMs 2000 -ScanOnPingFail | ft -a

#ADFinder(Are systems in the right OU for MLSPatching, Permissions, Qualys Agent)
$Servers = GC c:\temp\99.4349Servers.txt
$Output = foreach ($Server in $Servers ) {
Get-ADComputer -filter "Name -eq '$Server'" -Server "corp.microsoft.com:3268" | Select-Object Name, DistinguishedName 
}
$Output | Out-GridView

**Beijing Version**
#Port Scanner(this helps discover why nodes are not reachable?  Are they Windows(Port 3389) or Linux(Port 22) or fail DNS
Install-Module -Name PSnmap
$Servers = GC c:\temp\BeijingServers.txt
Invoke-PSnmap -ComputerName $Servers -Port 22,3389 -PortConnectTimeoutMs 2000 -ScanOnPingFail | ft -a

#ADFinder(Are systems in the right OU for MLSPatching, Permissions, Qualys Agent)
$Servers = GC c:\temp\BeijingServers.txt
$Output = foreach ($Server in $Servers ) {
Get-ADComputer -filter "Name -eq '$Server'" -Server "corp.microsoft.com:3268" | Select-Object Name, DistinguishedName 
}
$Output | Out-GridView
```
![image.png](/.attachments/image-9d413cd5-f355-4093-bdb8-3d46b79ac4fb.png)


