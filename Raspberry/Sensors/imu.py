import smbus
import math
import time

bus = smbus.SMBus(1)
address = 0x68

# Pusula kalibrasyon sabitleri
x_offset = 0
y_offset = 0
z_offset = 0
x_scale = 1
y_scale = 1

def read_byte(address, adr):
    return bus.read_byte_data(address, adr)

def read_word(address, adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(address, adr):
    val = read_word(address, adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(address, adr, value):
    bus.write_byte_data(address, adr, value)

def calibrate_compass():
    global x_offset, y_offset, z_offset, x_scale, y_scale
    x_offset = -84.5
    y_offset = -146.5
    z_offset = -126.5
    x_scale = 1.16
    y_scale = 1.08

def setup_imu():
    # MPU6050 için güç yönetimini ayarlama
    write_byte(address, 0x6B, 0x00)

    # AK8975C için ölçek faktörünü ayarlama
    write_byte(0x0C, 0x0A, 0x16)

def read_imu():
    # Pusula verileri okuma
    x_out = read_word_2c(address, 0x03) - x_offset
    y_out = read_word_2c(address, 0x05) - y_offset
    z_out = read_word_2c(address, 0x07) - z_offset

    # Pusula verilerinin yönlerini belirleme
    bearing = math.atan2(y_out * y_scale, x_out * x_scale)
    if (bearing < 0):
        bearing += 2 * math.pi

    # İvme verileri okuma
    x_acc_out = read_word_2c(address, 0x3B)
    y_acc_out = read_word_2c(address, 0x3D)
    z_acc_out = read_word_2c(address, 0x3F)

    # İvme verilerini hesaplama
    x_acc_scaled = x_acc_out / 16384.0
    y_acc_scaled = y_acc_out / 16384.0
    z_acc_scaled = z_acc_out / 16384.0

    # Sonuçları döndürme
    return (math.degrees(bearing), x_acc_scaled, y_acc_scaled, z_acc_scaled)

# Pusula kalibrasyonunu yapma
calibrate_compass()

# IMU ayarlarını yapma
setup_imu()

while True:
    # Verileri okuma
    bearing, x_acc, y_acc, z_acc = read_imu()

    # Sonuçları yazdırma
    print("Pusula Yönü:", bearing)
    print("X İvme:", x_acc)
    print("Y İvme:", y_acc)
    print("Z İvme:", z_acc)

    # 1
