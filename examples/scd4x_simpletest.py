import time
import board
import adafruit_scd4x
from flask import Flask, jsonify, Response
from prometheus_client import Gauge, generate_latest, CollectorRegistry

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")
time.sleep(5.4)
app = Flask(__name__)

# Create Prometheus metrics
co2_gauge = Gauge('co2_ppm', 'CO2 concentration in ppm')
temperature_gauge = Gauge('temperature_celsius', 'Temperature in Celsius')
humidity_gauge = Gauge('relative_humidity_percentage', 'Relative Humidity in percentage')

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    if scd4x.data_ready:
        co2_value = scd4x.CO2
        temperature_value = scd4x.temperature
        humidity_value = scd4x.relative_humidity

        data = {
            'co2_ppm': co2_value,
            'temperature_celsius': temperature_value,
            'relative_humidity_percentage': humidity_value
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Sensor data not ready'}), 503

@app.route('/metrics', methods=['GET'])
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
    app.run(host='0.0.0.0', port=5001)
