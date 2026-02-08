[[_TOC_]]

#1st Connect to Azure VPN
```
$vpnName = "MSFT-AzVPN-Manual";
$vpn = Get-VpnConnection -Name $vpnName;
if($vpn.ConnectionStatus -eq "Disconnected"){
rasdial $vpnName;
}
```

#Update clush for less noisy output
```
sudo apt install -y clustershell
{
echo '# Configuration file for clush'
echo '#'
echo '# Please see man clush.conf(5)'
echo '#'
echo ''
echo '[Main]'
echo 'fanout: 256'
echo 'connect_timeout: 15'
echo 'command_timeout: 480'
echo 'color: auto'
echo 'fd_max: 8192'
echo 'history_size: 100'
echo 'node_count: yes'
echo 'verbosity: 1'
echo ''
echo '# Add always all remote hosts to known_hosts without confirmation'
echo 'ssh_user: sdahl@microsoft.com'
echo 'ssh_path: /usr/bin/ssh'
echo 'ssh_options: -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -oBatchMode=yes -oLogLevel=quiet'
echo ''
echo '# Non-interactively performing password authentication with SSHs so called'
echo '# "interactive keyboard password authentication".'
echo '#Best to update DOMAIN.user so you do not have to run "clush -l REDMOND.billg -w nodes update -p"'
echo '#ssh_user: REDMOND.billg'
echo '#ssh_path: /usr/bin/sshpass -f /root/remotepasswordfile /usr/bin/ssh'
echo '#scp_path: /usr/bin/sshpass -f /root/remotepasswordfile /usr/bin/scp'
} > /etc/clustershell/clush.conf
```
#Group Configs:
```
{
echo 'sandbox1xx: GCRSANDBOX1[01-33]' #DGX Station
echo 'sandbox1rr: GCRSANDBOX1[34-93]' #HPE XL675d Gen10+
echo 'sandbox3: GCRSANDBOX[300-544]' #Amax GPU A6K & H100 workstations
echo 'NCUS: GCRAZGDL[1116-1215]' #Azure GPU workstations
echo 'WUS3: GCRAZGDL[1400-1715,3001-3068,4001-4048,5001-5004]' #Azure GPU workstations
} > /etc/clustershell/groups
```

#Clush will use your SSH configuration
```
#I often use virtual rather than typing passphrases.
eval `ssh-agent -s`
ssh-add .ssh/keyfilename
#ssh-add -l #to list key hash
2048 SHA256:bLP6zT3EA+aeDUxJOfMP1ETezSQXnBRMLPvJUVkHl4M /home/msrinet/.ssh/id_rsa (RSA)
2048 SHA256:RfaHJDcMgargUBiMHooDAqQxGsejw7h2ymXIemhT2vA .ssh/id_rsa_ddn (RSA)
2048 SHA256:LPXu8LNsn5463x8LVclA5cYB3wG8AnUpPxQi4iOop0E .ssh/ilokey (RSA)
256 SHA256:sBCltbZXLjq/+yqQ4Q1YUKRKj9/jaYkTjzg9Hty5zMQ core@microsoft.com (ED25519)
4096 SHA256:pr7KXbxHzMVcB/eQ6doYk2A9nlRRuW2Qd/Q7G8vJx7Q .ssh/id_sdahlrsa (RSA)
```

#Common Scripts
```
#Dump list from daily check to see if offline or login issue
vi Servers.txt
nodenames=`cat Servers.txt | cut -d':' -f1 | nodeset -f`;echo $nodenames
clush -w $nodenames --worker=exec nc -zv %host 22

# helps find failed GPU's & drivers
clush -f 350 -bg sandbox[1-3] "uname -r"
clush -f 350 -g sandbox[1-3] "sudo nvidia-smi -pm 1"
clush -f 350 -bg sandbox[1-3] "lsmod|grep peer|wc -l"

clush -f 350 -g sandbox[1-3] "uptime -p"|sort #great for seeing systems not being patched(4 weeks uptime)
clush -f 350 -bg sandbox[1-3] "sudo azcmagent show|grep 'Agent Version'"
clush -f 350 -bg sandbox[1-3] "apt list|grep gcr-ansible-pkg" 2>/dev/null
clush -f 350 -g sandbox[1-3] "sudo ansible-run|grep -i ignored" 2>/dev/null|sort  #finding Nodes managed by Ansible that are not functionally happy.
clush -f 350 -bg sandbox[1-3] "sudo /usr/local/bin/register_dns.sh 2>&1 | grep Successfully" #find nodes that fail Ansible user updates to provide DNS
clush -f 350 -g sandbox[1-3] "sudo cat /root/gcr_reservation.json | jq -r '.alias[]' | xargs -I {} last -w {} | sort -u -k1,1|grep -v wtmp" 2>/dev/null|sort #Build user list
clush -f 350 -bg sandbox[1-3] nvidia-smi topo -m |grep GPU # nvidia difference finder
clush -f 350 -bg sandbox[1-3] "apt list | grep gcr-ansible" #ansible version check
clush -f 350 -bg sandbox[1-3] "ls -la /var/lib/extrausers/* | wc -l" #groups needed for AAD auth
clush -f 350 -bg sandbox[1-3] "sudo ipmitool sensor|grep FAN|egrep -v 'ok|nc|0x0180'"
clush -w GCRSANDBOX[xxx] --worker=exec nc -zv %host 22 #useful for finding list of systems that are alive, but lack auth from 255 error scripts


clush -f 700 -bg NCUS,WUS2,WUS3 uname -r
clush -f 1040 -bg sandbox[1-3],NCUS,WUS2,WUS3 uname -r
clush -l msrsupp -f 350 -g sandbox[1-3] "sudo bash -l -c ansible-run 2>&1 | tee /tmp/ACheck.log"|sort
```

