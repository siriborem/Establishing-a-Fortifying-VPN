import ipaddress
from .variables import ZERO_BIT_CIDR, ZERO_BIT_HEX, UNIVERSAL_SUBNET, EVEN_MASK

class VPNController:
    def __init__(self, request_ip):
        self.original_ip = request_ip
        self.masked_ip = None
        self.configuration = None
        self.masking_fn = {
            'zero_bit': self.mask_ip_zero_bit,
            'subnet': self.mask_ip_subnet,
            'even': self.mask_even
        }

    def __str__(self):
        return str(self.masked_ip)

    def mask_ip_zero_bit(self):
        original_ip = ipaddress.ip_address(str(self.original_ip))
        masked_ip = ipaddress.ip_address(int(original_ip) & int(ZERO_BIT_HEX))
        self.masked_ip = masked_ip
        self.configuration = {'method': 'zero_bit'}
        return masked_ip
    
    def mask_ip_subnet(self):
        subnet_network = ipaddress.ip_network(UNIVERSAL_SUBNET, strict=False)
        original_ip = ipaddress.ip_address(str(self.original_ip))
        masked_ip = ipaddress.ip_address(int(original_ip) & int(subnet_network.network_address))
        self.masked_ip = masked_ip
        self.configuration = {'method': 'subnet'}
        return masked_ip
    
    def mask_even(self):
        mask = (2 ** EVEN_MASK) - 256
        original_ip = ipaddress.ip_address(str(self.original_ip))
        masked_ip = ipaddress.ip_address(int(original_ip) & mask)
        self.masked_ip = masked_ip
        self.configuration = {'method': 'even'}
        return masked_ip

    def unmask_ip(self):
        if self.masked_ip is None or self.configuration is None:
            raise ValueError("IP address is not masked or configuration is missing.")

        method = self.configuration['method']

        if method == 'zero_bit':
            original_ip = ipaddress.ip_address(int(self.masked_ip) | int(ZERO_BIT_HEX))
        elif method == 'subnet':
            subnet_network = ipaddress.ip_network(UNIVERSAL_SUBNET, strict=False)
            original_ip = ipaddress.ip_address(int(self.masked_ip) | int(subnet_network.network_address))
        elif method == 'even':
            mask = (2 ** EVEN_MASK) - 256
            original_ip = ipaddress.ip_address(int(self.masked_ip) | mask)
        else:
            raise ValueError("Invalid masking method.")

        return original_ip    


