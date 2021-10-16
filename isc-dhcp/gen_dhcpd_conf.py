#!/usr/bin/python3

from jinja2 import Template

""" Set your Vendor Prefix """
EX_VENDOR = "TP"

""" Set your Vendor Mac Prefix """
EX_MAC = "22:28:f3"

""" Set your Desired /24 Nets """
networks = ["192.168.0.0", "10.0.0.0"]

DHCPD_FILE = "dhcpd.hosts.stub.tmp"
HOSTS_FILE = "hosts.tmp"

template = """host {{ hostname }} {
    hardware ethernet {{ mac }};
    fixed-address {{ ip }};
}"""


def set_jinja(data, fh):
    fh.write(j2_template.render(data) + "\n")


try:

    dh = open(DHCPD_FILE, "w")
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

            j2_template = Template(template)

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
