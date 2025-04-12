import requests
from machine import Pin, ADC, I2C
import dht
import time
from light_sensor import BH1750
import network
import ujson as json
import uos

# Power Pin
pwer = Pin(16, Pin.OUT)  # D0 corresponds to GPIO16

# Enable LED on ESP8266
led = Pin(2, Pin.OUT)  # D4 corresponds to GPIO2

# Soil Moisture Sensor (Analog) - Pin A0
soil_sensor = ADC(0)  # ESP8266 has only ADC0 (A0) for analog input

# DHT22 Sensor - Pin D4
dht_sensor = dht.DHT22(Pin(13))  # D4 corresponds to GPIO2

# File to store configuration
CONFIG_FILE = "config.json"

def parse_query_string(query):
    body = query.split("\r\n\r\n")[1]
    pairs = body.split('&')
    result = {}
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key, value = pair, ''
        # URL decoding
        value = value.replace('%3A', ':').replace('%2F', '/')
        result[key] = value
    return result

def receive_full_request(client_socket):
    request = b""
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        request += chunk
        if b"\r\n\r\n" in request:
            break

    header_end = request.find(b"\r\n\r\n")
    headers = request[:header_end].decode("utf-8")
    body = request[header_end + 4:]

    content_length = 0
    for line in headers.split("\r\n"):
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":")[1].strip())
            except:
                content_length = 0
            break

    while len(body) < content_length:
        more = client_socket.recv(1024)
        if not more:
            break
        body += more

    full_request = request[:header_end] + b"\r\n\r\n" + body
    return full_request.decode("utf-8")

def read_dht():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
    except Exception as e:
        print("Error reading DHT22:", e)
        temperature, humidity = None, None
    return temperature, humidity

# Function to read configuration
def read_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None

# Function to save configuration
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Function to start Wi-Fi access point
def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="PlantSensorSetup", authmode=network.AUTH_OPEN)
    print("Access Point started. Connect to 'PlantSensorSetup' and visit 4.3.2.1")
    return ap

def connect_to_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    timeout = 10  # Timeout in seconds
    while not sta_if.isconnected() and timeout > 0:
        print("Attempting to connect to Wi-Fi...")
        time.sleep(1)
        timeout -= 1
    if sta_if.isconnected():
        print("Connected to Wi-Fi")
        print("IP Address:", sta_if.ifconfig()[0])
        return True
    else:
        print("Failed to connect to Wi-Fi")
        return False

def start_configuration_page():
    import socket
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Configuration page running on http://{}".format(network.WLAN(network.STA_IF).ifconfig()[0]))

    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        request = receive_full_request(cl)
        if "POST" in request:
            data = parse_query_string(request)
            wifi_ssid = data.get("wifi_ssid")
            wifi_password = data.get("wifi_password")
            server_address = data.get("server_address")
            plant_name = data.get("plant_name")
            plant_type = data.get("plant_type")
            plant_id = data.get("plant_id")

            if wifi_ssid and wifi_password:
                config = {
                    "wifi_ssid": wifi_ssid,
                    "wifi_password": wifi_password,
                    "server_address": server_address,
                    "plant_id": plant_id,
                    "plant_name": plant_name,
                    "plant_type": plant_type,
                }
                save_config(config)
                cl.send("HTTP/1.1 200 OK\r\n\r\nConfiguration saved. Rebooting...")
                cl.close()
                machine.reset()
            else:
                cl.send("HTTP/1.1 400 Bad Request\r\n\r\nInvalid data.")
        else:
            html = """<!DOCTYPE html>
            <html>
            <body>
            <h1>Plant Sensor Configuration</h1>
            <form method="POST" action="/">
              <label>Wi-Fi SSID:</label><br>
              <input type="text" name="wifi_ssid"><br>
              <label>Wi-Fi Password:</label><br>
              <input type="password" name="wifi_password"><br>
              <label>Server Address:</label><br>
              <input type="text" name="server_address"><br>
              <label>Plant Name:</label><br>
              <input type="text" name="plant_name"><br>
              <label>Plant Type:</label><br>
              <input type="text" name="plant_type"><br>
              <label>OR Plant ID:</label><br>
              <input type="text" name="plant_id"><br>
              <input type="submit" value="Submit">
            </form>
            </body>
            </html>"""
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
        cl.close()

