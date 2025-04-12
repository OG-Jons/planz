import network
import socket
import time
import machine
import ujson as json
from machine import Pin, ADC, I2C
import dht
from light_sensor import BH1750
import requests

CONFIG_FILE = "config.json"
POWER_PIN = Pin(16, Pin.OUT)
LED = Pin(2, Pin.OUT)
SOIL_SENSOR = ADC(0)
DHT_SENSOR = dht.DHT22(Pin(13))  # GPIO13 (D7)
I2C_BUS = I2C(scl=Pin(5), sda=Pin(4))  # GPIO5 (D1), GPIO4 (D2)


def read_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return None


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def connect_to_wifi(ssid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)
    for _ in range(10):
        if sta.isconnected():
            print("Wi-Fi connected:", sta.ifconfig()[0])
            return True
        print("Connecting...")
        time.sleep(1)
    print("Failed to connect.")
    return False


def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="PlantSensorSetup", authmode=network.AUTH_OPEN)
    print("Access Point running. Connect and go to http://4.3.2.1")


def receive_full_request(sock):
    request = b""
    while True:
        chunk = sock.recv(1024)
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
            content_length = int(line.split(":")[1].strip())
            break

    while len(body) < content_length:
        body += sock.recv(1024)

    return headers + "\r\n\r\n" + body.decode("utf-8")


def parse_form_data(request):
    try:
        body = request.split("\r\n\r\n", 1)[1]
        pairs = body.split('&')
        result = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                value = value.replace('%3A', ':').replace('%2F', '/').replace('+', ' ')
                result[key] = value
        return result
    except:
        return {}


def handle_config_request(client):
    request = receive_full_request(client)
    if "POST" in request:
        form = parse_form_data(request)
        ssid = form.get("wifi_ssid")
        password = form.get("wifi_password")
        server = form.get("server_address")
        plant_id = form.get("plant_id")
        plant_name = form.get("plant_name")
        plant_type = form.get("plant_type")

        if ssid and password and server:
            if connect_to_wifi(ssid, password):
                if not plant_id and plant_name and plant_type:
                    try:
                        r = requests.post(f"{server}/api/plants", json={
                            "name": plant_name,
                            "species": plant_type
                        })
                        if r.status_code == 200:
                            plant_id = r.json().get("id")
                        else:
                            raise Exception("Plant registration failed")
                    except Exception as e:
                        print("Error registering plant:", e)
                        client.send("HTTP/1.1 400\r\n\r\nPlant registration failed")
                        client.close()
                        return

                config = {
                    "wifi_ssid": ssid,
                    "wifi_password": password,
                    "server_address": server,
                    "plant_id": plant_id
                }
                save_config(config)
                client.send("HTTP/1.1 200 OK\r\n\r\nConfig saved. Rebooting...")
                client.close()
                time.sleep(1)
                machine.reset()
            else:
                client.send("HTTP/1.1 400 Bad Request\r\n\r\nWi-Fi connection failed.")
        else:
            client.send("HTTP/1.1 400 Bad Request\r\n\r\nMissing fields.")
    else:
        html = """\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html><body>
<h1>Plant Sensor Setup</h1>
<form method="POST">
SSID:<br><input name="wifi_ssid"><br>
Password:<br><input type="password" name="wifi_password"><br>
Server Address:<br><input name="server_address"><br>
Plant Name:<br><input name="plant_name"><br>
Plant Type:<br><input name="plant_type"><br>
OR Plant ID:<br><input name="plant_id"><br>
<input type="submit">
</form></body></html>"""
        client.send(html)
    client.close()


def run_setup_mode():
    start_access_point()
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Setup server listening...")

    while True:
        cl, addr = s.accept()
        print("Client connected:", addr)
        handle_config_request(cl)


def read_sensors():
    try:
        POWER_PIN.on()
        time.sleep(3)
        SOIL = SOIL_SENSOR.read()
        DHT_SENSOR.measure()
        TEMP = DHT_SENSOR.temperature()
        HUM = DHT_SENSOR.humidity()
        LIGHT = BH1750(I2C_BUS).luminance(BH1750.CONT_HIRES_1)
        POWER_PIN.off()
        return TEMP, HUM, LIGHT, SOIL
    except Exception as e:
        print("Sensor read failed:", e)
        return None, None, None, None


def run_normal_mode(config):
    if not connect_to_wifi(config["wifi_ssid"], config["wifi_password"]):
        print("Could not connect. Entering setup.")
        run_setup_mode()

    while True:
        TEMP, HUM, LIGHT, SOIL = read_sensors()
        if TEMP is not None:
            try:
                r = requests.post(f"{config['server_address']}/api/plants/{config['plant_id']}/stats", json={
                    "temperature_score": TEMP,
                    "humidity_score": HUM,
                    "sunlight_score": LIGHT,
                    "soil_moisture_score": SOIL
                })
                print("Data sent. Server response:", r.status_code)
            except Exception as e:
                print("Failed to send data:", e)
        time.sleep(60)


def main():
    config = read_config()
    if config and connect_to_wifi(config["wifi_ssid"], config["wifi_password"]):
        run_normal_mode(config)
    else:
        run_setup_mode()


main()
