import os
import pwd
import stat

from CrossCuttingConcerns import raspi_log

def setup_ip():
    file_path = "/dev/ttyS0"
    permissions = 0o666
    user = "goktas"
    group = "rpi"
    ip_address = "192.168.1.101"  # Değiştirilecek IP adresi
    subnet_mask = "255.255.255.0"  # Değiştirilecek alt ağ maskesi
    default_gateway = "192.168.1.1"  # Değiştirilecek varsayılan ağ geçidi
    dns_server = "8.8.8.8"  # Değiştirilecek DNS sunucusu

    raspi_log.log_process(str(f"IP address of eth0 is changing to {ip_address}"))
    raspi_log.log_process(str(f"File permission is configuring in dev/ttyS0"))
    os.system(f"sudo ip addr add {ip_address}/{subnet_mask} dev eth0")
    os.system(f"sudo ip route add default via {default_gateway}")
    os.system(f"sudo echo 'nameserver {dns_server}' > /etc/resolv.conf")
    try:
        user_uid = pwd.getpwnam(user).pw_uid
        group_gid = pwd.getpwnam(user).pw_gid
        os.chown(file_path,user_uid,group_gid)
        raspi_log.log_process("File owner changed to goktas")
    except OSError as e:
        raspi_log.log_process(str(f"There was an error while chown process: {e}"))
    os.chmod(file_path, permissions)
    al_permissions = oct(stat.S_IMODE(os.stat(file_path).st_mode))
    if al_permissions == oct(permissions):
        raspi_log.log_process(str(f"Permissions are configured!"))
    else:
        raspi_log.log_process(str(f"Permissions are not configured!"))


