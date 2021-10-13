#!/bin/bash

set -u 

STATIC_VARS="192.168.0.198   raspi4B
192.168.0.198   raspi4B"

export DHCPD_FILE_REAL='/etc/dhcp/dhcpd.conf'
export DHCPD_STUB='dhcpd.conf.stub'
export DHCPD_STUB_TMP='dhcpd.conf.stub.tmp'
export DHCPD_HOSTS_STUB_TMP='dhcpd.hosts.stub.tmp'
export EH='/etc/hosts'
export EH_TEMP='/etc/hosts.tmp'


#Delete old temp files...
(
rm $DHCPD_STUB_TMP
rm $DHCPD_HOSTS_STUB_TMP
) 2> /dev/null

set -e 

cd /etc/

#Back up important files
cp $DHCPD_FILE_REAL{,.bak} || exit 1
cp $DHCPD_STUB{,.bak}      || exit 1

#Prepare a temp dhcp stump file
cp $DHCPD_STUB $DHCPD_STUB_TMP

#Generate dhcpd.hosts.stub.tmp and  hosts.tmp
./gen_dhcpd_conf.py || exit 1

#Appends host to temp stub file
cat   $DHCPD_HOSTS_STUB_TMP >> $DHCPD_STUB_TMP
cp -p $DHCPD_STUB_TMP          $DHCPD_FILE_REAL 

#/etc/hosts
cp $EH{,.bak}
echo "$STATIC_VARS"  > $EH

cat $EH_TEMP >> /etc/hosts

#Bounce DHCPD
service isc-dhcp-server restart || exit 1

#Reload DNS Data into PiHole
/usr/local/bin/pihole restartdns reload-lists || exit 1

#Delete old temp files...
rm $DHCPD_STUB_TMP
rm $DHCPD_HOSTS_STUB_TMP

