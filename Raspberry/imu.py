import smbus2
import time

# I2C address of the sensor
DEVICE_ADDRESS = 0x68

# Register addresses for sensor data
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
TEMP_OUT_H = 0x41
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
COMPASS_XOUT_H = 0x49
COMPASS_YOUT_H = 0x4B
COMPASS_ZOUT_H = 0x4D

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Set up the sensor
bus.write_byte_data(DEVICE_ADDRESS, 0x6B, 0)
bus.write_byte_data(DEVICE_ADDRESS, 0x1A, 1 << 2)
bus.write_byte_data(DEVICE_ADDRESS, 0x1B, 1 << 1)

# Main loop
while True:
    # Read raw sensor data
    accel_x = read_word_2c(bus, ACCEL_XOUT_H)
    accel_y = read_word_2c(bus, ACCEL_YOUT_H)
    accel_z = read_word_2c(bus, ACCEL_ZOUT_H)
    temp = read_word_2c(bus, TEMP_OUT_H) / 340.0 + 36.53
    gyro_x = read_word_2c(bus, GYRO_XOUT_H)
    gyro_y = read_word_2c(bus, GYRO_YOUT_H)
    gyro_z = read_word_2c(bus, GYRO_ZOUT_H)
    compass_x = read_word_2c(bus, COMPASS_XOUT_H)
    compass_y = read_word_2c(bus, COMPASS_YOUT_H)
    compass_z = read_word_2c(bus, COMPASS_ZOUT_H)

    # Print sensor data
    print("Acceleration (m/s^2): ({:.2f}, {:.2f}, {:.2f})".format(accel_x/16384.0, accel_y/16384.0, accel_z/16384.0))
    print("Temperature: {:.2f} C".format(temp))
    print("Angular velocity (dps): ({:.2f}, {:.2f}, {:.2f})".format(gyro_x/131.0, gyro_y/131.0, gyro_z/131.0))
    print("Magnetic field (uT): ({:.2f}, {:.2f}, {:.2f})".format(compass_x*0.92, compass_y*0.92, compass_z*0.92))

    # Delay before next reading
    time.sleep(0.5)

def read_word_2c(bus, reg):
    high = bus.read_byte_data(DEVICE_ADDRESS, reg)
    low = bus.read_byte_data(DEVICE_ADDRESS, reg+1)
    value = (high << 8) + low
    if (value >= 0x8000):
        return -((65535 - value) + 1)
    else:
        return value