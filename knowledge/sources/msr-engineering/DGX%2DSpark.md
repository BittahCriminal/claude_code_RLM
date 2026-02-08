[[_TOSP_]]
[[_TOC_]]
### ✅ **What is NVIDIA DGX-Spark?** https://aka.ms/DGXSpark - This page

*   **Purpose:** A compact, power-efficient AI system for prototyping, fine-tuning, and inference of large reasoning models. 
*   **Key Specs:**
    *   **Processor:** NVIDIA GB10 Grace Blackwell Superchip
    *   **Performance:** 1 petaFLOP of AI compute
    *   **Memory:** 128 GB
    *   **Software:** NVIDIA AI stack preinstalled
*   **Use Case:** Run models from DeepSeek, Meta, NVIDIA, Google, Qwen, etc., up to **200B parameters locally**.

### 🔧 **Post-Manufacturing Firmware Updates**

Run these commands after initial setup to ensure your DGX-Spark is up to date:
```
sudo apt update  
sudo apt dist-upgrade  
sudo fwupdmgr refresh  
sudo fwupdmgr upgrade  
#sudo reboot now  
```
**Reference:** https://docs.nvidia.com/dgx/dgx-spark/os-and-component-update.html

### 📚 **Helpful Links**

*   http://www.nvidia.com/DGX-Spark - Home Page
*   https://www.nvidia.com/en-us/support/dgx-spark - NVIDIA DGX Spark Support
*   https://docs.nvidia.com/dgx/dgx-spark - User Guide
*   https://docs.nvidia.com/dgx/dgx-os-7-user-guide/initial_setup.html#first-boot-process-for-dgx-servers - 1st boot experience for DGX-Spark OS7.
*   https://forums.developer.nvidia.com/c/accelerated-computing/dgx-spark-gb10 - User Forum
*   https://www.amax.com/5-things-you-need-to-know-about-nvidia-dgx-spark - Distributor Blog
*   https://aka.ms/LinuxDesktop - _still working_ with Intune & Edge teams to release ARM based support.

### 💻 **Reimaging DGX-Spark for LinuxDesktop**

1.  **Get ISO:**  
    `\\msr-data\software\drivers\nvidia\DGX\DGXBaseImageISO`
       - DGXOS-7.3.1-2025-11-12-09-12-21-arm64.iso
2.  **Create Bootable USB:** Use **Rufus**.  Times:  10 minutes to copy from share to local,  20-40 minutes to create the USB Stick and 45 minutes to image the Spark.
3.  **Boot Process:**
    *   Power on DGX-Spark.
    *   Select **Delete within 10 seconds** → Setup Menu.
    *   Choose **USB Hard Drive** to start reimage.
4.  **Passphrase:** Found in https://docs.nvidia.com/dgx/dgx-os-7-user-guide/initial_setup.html#first-boot-process-for-dgx-servers.
5.  **TPM & Unlock:** First change you encrypted passphrase `sudo cryptsetup luksChangeKey /dev/nvme0n1p3`, then use [Using TPM with Ubuntu+Clevis - Overview](https://dev.azure.com/linux-at-microsoft/one/_wiki/wikis/Linux%20Desktop/14/Using-TPM-with-Ubuntu-Clevis)[.pdf(if permissions issue)](/.attachments/Using%20TPM%20with%20Ubuntu+Clevis-c8e4aa51-c066-40d1-abf8-c82fa306d740.pdf) for a similar bitlocker experience on Windows.  You need to clear TPM(3rd gray section), then install Clevis and configure TPM(4th gray section).  This is critital if you run the Spark in headless mode.

![image.png](/.attachments/image-78dff980-52d9-4ab5-bdf0-ac0ba7e1214d.png)
![image.png](/.attachments/image-1efdcc1b-9840-4ae3-a799-2bb5789bb967.png)
![image.png](/.attachments/image-8b935199-bc1a-40dc-81da-09fe1f5ed765.png)
![image.png](/.attachments/image-0bf7b8b1-4661-4dee-8832-ad6619362786.png)
![==image_0==.png](/.attachments/==image_0==-5e8efe33-243b-45a7-8ca7-ec827b38dc28.png)
