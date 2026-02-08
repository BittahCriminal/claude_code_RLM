### ✅ **Why Registration Is Required**

Microsoft has adopted a **Zero Trust** model, so devices connected to the wired network default to **internet-only access** unless registered.  Starting March 2025, unregistered devices are removed from CorpNet and must be registered to regain access. [[Wired Netw...nnectivity | ServiceNow KB (HelpDesk)]](https://microsoft.service-now.com/sp?id=kb_article_view&sys_id=0381e15c6408ae50356bc6ab217ed784)

* * *

### 🔐 **Steps to Register Your Wired Device**

1.  **Go to** [aka.ms/GetConnected](https://aka.ms/GetConnected).
2.  **Select**:
    *   **Quick Registration – Wired**
    *   **Employee CorpNet**
3.  **Choose your Region** from the dropdown.
4.  **Enter your device’s MAC address**:
    *   **Windows**:
        *   Open **Command Prompt** → type `netsh lan show interfaces` for wired connections.
        *   Look for **Physical Address**.
    *   **Linux**:
        *   Open **Terminal** → type `ip a` for wired connections.
        *   Look for **link/ether**.
    *   **Mac**:
        *   Go to **Apple Menu > System Preferences > Network > Ethernet Interface > Advanced > Hardware tab**.
5.  **Optional**:
    *   Check **Cycle Port** during registration or unplug/reboot the device **including** your network hub so the CorpNet switch port refreshes and moves your MAC address to the CorpNet network.
    *   Enable **Auto Renew** to avoid manual renewal every 30 days. [[Wired Netw...nnectivity | ServiceNow KB (HelpDesk)]](https://microsoft.service-now.com/sp?id=kb_article_view&sys_id=0381e15c6408ae50356bc6ab217ed784), [[Wired Netw...ork (ZTN) | ServiceNow KB (HelpDesk)]](https://microsoft.service-now.com/sp?id=kb_article_view&sys_id=3fa82b0e1b755910a29d2fc8b04bcbda), [[RE: Connec...g April 24 | Outlook]](https://outlook.office365.com/owa/?ItemID=AAMkADBiNDg3NGZmLWVlZjAtMTFkMi04ZjE2LTAwMDhjNzRiODU1NwBGAAAAAACQPS8yW7jOEZlwAIBfaCyzBwAqhZUX9foxSp6jiCXRwLDjAAACkeo9AAA9mrr90Bh4T52%2bZPLS%2fvjGAAW99GXEAAA%3d&exvsurl=1&viewmodel=ReadMessageItem)

![image.png](/.attachments/image-58c7e4c3-0817-4b74-8ff2-fba60122e0a7.png)