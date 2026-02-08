
```
ifconfig eth0 10.184.185.888/24
route add default gw 10.184.185.1 eth0

rm /etc/resolv.conf;touch /etc/resolv.conf;chmod 777 /etc/resolv.conf
{ echo 'options rotate'; echo 'options timeout:5'; echo 'options attempts:3'; echo ''; echo 'nameserver 10.50.10.50'; echo 'nameserver 10.50.50.50'; echo 'search redmond.corp.microsoft.com corp.microsoft.com guest.corp.microsoft.com'; } > /etc/resolv.conf

dnf -y update;dnf upgrade -y
#dnf whatprovides moby*

tdnf install -qy dhcp-client.x86_64 netplan.x86_64 python3-setuptools python3-pip openssh sudo shadow-utils vim procps-ng net-tools less azure-cli kubernetes-client golang zip make uuid git mlocate tar which util-linux tzdata iputils traceroute bind-utils awk bc ca-certificates

pip3 install –-upgrade pip
pip3 install az.cli

IPADDR=$(ip route get 10.50.50.50 | awk '{ print $7; exit}')
{ echo $IPADDR' '$HOSTNAME'.redmond.corp.microsoft.com '$HOSTNAME''; echo '127.0.0.1 localhost '$HOSTNAME; echo ''; echo '# The following lines are desirable for IPv6 capable hosts'; echo '::1     localhost ip6-localhost ip6-loopback'; echo 'ff02::1 ip6-allnodes'; echo 'ff02::2 ip6-allrouters'} > /etc/hosts



 
```