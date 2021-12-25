#!/bin/bash
PI="192.168.0.199"
scp -i /root/wild hosts2mac.txt dhcpd.template dhcpd.conf.stub gen_dhcpd_conf* $PI:/etc
ssh -i /root/wild $PI "cd /etc/; ./gen_dhcpd_conf.sh"
