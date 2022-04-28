#!/usr/bin/python3

""" gen_dhcpd_conf.py - Create an entry for MACs not masked by the vendor's """
""" extender and one that is for each network on the LAN using hosts2mac as """
""" primary source of information - (Name|MAC|last IP octect)               """
""" Each final entry contains MAC,IP and Name (see template)                """

import sys
from jinja2 import Template

""" Set your Vendor Prefix """
EX_VENDOR = "TP"

""" Set your Vendor Mac Prefix """
EX_MAC = "22:28:f3"

""" Set your Desired /24 Nets """
networks = ["192.168.0.0", "10.0.0.0"]

DHCPD_STUB      = "dhcpd.hosts.stub.tmp"
HOSTS_FILE_STUB = "hosts.tmp"
DHCPD_TEMPLATE  = "dhcpd.template"
MAC_DB          = "hosts2mac.txt"

def set_jinja(data, fh):
    fh.write(j2_template.render(data) + "\n")

try:

    #Open Template and be done with it
    with open(DHCPD_TEMPLATE,'r') as dt:
        j2_template = Template(dt.read())

    dh_tmp = open(DHCPD_STUB, "w")
    eh_tmp = open(HOSTS_FILE_STUB, "w")

    for line in open(MAC_DB, "r"):

        if line.startswith("#"):
            continue

        for one_network in networks:

            mac, number, name = line.split(",")
            name = name.strip()

            quads = one_network.split(".")
            quads[-1] = number
            ip = ".".join(quads)

            sn_pre = one_network.split(".")[0]
            hostname = f"{name}-{sn_pre}"


            """ Normal Mac """
            data = {"mac": mac, "ip": ip, "hostname": hostname}
            set_jinja(data, dh_tmp)

            """ Vendor Prefix Mac """
            data = {
                "mac": EX_MAC + mac[8:],
                "ip": ip,
                "hostname": f"{hostname}-{EX_VENDOR}",
            }
            set_jinja(data, dh_tmp)
            eh_tmp.write(f"{ip}  {hostname}-{EX_VENDOR}\n")

except OSError as e:
    print(e)
except ValueError as e:
    if 'not enough values to unpack' in str(e):
        print(f"Error: {e}, Did you format {MAC_DB} correctly?") 
        sys.exit(1)
finally:
    dh_tmp.close()
    eh_tmp.close()
