
###Dynamic DNS was designed for PC’s
###Static DNS is for servers

- Servers use well known IP addresses and ports
- Server IP addresses rarely change.
- Servers use well known IP ports.
- Clients use less known IP addresses and random ports.

### Servers are static, so their DNS should be as well.




 Each zone file in the dns directory controls a domain.  The domain is the name of the zone file.
Make a change (or add a file) and push it to master and VSTS builds will check and push your zone files and config.  

It auto updates the zone file serial numbers as well.  If your syntax is bad or has other problem it won't push.
The DNS servers themselves also check zone file syntax before they install the zone.

The VSTS build also creates a config for the DNS caching servers (see below), automatically updated for each zone that's defined in the zone files.

So if you create a new zone (super.secret.network.net) or other for example, the DNS caches will automatically start answering queries for that and all the other domains.


The caching (recursive) resolvers:   (for use on workstations to resolve all addresses)

netservice3.corp.microsoft.com has address 10.170.69.135
netservice4.corp.microsoft.com has address 172.16.227.210

The authoritative servers:  Humans don't normally query these servers, they only answer questions about the domains that they are authoritative for.

netservice1.corp.microsoft.com has address 10.214.70.0
netservice2.corp.microsoft.com has address 10.214.70.1


Examples:

dig @10.170.69.135 zeroedge.zero.ms.corp.

(stuff deleted - answer)

zeroedge.zero.ms.corp. 120 IN A 192.168.5.1

The resolvers will resolve for all microsoft and other domains in addition to the "added" domains like zero.ms.corp. which is one of my "fake" domains.

dig @10.170.69.135 ufl.edu

(reduced output)

ufl.edu.  65 IN A 128.227.9.98


Also all microsoft internal domain names:


dig @10.170.69.135 msrqc002.corp.microsoft.com






