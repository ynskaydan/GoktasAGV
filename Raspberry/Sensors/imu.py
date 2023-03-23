import smbus
import time

# initialize the I2C bus
bus = smbus.SMBus(1)

# set the address of the IMU sensor
address = 0x1e

# write to the configuration registers of the magnetometer
bus.write_byte_data(address, 0x00, 0x18)
bus.write_byte_data(address, 0x01, 0x20)
bus.write_byte_data(address, 0x02, 0x00)

# read the accelerometer data from the IMU sensor
def read_accelerometer():
    # set the address of the accelerometer
    address = 0x1d

    # read the raw accelerometer data from the sensor
    x = bus.read_byte_data(address, 0x28)
    y = bus.read_byte_data(address, 0x2a)
    z = bus.read_byte_data(address, 0x2c)

    # convert the raw accelerometer data to G units
    x = (x / 63.0) - 1.0
    y = (y / 63.0) - 1.0
    z = (z / 63.0) - 1.0

    # return the accelerometer data as a tuple
    return (x, y, z)

# read and calibrate the magnetometer data from the IMU sensor
def read_magnetometer():
    # set the address of the magnetometer
    address = 0x1e

    # read the raw magnetometer data from the sensor
    x = bus.read_byte_data(address, 0x03) << 8 | bus.read_byte_data(address, 0x04)
    z = bus.read_byte_data(address, 0x05) << 8 | bus.read_byte_data(address, 0x06)
    y = bus.read_byte_data(address, 0x07) << 8 | bus.read_byte_data(address, 0x08)

    # calibrate the magnetometer data
    x = (x - 152.0) / 315.0
    y = (y - 81.0) / 335.0
    z = (z - 110.0) / 250.0

    # return the magnetometer data as a tuple
    return (x, y, z)

# continuously read and display the accelerometer and magnetometer data
while True:
    # read the accelerometer and magnetometer data
    accel_data = read_accelerometer()
    mag_data = read_magnetometer()

    # print the accelerometer and magnetometer data
    print("Accelerometer data: ", accel_data)
    print("Magnetometer data: ", mag_data)

    # wait for 1 second before reading the data again
    time.sleep(1)
