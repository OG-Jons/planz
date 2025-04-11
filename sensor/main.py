import requests
from machine import Pin, ADC, I2C
import dht
import time
from light_sensor import BH1750
import network

# Power Pin
pwer = Pin(16, Pin.OUT)  # D0 corresponds to GPIO16

# Enable LED on ESP8266
led = Pin(2, Pin.OUT)  # D4 corresponds to GPIO2

# Soil Moisture Sensor (Analog) - Pin A0
soil_sensor = ADC(0)  # ESP8266 has only ADC0 (A0) for analog input

# DHT22 Sensor - Pin D4
dht_sensor = dht.DHT22(Pin(13))  # D4 corresponds to GPIO2

print("Connecting to wifi...")
### Connect to WI-FI
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect("Nothing", "bigchonker100")
# while not sta_if.isconnected():
#     pass

print("Connected to wifi")

def read_dht():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
    except Exception as e:
        print("Error reading DHT22:", e)
        temperature, humidity = None, None
    return temperature, humidity

while True:
    try:
        print("Powering on Sensors...")
        # Power on the sensors
        pwer.on()
        time.sleep(5)  # Wait for the sensors to power on and stabilize

        print("Reading Sensor values...")
        # # Read Soil Moisture
        soil_value = soil_sensor.read()

        # Read Temperature and Humidity
        temperature, humidity = read_dht()

        # Read Light Intensity
        # BH1750 Sensor - I2C on D1 (SCL) and D2 (SDA)
        i2c = I2C(scl=Pin(5), sda=Pin(4))  # Force hardware I2C
        light_sensor = BH1750(i2c)

        light_level = light_sensor.luminance(BH1750.CONT_HIRES_1)

        # Power off the sensors
        print("Powering off sensors...")
        pwer.off()

        # Print Values
        print("Temperature: {} C".format(temperature))
        print("Humidity: {} %".format(humidity))
        print("Soil Moisture: {}".format(soil_value))
        print("Light Intensity: {} lx".format(light_level))

        # Send a POst request to 192.168.1.124, with the following body:
        ### {
        # humidity_score: 0
        # sunlight_score: 0
        # temperature_score: 0
        # soil_moisture_score: 0
        #}
        print("Sending data to server...")
        # r = requests.post("http://10.95.1.8:8000/api/plants/1/stats", json={
        #     "humidity_score": humidity,
        #     "sunlight_score": light_level,
        #     "temperature_score": temperature,
        #     "soil_moisture_score": soil_value
        # })
        # print(r.status_code)
        print("Waiting 60 seconds...")
        time.sleep(60)  # Wait 30 seconds before the next reading

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
