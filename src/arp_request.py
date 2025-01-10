from scapy.all import ARP, Ether, srp,conf

def scan_network(network_cidr:str):
    """
    Scans the given network to find the connected devices
    Args: network_cidr:the nw range in cidr format (eg: 192.168.1.0/24)
    Returns: a list of dict containing info about connected devices
    """

    # Creating an ARP request packet
    arp_request = ARP(pdst=network_cidr) # Set the destination subnet

    # Create an ethernet frame
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff") # Send to all the devices

    # Combine the ARP request and ethernet frame
    packet = broadcast / arp_request

    # Send the packet and recieve the response
    result = srp(packet,timeout=1,verbose=0)

    print(result)
    # Prase the response
    devices=[]
    for sent,recieved in result[0]:
        print(f"Sent ARP request to: {sent[ARP].pdst}")
        print(f"Received response from: {recieved[ARP].psrc} - {recieved[ARP].hwsrc}")
        devices.append({
            "IP ADDRESS":recieved.psrc,
            "MAC ADDRESS": recieved.hwsrc
        })

    return devices


def get_mac_address(ip:str):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    result = srp(packet,timeout=5,verbose=0)

    if result[0]: # Answered array
        return result[0][0][1].hwsrc
    else:
        return None

# Main code
if __name__ == "__main__":
    try:
        network_cidr = "192.168.1.0/24"
        devices = scan_network(network_cidr=network_cidr)
        print(devices)
        print(len(devices))

        print(f"Devices found in the network {network_cidr}:")
        for idx,device in enumerate(devices,start=1):
            print(f"{idx}: IP Address: {device['IP ADDRESS']}, MAC Address: {device['MAC ADDRESS']}")

    except Exception as e:
        print(str(e))