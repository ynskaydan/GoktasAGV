import smbus
import time

# Define the I2C bus to use (0 or 1)
bus = smbus.SMBus(1)

# Define the address of the IMU sensor
address = 0x68

# Power on the IMU sensor
bus.write_byte_data(address, 0x6B, 0)


# Read the accelerometer data
def read_accel():
    # Read the raw accelerometer data
    raw_accel_x = bus.read_word_data(address, 0x3B)
    raw_accel_y = bus.read_word_data(address, 0x3D)
    raw_accel_z = bus.read_word_data(address, 0x3F)

    # Convert the raw data to G values
    accel_x = raw_accel_x / 16384.0
    accel_y = raw_accel_y / 16384.0
    accel_z = raw_accel_z / 16384.0

    # Return the G values as a tuple
    return (accel_x, accel_y, accel_z)


# Read the gyroscope data
def read_gyro():
    # Read the raw gyroscope data
    raw_gyro_x = bus.read_word_data(address, 0x43)
    raw_gyro_y = bus.read_word_data(address, 0x45)
    raw_gyro_z = bus.read_word_data(address, 0x47)

    # Convert the raw data to degrees per second
    gyro_x = raw_gyro_x / 131.0
    gyro_y = raw_gyro_y / 131.0
    gyro_z = raw_gyro_z / 131.0

    # Return the degrees per second as a tuple
    return (gyro_x, gyro_y, gyro_z)


# Read the magnetometer data
def read_mag():
    # Read the raw magnetometer data
    raw_mag_x = bus.read_word_data(address, 0x03)
    raw_mag_y = bus.read_word_data(address, 0x05)
    raw_mag_z = bus.read_word_data(address, 0x07)

    # Convert the raw data to microtesla
    mag_x = raw_mag_x * 0.92
    mag_y = raw_mag_y * 0.92
    mag_z = raw_mag_z * 0.92

    # Return the microtesla as a tuple
    return (mag_x, mag_y, mag_z)


# Continuously read and display the IMU data
while True:
    try:
        accel_data = read_accel()
        gyro_data = read_gyro()
        mag_data = read_mag()

        print("Accelerometer (G): X = {0:.2f}, Y = {1:.2f}, Z = {2:.2f}".format(*accel_data))
        print("Gyroscope (deg/s): X = {0:.2f}, Y = {1:.2f}, Z = {2:.2f}".format(*gyro_data))
        print("Magnetometer (uT): X = {0:.2f}, Y = {1:.2f}, Z = {2:.2f}".format(*mag_data))
        print("------------------------------")

        # Wait for 0.5 seconds before reading again
        time.sleep(0.5)
    except KeyboardInterrupt:
