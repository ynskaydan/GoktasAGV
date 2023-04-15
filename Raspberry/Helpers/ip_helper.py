import os

from CrossCuttingConcerns import raspi_log


def setup_ip():
    ip_address = "192.168.1.100"  # Değiştirilecek IP adresi
    subnet_mask = "255.255.255.0"  # Değiştirilecek alt ağ maskesi
    default_gateway = "192.168.1.1"  # Değiştirilecek varsayılan ağ geçidi
    dns_server = "8.8.8.8"  # Değiştirilecek DNS sunucusu
    raspi_log.log_process(str(f"IP address of eth0 is changing to {ip_address}"))
    os.system(f"sudo ip addr add {ip_address}/{subnet_mask} dev eth0")
    os.system(f"sudo ip route add default via {default_gateway}")
    os.system(f"sudo echo 'nameserver {dns_server}' > /etc/resolv.conf")



