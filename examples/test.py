from prometheus_client import start_http_server, Gauge
import time
import board
import adafruit_scd4x


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

# Create a Gauge metric for temperature readings
co2_gauge = Gauge('co2_ppm', 'CO2 concentration in ppm')
temperature_gauge = Gauge('temperature_celsius', 'Temperature in Celsius')
humidity_gauge = Gauge('relative_humidity_percentage', 'Relative Humidity in percentage')

time.sleep(5.4)
mylist = [float(scd4x.CO2),scd4x.relative_humidity,scd4x.temperature]


print(mylist)

def simulate_sensor():
    while True:
        # Simulate a temperature reading between 0 and 100 degrees Celsius
        co2_gauge.set(scd4x.CO2)
        temperature_gauge.set(scd4x.temperature)
        humidity_gauge.set(scd4x.relative_humidity)
       

if __name__ == '__main__':
    # Start an HTTP server to expose metrics
    start_http_server(5000)
    simulate_sensor()
    