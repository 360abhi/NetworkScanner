
def get_cidr_notation(ip:str,subnet_mask:str)->str:
    cidr = sum([bin(int(octet)).count('1') for octet in subnet_mask.split(".")])
    return f"{ip}/{cidr}"