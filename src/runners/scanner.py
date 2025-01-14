import json
import sys
import os
# Adding the project root to the sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
sys.path.insert(0, root_dir)
from src.router_helpers import get_public_ip,arp_request,get_mac_address,scan_network,network_interfaces,get_cidr_notation

def runner():

    # Getting the interface and the cidr notation
    ip,mask = None,None
    interfaces = network_interfaces()
    for _,value_dict in interfaces.items():
        ip = value_dict['IP Address']
        mask = value_dict['Subnet Mask']
    
    cidr = get_cidr_notation(ip=ip,subnet_mask=mask)

    # Getting the public ip
    public_ip = get_public_ip()
    print(f"CIDR :{cidr} and PUBLIC IP:{public_ip}")

    # Getting the devices connected ip address
    devices = []
    devices_list = scan_network(network_cidr=cidr)
    for device in devices_list:
        devices.append(device['IP Address'])

    print(devices)

    # Getting Mac Address of the devices
    mac = []
    for ip in devices:
        mac.append(get_mac_address(ip=ip))

    print(mac)


runner()