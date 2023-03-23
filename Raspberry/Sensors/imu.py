import smbus2
import struct

# Initialize the I2C bus and sensor address
bus = smbus2.SMBus(1)
address = 0x1e  # Magnetometer address

# Magnetometer calibration data
mag_x_min = -250
mag_x_max = 250
mag_y_min = -250
mag_y_max = 250
mag_z_min = -250
mag_z_max = 250

# Accelerometer sensitivity (LSB/g)
acc_sensitivity = 8192

def read_acceleration():
    # Read acceleration data
    data = bus.read_i2c_block_data(address, 0x28, 6)
    x = struct.unpack('>h', bytes(data[0:2]))[0]
    y = struct.unpack('>h', bytes(data[2:4]))[0]
    z = struct.unpack('>h', bytes(data[4:6]))[0]

    # Convert to g
    x = x / acc_sensitivity
    y = y / acc_sensitivity
    z = z / acc_sensitivity

    return x, y, z

def read_magnetic_field():
    # Read magnetic field data
    data = bus.read_i2c_block_data(address, 0x03, 6)
    x = struct.unpack('>h', bytes(data[0:2]))[0]
    z = struct.unpack('>h', bytes(data[2:4]))[0]
    y = struct.unpack('>h', bytes(data[4:6]))[0]

    # Calibrate magnetometer data
    x = (x - mag_x_min) / (mag_x_max - mag_x_min) * 2 - 1
    y = (y - mag_y_min) / (mag_y_max - mag_y_min) * 2 - 1
    z = (z - mag_z_min) / (mag_z_max - mag_z_min) * 2 - 1

    return x, y, z

# Example usage
while True:
    accel_data = read_acceleration()
    print('Acceleration: x={:.2f}g, y={:.2f}g, z={:.2f}g'.format(*accel_data))

    mag_data = read_magnetic_field()
    print('Magnetic Field: x={:.2f}uT, y={:.2f}uT, z={:.2f}uT'.format(*mag_data))
