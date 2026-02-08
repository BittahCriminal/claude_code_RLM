Here is a quick template to register DNS,  have it register at startup(rc.local) and reregister every 30 minutes(cron job).

```
#Startup
touch /etc/rc.local;chmod +x /etc/rc.local
    cat <<'EOF' > /etc/rc.local
#!/usr/bin/env bash
/etc/rc.local
EOF


#DNS Script to register $HOSTNAME.guest.corp.microsoft.com
touch /usr/local/bin/register_dns.sh;chmod +x /usr/local/bin/register_dns.sh
    cat <<'EOF' > /usr/local/bin/register_dns.sh
#!/usr/bin/env bash
DOMAIN1="redmond.corp.microsoft.com"
DOMAIN2="guest.corp.microsoft.com"
IPADDR=$(ip route get 10.50.50.50 | awk '{ print $7; exit}')
GUESTNS=`dig +short -t NS guest.corp.microsoft.com|head -n 1`
GUESTNSIP=`dig +short $GUESTNS`
echo "server $GUESTNSIP" > /tmp/dnsupdate
echo "update add $(hostname -s).${DOMAIN1}. 86400 A $IPADDR" >> /tmp/dnsupdate
echo "update add $(hostname -s).${DOMAIN2}. 86400 A $IPADDR" >> /tmp/dnsupdate
if [ -n "$BIPADDR" ]; then
echo "update add i$(hostname -s).${DOMAIN2}. 86400 A $BIPADDR" >> /tmp/dnsupdate
fi
echo "send" >> /tmp/dnsupdate
nsupdate -d /tmp/dnsupdate
rm /tmp/dnsupdate
EOF


#Add CronJob for /usr/local/bin/register_dns.sh
echo '0 * * * * root test -x /usr/local/bin/register_dns.sh && sleep $(shuf -i 0-900 -n 1) && /usr/local/bin/register_dns.sh'>/etc/cron.d/register_dns;chmod 644 /etc/cron.d/register_dns

```
