import paho.mqtt.client as mqtt
import base64
import time

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "test/hivemq/minjung"
IMAGE_PATH = "/home/pi/bcsm/static/photos/couple/test.jpg"

client = mqtt.Client()
client.connect(BROKER, PORT)
client.loop_start()

with open(IMAGE_PATH, "rb") as img:
    encoded = base64.b64encode(img.read()).decode("utf-8")
    client.publish(TOPIC, encoded)
    print("tjdrhd")

time.sleep(1)
client.loop_stop()
client.disconnect()