# Function to start web server for configuration
def start_web_server():
    import socket
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server running on http://4.3.2.1")

    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        request = receive_full_request(cl)
        if "POST" in request:
            print("Received POST request")
            print("Request:", request)
            data = parse_query_string(request)
            print("Parsed data:", data)
            wifi_ssid = data.get("wifi_ssid")
            wifi_password = data.get("wifi_password")
            server_address = data.get("server_address")
            plant_name = data.get("plant_name")
            plant_type = data.get("plant_type")
            plant_id = data.get("plant_id")
            print("Data received:", data)

            if plant_id:
                config = {
                    "wifi_ssid": wifi_ssid,
                    "wifi_password": wifi_password,
                    "server_address": server_address,
                    "plant_id": plant_id,
                }
                save_config(config)
                cl.send("HTTP/1.1 200 OK\r\n\r\nConfiguration saved. Rebooting...")
                cl.close()
                machine.reset()
            elif plant_name and plant_type:
                # Connect to WI-Fi

                # Register plant and get Plant ID
                response = requests.post(f"{server_address}/api/plants", json={
                    "name": plant_name,
                    "species": plant_type
                })
                if response.status_code == 200:
                    plant_id = response.json().get("id")
                    config = {
                        "wifi_ssid": wifi_ssid,
                        "wifi_password": wifi_password,
                        "server_address": server_address,
                        "plant_id": plant_id,
                    }
                    save_config(config)
                    cl.send("HTTP/1.1 200 OK\r\n\r\nConfiguration saved. Rebooting...")
                    cl.close()
                    machine.reset()
                else:
                    cl.send("HTTP/1.1 400 Bad Request\r\n\r\nFailed to register plant.")
            else:
                cl.send("HTTP/1.1 400 Bad Request\r\n\r\nInvalid data.")
        else:
            html = """<!DOCTYPE html>
            <html>
            <body>
            <h1>Plant Sensor Setup</h1>
            <form method="POST" action="/">
              <label>Wi-Fi SSID:</label><br>
              <input type="text" name="wifi_ssid"><br>
              <label>Wi-Fi Password:</label><br>
              <input type="password" name="wifi_password"><br>
              <label>Server Address:</label><br>
              <input type="text" name="server_address"><br>
              <label>Plant Name:</label><br>
              <input type="text" name="plant_name"><br>
              <label>Plant Type:</label><br>
              <input type="text" name="plant_type"><br>
              <label>OR Plant ID:</label><br>
              <input type="text" name="plant_id"><br>
              <input type="submit" value="Submit">
            </form>
            </body>
            </html>"""
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
        cl.close()

# Main function
def main():
    config = read_config()
    if not config or not connect_to_wifi(config["wifi_ssid"], config["wifi_password"]):
        print("Starting Access Point...")
        ap = start_access_point()
        start_web_server()
    else:
        print("Starting Configuration Page...")
        start_configuration_page()

        # Normal operation loop
        while True:
            try:
                print("Powering on Sensors...")
                pwer.on()
                time.sleep(5)

                print("Reading Sensor values...")
                soil_value = soil_sensor.read()
                temperature, humidity = read_dht()
                i2c = I2C(scl=Pin(5), sda=Pin(4))
                light_sensor = BH1750(i2c)
                light_level = light_sensor.luminance(BH1750.CONT_HIRES_1)

                print("Powering off sensors...")
                pwer.off()

                print("Sending data to server...")
                r = requests.post(f"{config['server_address']}/api/plants/{config['plant_id']}/stats", json={
                    "humidity_score": humidity,
                    "sunlight_score": light_level,
                    "temperature_score": temperature,
                    "soil_moisture_score": soil_value
                })
                print("Response:", r.status_code)
                time.sleep(60)
            except Exception as e:
                print("Error:", e)
                time.sleep(5)

# Run the main function
main()