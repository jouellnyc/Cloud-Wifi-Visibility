#!/bin/bash

LEASE_FILE="/var/lib/dhcp/dhcpd.leases"
LEASE_DH_FILE="/var/lib/dhcp/dhclient.leases"

service isc-dhcp-server stop
rm "${LEASE_FILE}"    && rm "${LEASE_FILE}"~ 
rm "${LEASE_DH_FILE}" && rm "${LEASE_DH_FILE}"~ 

echo "" > $LEASE_FILE 
service isc-dhcp-server start
