| Storage Type | GlusterFS | BeeGFS | Azure Files | Azure Blob (blobfuse) | Kernel NFS (single node)  
|-----------|:-----------|:-----------|:-----------|:-----------|:-----------|  
**Management** | Complex | Complex | None | None | Simple
**Storage Node Fault Tolerence** | High | High<sup>1</sup> | High | High | Low
**Known Media Performance (MB/s)** | 75 | 213-1200 | 60 | 60 | 200-8640<sup>2</sup>
**Supports Samba (SMB)** | Gateway<sup>3</sup> | Gateway<sup>3</sup> | Yes | No |Yes
**Linux Permissions** | Yes | Yes | Reduced | Reduced | Yes
**Supports [xattr](https://en.wikipedia.org/wiki/Extended_file_attributes)**| Yes | Addon | No | No | Yes
**Suports user quotas** | Yes | Yes | No | No | Yes
**Linux Connect** | Custom FUSE Client | Native Kernel Client | Samba | Custom Fuse Client | NFS
**Volume Size Limit** | PB or EB Scale | 16EiB | 5 TiB | 500 TiB | 256TB<sup>4</sup>
**File Size** | 8EiB | 8EiB | 1TiB | 1 TiB | 8 EiB
**SPOF Points<sup>5</sup>** | None | Mangement Node<br> Metadata Node | Azure | Azure | Single Node
**Encryption** | [DM-Crypt](https://docs.microsoft.com/en-us/azure/security/azure-security-disk-encryption#encrypting-os-drive-on-a-running-linux-vm) | [DM-Crypt](https://docs.microsoft.com/en-us/azure/security/azure-security-disk-encryption#encrypting-os-drive-on-a-running-linux-vm) | [Azure Storage Encryption](https://docs.microsoft.com/en-us/azure/storage/common/storage-service-encryption) | [Azure Storage Encryption](https://docs.microsoft.com/en-us/azure/storage/common/storage-service-encryption) | [DM-Crypt](https://docs.microsoft.com/en-us/azure/security/azure-security-disk-encryption#encrypting-os-drive-on-a-running-linux-vm) | 
**NFS Support** | NFSv3<br> NFS-Ganesha (not stable) | Gateway<sup>3</sup> | Gateway<sup>3</sup> | Gateway<sup>3</sup> | NFSv4
<sup>1</sup> BeeGFS has a SPOF at the management node
<sup>2</sup> Using a single disk, or a 5 disk raid increased performance slightly, but really allows better scale for multiple connections
<sup>3</sup> Gateway in this case means a separate node is set up mounting the filesystem, and runs Samba or an NFS server as a proxy.
<sup>4</sup> On a DS5_v2 or an L16s supporting 64 data disks
<sup>5</sup> All our clusters are built with RAID0 which is also a SPOF, but Azure data drive failures are extremely rare as they're backed by multiple devices.
<sup>6</sup> Encryption experimentation with LUKS is ongoing
##Reference
https://en.wikipedia.org/wiki/Comparison_of_file_systems


# Comparison Text
## GlusterFS
- Complex management/higher maintenance
- Robust storage/Low performance
- Ability to encrypt at rest with effort
- A single gluster cluster can manage multiple volumes of storage.
- Each storage volume is made up of backend "bricks". So different RAID arrays on each node member would be associated with a volume and thus a team.
- About the only reason you'd want different volumes is for different underlying storage architectures. Breaking up teams per volume would be a lot of work for little benefit.
- Can connect via native linux methods, not exactly performant.
- SMB needs to be done manually.
- ~70-80MB/sec on 16 thread for native client
- NFS-Ganesha got us 4.5GB/sec on 16 thread

##BeeGFS
- Complex management/higher maintenance
- Robustish storage/High performance
- Ability to encrypt at rest with effort
- Linux kernel issue is fixed in BeeGFS 6.18 (current release as of this writing)
- Similar to Gluster in many ways
- Doesn't support root_squash, but now with GDPR we don't need it
- ~1GB/sec on 16 thread for larger files >=16MB
- We found that the management server is still a SPOF
- Performance did extremely well on small files - 
   - 24GB/sec for 16 thread
   - 97GB/sec for 128 thread

##Azure Files
* Low/No cluster maintenance
* Ability to encrypt at rest, fuss free
* Robust storage/Low performance
* Serveral limitations (see below)
* SMB Only, so no user permissions. 
* Each team could easily have their own storage account for segmentation
* SMB gives HCL Access
* Samba related performance issues.
* 5TB limit/share
* 1TB file size limit
* Max 1000 IOPS/share
* 60MiB/s throughput
* Seems to imply a 64KB/transation
* No file limit
	
##Azure blobfuse
* Low/No cluster maintenance
* Ability to encrypt at rest, fuss free
* Robust storage/Low performance
* No user level permissions
* Each team could easily have their own storage account for segmentation
* Can HCL scan blobs?
* Azure Storage account has a default egress limit of 20Gbps, with 50 Gbps as the maximum. We observed Philly jobs in one Philly cluster frequently hit 100 Gbps egress bar. Reference
* 500TiB maximum share
* 60Mib/s or 500 requests/sec
* Some file system APIs have not been implemented: readlink, symlink, link, chmod, chown, fsync, lock and extended attribute calls.
* Can you expand a git repository on this?
	
##Kernel NFS
* Low Cluster Maintenance
* Not robust, limited scale/High performance
* Ability to encrypt at rest with effort
* Team shares would exist on different folders, and be available as different mounts
* Azure backed storage can make this reasonably fast
* NFS 4.1 makes the protocol performant.
* Can share this via Samba, as with GlusterFS
* Single 4TB (P50) drive offers 7500 IOPS/250MBps
* VMs go from 4000 IOPS - 128k IOPS (4*17 to max that out)
* A large enough VM should be able to scale.

##GDPR Needs
For shares not native Azure (GlusterFS, BeegFS, kNFS) a samba gateway would still need to exist as today.
* Turn off root_squashing (done)
* Add the following to smb.conf:
   *	username map = /etc/samba/usermap.txt
  *	Contents of usermap.txt to map myself to root:
   *	root = REDMOND.krisz

##Scratch Needs
* Peak storage utilization on on /bscratch and /gscratch was 21TB and 28TB respectively.

#Reference:
##IOPS
* Azure attached SSD 750 MB/s
* Typical SSD IOPS - 6,000
* Typical 15k drive IOPS - 175
* Max IOPS for a DS14 host - ~50k IOPS
##Azure
* Storage Accounts can hold a max of 500TiB/ea
