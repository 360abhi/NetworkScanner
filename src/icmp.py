import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor

def ping(ip):
    """
    Pings an IP address to check if it is active.
    Args:
        ip (str): The IP address to ping.
    Returns:
        dict: A dictionary containing the IP and Hostname if the device is reachable.
    """
    try:
        # Use the ping command to check connectivity
        output = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
        if output.returncode == 0:
            try:
                # Try to get the hostname of the device
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = "Unknown"
            return {"IP Address": ip, "Hostname": hostname}
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
    return None

def scan_network(network_cidr):
    """
    Scans the given network range to find connected devices.
    Args:
        network_cidr (str): The network range in CIDR format (e.g., "192.168.1.0/24").
    Returns:
        list: A list of dictionaries containing IP and hostname of connected devices.
    """
    network = network_cidr.split("/")[0]
    subnet_mask = int(network_cidr.split("/")[1])

    # Calculate the range of IP addresses
    octets = network.split(".")
    base_ip = ".".join(octets[:3]) + "."
    start_ip = 1
    end_ip = 2 ** (32 - subnet_mask) - 2

    devices = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        ips = [base_ip + str(i) for i in range(start_ip, end_ip + 1)]
        results = executor.map(ping, ips)

    for result in results:
        if result is not None:
            devices.append(result)

    return devices

# Main code
try:
    network_cidr = "192.168.1.0/24"  # Replace with your network range
    print(f"Scanning network: {network_cidr}")
    devices = scan_network(network_cidr)
    
    print(f"\nDevices found in the network {network_cidr}:")
    for idx, device in enumerate(devices, start=1):
        print(f"{idx}: IP Address: {device['IP Address']}, Hostname: {device['Hostname']}")

except Exception as e:
    print(str(e))
