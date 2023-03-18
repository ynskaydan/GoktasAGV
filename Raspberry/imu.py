import smbus2
import time

# Register addresses
MPU9250_ADDRESS = 0x68
MPU9250_PWR_MGMT_1 = 0x6B
MPU9250_ACCEL_XOUT_H = 0x3B
MPU9250_GYRO_XOUT_H = 0x43

AK8963_ADDRESS = 0x0C
AK8963_CNTL1 = 0x0A
AK8963_HXL = 0x03

bus = smbus2.SMBus(1)  # Use i2c bus 1

# Configure MPU9250
bus.write_byte_data(MPU9250_ADDRESS, MPU9250_PWR_MGMT_1, 0x00)

while True:
    # Read accelerometer data
    accel_x_h = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_ACCEL_XOUT_H)
    accel_x_l = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_ACCEL_XOUT_H + 1)
    accel_x = (accel_x_h << 8) | accel_x_l
    accel_x = accel_x / 16384.0

    # Read gyroscope data
    gyro_x_h = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_GYRO_XOUT_H)
    gyro_x_l = bus.read_byte_data(MPU9250_ADDRESS, MPU9250_GYRO_XOUT_H + 1)
    gyro_x = (gyro_x_h << 8) | gyro_x_l
    gyro_x = gyro_x / 131.0

    # Read magnetometer data
    bus.write_byte_data(AK8963_ADDRESS, AK8963_CNTL1, 0x16)  # Enter continuous measurement mode
    time.sleep(0.1)  # Wait for measurement to stabilize
    mag_x_l = bus.read_byte_data(AK8963_ADDRESS, AK8963_HXL)
    mag_x_h = bus.read_byte_data(AK8963_ADDRESS, AK8963_HXL + 1)
    mag_x = (mag_x_h << 8) | mag_x_l

    print("Accelerometer X: %.2f" % accel_x)
    print("Gyroscope X: %.2f" % gyro_x)
    print("Magnetometer X: %d" % mag_x)

    time.sleep(0.1)  # Wait for next reading
