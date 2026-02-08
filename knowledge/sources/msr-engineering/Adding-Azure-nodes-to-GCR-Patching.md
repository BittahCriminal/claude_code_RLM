This article explains how to add Azure VM's into GCR azure patch management.

## Remove OMS extension

For onboarding AUM for VMs, first go to VM and then click on Extensions if there is any existing extension for OMS-agent opr anything says monitoring first uninstall it 

![APM1.jpg](/.attachments/APM1-6ef28afa-7372-45bc-9fa0-99a9ab280907.jpg)

## Enable Update Management

Once done go to Guest + host updates down below under Operations and enable it by clicking on enable make sure the below details are met 

![APM2.jpg](/.attachments/APM2-6d3f77a8-0520-4f84-8d70-2be846c1a4aa.jpg)

Once onboarded, you can go to AUM under update management and search the host it show show up there

![APM3.jpg](/.attachments/APM3-a8a8fc8c-019e-423f-b937-eb4466f27f8f.jpg)
