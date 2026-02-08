### ✅ **What You Need**

*   **Rufus**: Download from [rufus.ie](https://rufus.ie/en/) (portable or installer version).
*   **ISO file**: The operating system image you want to install (Windows, Linux, etc.).
*   **USB drive**: At least 8 GB (larger for modern OS images).
*   A **Windows PC** (Rufus runs on Windows).

* * *

### 🔍 **Steps to Create a Bootable USB with Rufus**

1.  **Download and Launch Rufus**
    *   Go to [rufus.ie](https://rufus.ie/en/) and download the latest version.
    *   No installation required for the portable version—just run the `.exe` file. [[rufus.ie]](https://rufus.ie/en/)
2.  **Insert Your USB Drive**
    *   Plug in the USB stick you want to use.
    *   **Important:** Back up any data on it—Rufus will erase everything. [[wikihow.com]](https://www.wikihow.com/Use-Rufus)
3.  **Select the Device**
    *   In Rufus, your USB drive should appear under **Device**.
    *   If multiple drives are connected, choose the correct one. [[easytechsolver.com]](https://easytechsolver.com/how-to-create-a-bootable-usb-with-rufus/)
4.  **Choose the ISO File**
    *   Click **SELECT** and browse to your ISO file.
    *   Rufus will auto-detect the image and suggest settings. [[techbloat.com]](https://www.techbloat.com/how-to-create-bootable-usb-from-iso-file-using-rufus.html)
5.  **Configure Settings**
    *   **Partition Scheme**:
        *   **UEFI systems** → GPT
        *   **Legacy BIOS** → MBR
    *   **File System**:
        *   FAT32 for UEFI boot (required for Windows install on UEFI).
        *   NTFS if ISO is larger than 4 GB (Rufus will handle splitting if needed). [[additional...rosoft Q&A | Learn.Microsoft.com]](https://learn.microsoft.com/en-us/answers/questions/5551481/additional-steps-for-creating-a-bootable-usb-from)
    *   Leave cluster size as default.
6.  **Start the Process**
    *   Click **START**.
    *   Confirm warnings about data loss.
    *   Rufus will format the USB and copy the ISO contents. [[[Article]...rosoft Q&A | Learn.Microsoft.com]](https://learn.microsoft.com/en-us/answers/questions/4376919/(article)-how-to-download-official-windows-11-iso)
7.  **Wait and Verify**
    *   When done, you’ll see **READY**.
    *   Test by booting from the USB on your target machine (change boot order in BIOS/UEFI). [[youtube.com]](https://www.youtube.com/watch?v=kwDSIOqt6xI)