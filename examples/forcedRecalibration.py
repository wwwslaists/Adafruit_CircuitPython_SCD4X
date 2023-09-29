from prometheus_client import start_http_server, Gauge
import time 
import board
import adafruit_scd4x
from datetime import datetime


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

sample_counter = 0
while sample_counter < 20:     
       time.sleep(30)
       now = datetime.now()
       current_time = now.strftime("%H:%M:%S")
       print("Current Time =", current_time)
       mylist = [float(scd4x.CO2),scd4x.relative_humidity,scd4x.temperature]
       print(mylist)
       if sample_counter == 10:
        print('start calibrate')
        scd4x.stop_periodic_measurement()
        time.sleep(2)
        scd4x.force_calibration = 400
        time.sleep(10)
        scd4x.start_periodic_measurement()
        print('end calibrate')
        time.sleep(2)
       sample_counter += 1


       
