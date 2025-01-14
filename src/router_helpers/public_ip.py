import psutil
import requests

def get_public_ip():
    """
    Fetch the public ip of the router from an external service.
    """
    try:
        response = requests.get('https://api.ipify.org?format=json') # Public ip to get external IP
        response.raise_for_status() # To ensure no http errors occured
        return response.json().get("ip","Unable to fetch the IP...")
    except requests.RequestException as e:
        return f"Error fetching public IP: {e}"

if __name__ == "__main__":
    print("Fetching Network Details......\n")
    print(f"public ip : {get_public_ip()}")