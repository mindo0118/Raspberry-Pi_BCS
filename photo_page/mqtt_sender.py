import paho.mqtt.client as mqtt
import base64
import json
import os
from datetime import datetime

topic_label = None
filename = None

with open("/home/pi/bcsm/current_topic.txt", "r") as f:
    topic_label = f.read().strip()

with open("/home/pi/bcsm/current_filename.txt", "r") as f:
    filename = f.read().strip()

photo_path = f"/home/pi/bcsm/static/photos/{topic_label}/{filename}"

BROKER = "172.16.111.172" 
PORT = 1883
TOPIC = "photo/data"

with open(photo_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode('utf-8')

payload = {
    "filename": filename,
    "topic": topic_label,
    "image": encoded
}

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.publish(TOPIC, json.dumps(payload))
client.disconnect()

print(f"[MQTT send complete] {filename} → topic: {topic_label}")

