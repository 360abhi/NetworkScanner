# Get Connected Network Details 

import psutil
import socket

def connected_network_details() -> dict:
    """
    Fetches the details of the network interfaces currently up in the device.
    """
    # Network interfaces
    net_if_addrs = psutil.net_if_addrs() # Network interfaces and their addresses
    net_if_stats = psutil.net_if_stats() # Fetch stats of interfaces
    network_details = {}

    print("Fetching Network Details.....\n")

    for interface,addrs in net_if_addrs.items():
        details = {}
        flag = True
        for addr in addrs:
            if addr.family == socket.AF_INET: #IPv4 Address
                details['IP Address'] = addr.address
                details['Subnet Mask'] = addr.netmask
                details['Broadcast'] = addr.broadcast
            elif addr.family == socket.AF_PACKET: #MAC Address
                if str(addr.address) == "00:00:00:00:00:00":
                    flag = False
                details['MAC Address'] = addr.address

        # Checking if the interface is up/down
        details['Status'] = "UP" if net_if_stats[interface].isup else "DOWN"
        if details and flag:
            network_details[interface] = details

    return network_details


def print_network_details(network_details:dict) -> None:
    for interface,details in network_details.items():
        print(f"Interface: {interface}")
        for key,val in details.items():
            print(f"{key}: {val}")
        print()

print_network_details(connected_network_details())