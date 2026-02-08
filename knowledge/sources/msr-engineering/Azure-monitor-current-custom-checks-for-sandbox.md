List of current custom checks for Azure monitor for sandbox:
*   **check_gpumetrics** : This check runs on both Azure and onprem on GPU nodes to make sure the GPUmetric service is running.

*   **check_gpu** : This check runs on both Azure and GCR onprem and its job to detect GPU failures such as missing nvidia driver, missing GPU , pending black list , etc.
*   **check_nvsm**: This check runs  on GCR Onprem and is specific to DGX stations it runs the nvsm-health a built in Nvidia tool to detect failure for DGX systems.
*   **check_gpu_amd**: This checks runs  on GCR AMD GPUs such as GCR-openpai-XX systems and its job is to detect AMD GPU failure such as missing driver , missing GPUs mismatch version etc
*   **check_ansible_status**: this check runs  on all nodes managed by Ansible and its job is to detect ansible run failure.
*   **check_amax**: This check runs  on GCRSANDBOX3XX 4XX and 5XX series or any AMAX system and its job is to detect hardware failure on AMAX systems.
*   **check_disk_usage**: This check runs on all GCR Azure and Onprem and alert if the OS disk has 6 GB or less available space. **Warning** **If you receive this alert don't delete customer data blindly to make space always check with customer and ask them to delete unused data first.**
*   **check_pkg_repo**: This check runs  on both Azure and GCR onprem and its job is to detect ubuntu broken package repository.
* **check_disk_partition**: This checks runs both on Azure and Onprem and make sure the disk is mounted this check assumes the following details and only works based on below details: ( **disk check is currently disabled until the GCR arc hosts has consistency with all their drive** )

- [ ]    GCRSANDBOX1XX have 4 sd disks and look for sd type disk in the script
- [ ]   GCRSANDBOX2XX have 5 sd disk and look for sd type disk in the script
- [ ]   GCRSANDBOX3-5XX have 2 nvme and 2 sd disk so script looks for both nvme and sd
- [ ]  GCRAZGDLXXX has 1 nvme disk that script looks for.