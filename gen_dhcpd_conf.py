#!/usr/bin/python3

""" Set your Vendor Prefix """ 
EX_VENDOR = "TP"

""" Set your Vendor Mac Prefix """ 
EX_MAC ="22:28:f3"

""" Set your Desired /24 Nets """ 
networks = ['192.168.0.0', '10.0.0.0']

DHCPD_FILE='dhcpd.hosts.stub.tmp'
HOSTS_FILE='hosts.tmp'

try:

    fh = open(DHCPD_FILE,'w')
    eh = open(HOSTS_FILE,'w')

    for line in open('hosts2mac.txt','r'):

        if line.startswith('#'):
            continue

        for one_network in networks:

            mac,number,name = line.split(',')
            name = name.strip()

            quads = one_network.split('.')
            quads[-1] =  number
            ip  = '.'.join(quads) 
            sn_pre = one_network.split('.')[0]

            fh.write(f"host {name}-{sn_pre} {{\n")
            fh.write(f"   hardware ethernet {mac};\n")
            fh.write(f"   fixed-address {ip};\n")
            fh.write(f"}}\n")

            mac = mac[8:]
            mac = EX_MAC +  mac
            fh.write(f"host {name}-{sn_pre}-{EX_VENDOR} {{\n")
            fh.write(f"   hardware ethernet {mac};\n")
            fh.write(f"   fixed-address {ip};\n")
            fh.write(f"}}\n")

        eh.write(f"{ip}   {name}\n")
except OSError as e:
    print(e)
finally:
    fh.close()
    eh.close()
