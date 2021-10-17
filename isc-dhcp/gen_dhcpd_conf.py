#!/usr/bin/python3

""" gen_dhcpd_conf.py - Create an entry for MACs not masked by the vendor's """
""" extender and one that is for each network on the LAN using hosts2mac as """
""" primary source of information - (Name|MAC|last IP octect)               """
""" Each final entry contains MAC,IP and Name (see template)                """

from jinja2 import Template

""" Set your Vendor Prefix """
EX_VENDOR = "TP"

""" Set your Vendor Mac Prefix """
EX_MAC = "22:28:f3"

""" Set your Desired /24 Nets """
networks = ["192.168.0.0", "10.0.0.0"]

DHCPD_STUB     = "dhcpd.hosts.stub.tmp"
HOSTS_FILE     = "hosts.tmp"
DHCPD_TEMPLATE = "dhcpd.template"

def set_jinja(data, fh):
    fh.write(j2_template.render(data) + "\n")

try:

    #Open Template and be done with it
    with open(DHCPD_TEMPLATE,'r') as dt:
        j2_template = Template(dt.read())

    dh = open(DHCPD_STUB, "w")
    eh = open(HOSTS_FILE, "w")

    for line in open("hosts2mac.txt", "r"):

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
            set_jinja(data, dh)

            """ Vendor Prefix Mac """
            data = {
                "mac": EX_MAC + mac[8:],
                "ip": ip,
                "hostname": f"{hostname}-{EX_VENDOR}",
            }
            set_jinja(data, dh)

        eh.write(f"{ip}   {name}\n")

except OSError as e:
    print(e)
finally:
    dh.close()
    eh.close()
