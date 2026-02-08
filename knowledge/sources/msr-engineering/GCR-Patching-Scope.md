**Note: Please do NOT edit this page before contacting the service owners Omid Balouchi or Kris Zentner with any changes.**

The nodes in scope for GCR patching are categorized based on their environment and subscription:

**Azure GPU Linux VMs (GCRprodex2 subscription):**

- **RG**: GPU-SANDBOX, GPU-SANDBOX2, and GPU-SANDBOX3
- GCRAZGDL1XXX
- GCRAZGDL3XXX
- GCRAZGDL4XXX

**Azure CPU Linux VMs (GCRprodex1 subscription):**

- **RG**: CPU-Sandbox
- GCRAZCDLXXX

**On-prem GCRSANDBOXES - GCR-Arc subscription:**

**Linux** 
- **RG**: GPU-SANDBOX 
- GCR-SANDBOX-[001-011,013,017-022]
- MSR-SANDBOX-046
- GCRSANDBOX[101-193]
- GCRSANDBOX[300-544]

**B200 jumpbox VMs - GCRProdex1 subscription** 

RG: CPU-Sandbox

- [msrne-bio01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msrne-bio01)
[msri-reform01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msri-reform01)
[msrhf-dximaging01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msrhf-dximaging01)
[msremea-nextgen01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msremea-nextgen01)
[msraif-shared01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-SANDBOX/providers/Microsoft.Compute/virtualMachines/MSRAIF-SHARED01)
[msrai4s-shared01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msrai4s-shared01)
[msra-daai01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msra-daai01)
[msr-redmond01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msr-redmond01)
[msr-accelerator01](https://ms.portal.azure.com/#resource/subscriptions/7ccdb8ae-4daf-4f0f-8019-e80665eb00d2/resourceGroups/CPU-Sandbox/providers/Microsoft.Compute/virtualMachines/msr-accelerator01)



**Windows**
- **RG**: GPU-SANDBOX
- GCRSANDBOX393, GCRSANDBOX394, GCRSANDBOX421

**Out of scope**

- None