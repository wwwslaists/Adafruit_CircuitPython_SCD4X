# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_scd4x
from prometheus_client import start_http_server, Gauge

# Create Prometheus metrics
co2_gauge = Gauge('co2_ppm', 'CO2 concentration in ppm')
temperature_gauge = Gauge('temperature_celsius', 'Temperature in Celsius')
humidity_gauge = Gauge('relative_humidity_percentage', 'Relative Humidity in percentage')

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

# Start Prometheus HTTP server on port 8000
start_http_server(8181)

while True:
    if scd4x.data_ready:
        co2_value = scd4x.CO2
        temperature_value = scd4x.temperature
        humidity_value = scd4x.relative_humidity

        co2_gauge.set(co2_value)
        temperature_gauge.set(temperature_value)
        humidity_gauge.set(humidity_value)

        print("CO2: %d ppm" % co2_value)
        print("Temperature: %0.1f *C" % temperature_value)
        print("Humidity: %0.1f %%" % humidity_value)
        print()
    time.sleep(1)
