from flask import Flask, render_template, jsonify
import threading
import os
import base64
from datetime import datetime
import paho.mqtt.client as mqtt

# ====== Flask ======
app = Flask(__name__, static_url_path='/static')
PHOTO_BASE = "static/photos"
TOPIC_LIST = ["couple", "family", "friend", "me"]

@app.route('/')
def index():
    topics = [folder for folder in os.listdir(PHOTO_BASE) if os.path.isdir(os.path.join(PHOTO_BASE, folder))]
    return render_template('indexindex.html', topics=topics)

@app.route('/photos/json/<topic>')
def photos_by_topic(topic):
    topic_path = os.path.join(PHOTO_BASE, topic)
    images = os.listdir(topic_path) if os.path.exists(topic_path) else []
    images = [f"/static/photos/{topic}/{img}" for img in sorted(images)
              if img.lower().endswith((".jpg", ".jpeg", ".png"))]
    return jsonify({"images": images})

# ====== MQTT ======

def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connected to broker")
    for topic in TOPIC_LIST:
        client.subscribe(f"test/hivemq/{topic}")
        print(f"[MQTT] Subscribed to topic: test/hivemq/{topic}")

def on_message(client, userdata, msg):
    topic_name = msg.topic.split("/")[-1]
    if topic_name in TOPIC_LIST:
        folder = os.path.join(PHOTO_BASE, topic_name)
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mqtt_{timestamp}.jpg"
        path = os.path.join(folder, filename)

        try:
            image_data = base64.b64decode(msg.payload)
            with open(path, "wb") as f:
                f.write(image_data)
            print(f"[MQTT] Image saved to: {path}")
        except Exception as e:
            print(f"[MQTT] Error decoding image: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_forever()

# ====== go ======
if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()
    app.run(host='0.0.0.0', port=5000)