#Accounts and Access
```
clush -w GCRAMDRR1-MI100-[001-092] "ls -la /home | grep aiscadmin$" | sort # check that aiscadmin homedir exists
clush -w GCRAMDRR1-MI100-[001-092] "ls -la /home | grep core$" | sort # check that core homedir exists
clush -w GCRAMDRR1-MI100-[001-092] "ls -la /home | grep msrsupp$" | sort # check that msrsupp homedir exists

clush -w GCRAMDRR1-MI100-[001-092] "sudo cat /home/aiscadmin/.ssh/authorized_keys | wc -l" | sort # count should be 1
#clush -w GCRAMDRR1-MI100-[001-092] "sudo cat /home/core/.ssh/authorized_keys | wc -l" | sort # no longer using core ssh keys, so check is commented out
clush -w GCRAMDRR1-MI100-[001-092] "sudo cat /home/msrsupp/.ssh/authorized_keys | wc -l" | sort # count should be 8

clush -w GCRAMDRR1-MI100-[001-092] "id -u aiscadmin" | sort # aiscadmin uid should be 9022
clush -w GCRAMDRR1-MI100-[001-092] "id -u msrsupp" | sort # msrsupp uid should be 9023
clush -w GCRAMDRR1-MI100-[001-092] "id -u core" | sort # core uid should be 1000

clush -w GCRAMDRR1-MI100-[001-092] "groups aiscadmin" | sort # groups should be aiscadmin : localaccounts adm sudo docker
clush -w GCRAMDRR1-MI100-[001-092] "groups msrsupp" | sort # groups should be msrsupp : localaccounts

```

#HPE Checks
```
clush -l ubuntu -bw GCRAMDRR1-MI100-[001-090] "sudo dmidecode -s bios-release-date" # should be 08/11/2021
clush -l ubuntu -bw GCRAMDRR1-MI100-[001-099] "sudo hponcfg -h|grep Firmware" # should be Firmware Revision = 2.42 Device type = iLO 5 Driver name = hpilo
clush -f 250 -w iphlrr[2001-2020,3001-3116,4001-4114] --worker=exec nc -zv %host 22
for i in {2001..2020} {3001..3116} {4001..4114};do nc -zv iphlrr$i.guest.corp.microsoft.com 22;done

nodenames=`cat Servers.txt | cut -d':' -f1 | nodeset -f`;echo $nodenames
clush -f 400 -bw $nodenames "uname -r"
clush -f 400 -w gcrsandbox101 --worker=exec nc -zv %host 22
clush -f 400 -w $nodenames "curl -s ftp://172.31.43.138/CheckILO.iLO.sh|sudo bash 2>/dev/null"
```
#iLO REST
```
clush -w GCRAMDRR1-MI100-[001-092] "which ilorest" | sort
clush -w GCRAMDRR1-MI100-[001-092] "sudo ilorest bootorder | grep '^1\.' | grep -v None" | sort
clush -w GCRAMDRR1-MI100-[001-092] "sudo ilorest get BootOrderPolicy --select Bios. | grep BootOrderPolicy" | sort
```
#Drivers
```
clush -w GCRAMDRR1-MI100-[001-092] "ofed_info -s" | sort # MLNX_OFED_LINUX-5.3-1.0.0.1:
```

#Docker
```
clush -w GCRAMDRR1-MI100-[001-092] "cat /etc/group | grep docker" | sort # docker:x:998:core,aiscadmin
clush -w GCRAMDRR1-MI100-[001-092] "docker -v" | sort # Docker version 20.10.6+azure, build 370c28948e3c12dce3d1df60b6f184990618553f
clush -w GCRAMDRR1-MI100-[001-092] "systemctl show --property ActiveState docker" | sort # Should we be making sure the service is started?

```
```
clush -f 350 -g sandbox[1-3] "nvidia-smi -h|grep Sys" 2>/dev/null | sort
clush -f 350 -w GCRSANDBOX[107-109,203-204,208-211,245,275,312,315,318,334,361,365,393-394,408,410,412,421,424,431,439,447,469,475,477,479,484,492,494,498,507,521-522,526-527,530-533,535,541] --worker=exec nc -zv %host 22
```
