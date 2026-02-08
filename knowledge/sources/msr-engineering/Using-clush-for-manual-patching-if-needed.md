In case manual patching is needed these below clush commands can be used based on VMs location. Please never use clush during off maintenance GCR window and always double check what your clush commands does as it can break things easily. 

**Westus2 nodes**

`clush -w GCRAZGDL[3101-3200].westus2.cloudapp.azure.com "sudo apt-get update && sudo apt-get upgrade -y && sudo reboot"`
 
**Westus3 nodes**

`clush -w GCRAZGDL[1400-1768,3001-3068,4001-4048].westus3.cloudapp.azure.com "sudo apt-get update && sudo apt-get upgrade -y && sudo reboot"`
 

**Northcentralus**

`clush -w GCRAZGDL[1116-1215].northcentralus.cloudapp.azure.com "sudo apt-get update && sudo apt-get upgrade -y && sudo reboot"`

For Onprem nodes:

`clush -w gcrsandbox[101-133,205-207,212-246,267-286,300-543].redmond.corp.microsoft.com "sudo apt update && sudo apt upgrade -y && sudo reboot"`