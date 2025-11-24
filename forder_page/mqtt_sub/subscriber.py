import paho.mqtt.client as mqtt
from paho.mqtt.client import Client, MQTTMessage, CallbackAPIVersion

def on_connect(client, userdata, flags, rc):
	print("Connected with result code", rc)
	client.subscribe("test/topic")

def on_message(client,userdata,msg):
	print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

broker_address = "0.0.0.0"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("0.0.0.0", 1883, 60)

client.loop_forever()
