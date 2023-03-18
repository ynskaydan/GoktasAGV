import smbus2
from mpu6050 import MPU6050
from bme280 import BME280

# I2C bağlantısı
bus = smbus2.SMBus(1)

# MPU6050 sensörü için nesne oluşturma
mpu = MPU6050(bus)

# BME280 sensörü için nesne oluşturma
bme = BME280(i2c_dev=bus)

# Sensörlerden veri okuma
acceleration_data = mpu.get_accel_data()
gyroscope_data = mpu.get_gyro_data()
magnetic_data = mpu.get_mag_data()

temperature_data = bme.get_temperature()
pressure_data = bme.get_pressure()

# Verileri ekrana yazdırma
print("Acceleration: ({0:.2f}, {1:.2f}, {2:.2f})".format(acceleration_data['x'], acceleration_data['y'], acceleration_data['z']))
print("Gyroscope: ({0:.2f}, {1:.2f}, {2:.2f})".format(gyroscope_data['x'], gyroscope_data['y'], gyroscope_data['z']))
print("Magnetic: ({0:.2f}, {1:.2f}, {2:.2f})".format(magnetic_data['x'], magnetic_data['y'], magnetic_data['z']))
print("Temperature: {0:.2f} C".format(temperature_data))
print("Pressure: {0:.2f} hPa".format(pressure_data))
