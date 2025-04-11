import random

import requests
data1 = {
    "humidity_score": random.randint(50, 60),
    "sunlight_score": random.randint(20, 60),
    "temperature_score": random.randint(20, 30),
    "soil_moisture_score": random.randint(430, 520),
}
data2 = {
    "humidity_score": random.randint(20, 60),
    "sunlight_score": random.randint(50, 60),
    "temperature_score": random.randint(20, 30),
    "soil_moisture_score": random.randint(260, 430),
}
data3 = {
    "humidity_score": random.randint(40, 45),
    "sunlight_score": random.randint(55, 60),
    "temperature_score": random.randint(20, 30),
    "soil_moisture_score": random.randint(0, 60),
}

r1 = requests.post("http://localhost:8000/api/plants/1/stats", json=data1)
r2 = requests.post("http://localhost:8000/api/plants/2/stats", json=data2)
# r3 = requests.post("http://localhost:8000/api/plants/3/stats", json=data3)