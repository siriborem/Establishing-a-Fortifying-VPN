import ipaddress

UNIVERSAL_SUBNET = '192.168.1.0/24'
ZERO_BIT_CIDR = '255.255.255.0'
ZERO_BIT_HEX = ipaddress.IPv4Network(ZERO_BIT_CIDR, strict=False).network_address
EVEN_MASK = ipaddress.IPV4LENGTH