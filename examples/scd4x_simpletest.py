# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_scd4x
from prometheus_client import Gauge, generate_latest, CollectorRegistry
from flask import Flask, Response

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

app = Flask(__name__)

@app.route('/metrics')
def prometheus_metrics():
    registry = CollectorRegistry()
    co2_value = scd4x.CO2
    temperature_value = scd4x.temperature
    humidity_value = scd4x.relative_humidity

    co2_gauge.set(co2_value)
    temperature_gauge.set(temperature_value)
    humidity_gauge.set(humidity_value)

    return Response(generate_latest(registry), content_type='text/plain')

if __name__ == '__main__':
    # Start the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)
