from flask import Flask, render_template, Response, request, redirect, url_for
from datetime import datetime
import os
import qrcode
from picamera2 import Picamera2
import cv2
import threading
import RPi.GPIO as GPIO
import time
import socket

app = Flask(__name__)
PHOTO_DIR = 'static/photos'
QR_DIR = 'static/qrcodes'
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)

BUTTON_PIN = 21
BUZZER_PIN = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

latest_filename = ""
latest_topic = "family"
capture_done = False

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def button_listener():
    global latest_filename, latest_topic, capture_done
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.2)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            folder = os.path.join(PHOTO_DIR, latest_topic)
            os.makedirs(folder, exist_ok=True)
            save_path = os.path.join(folder, filename)

            picam2.capture_file(save_path)
            
            ngrok_url = get_ngrok_url()
            if ngrok_url:
                photo_url = f"{ngrok_url}/static/photos/{latest_topic}/{filename}"
            else:
                ip_address = get_local_ip()
                photo_url = f"http://{ip_address}:5000/static/photos/{latest_topic}/{filename}"

            qr_img = qrcode.make(photo_url)
            qr_filename = filename.replace('.jpg', '.png')
            qr_path = os.path.join(QR_DIR, qr_filename)
            qr_img.save(qr_path)

            latest_filename = filename
            capture_done = True
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.5)

        time.sleep(0.1)

def get_ngrok_url():
    try:
        res = requests.get("http://localhost:4040/api/tunnels")
        tunnels = res.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except:
        return None

@app.route('/')
def flask_cctv():
    return render_template('flask_cctv.html', topic=latest_topic)

def generate():
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_topic', methods=['POST'])
def set_topic():
    global latest_topic
    latest_topic = request.form.get('topic')
    return redirect(url_for('flask_cctv'))

@app.route('/capture_result')
def capture_result():
    global latest_filename, latest_topic, capture_done
    capture_done = False
    qr_filename = latest_filename.replace('.jpg', '.png')
    return render_template('capture.html', filename=latest_filename, topic=latest_topic, qr_filename=qr_filename)

@app.route('/trigger_capture', methods=['POST'])
def trigger_capture():
    global capture_done
    capture_done = True
    return '', 204

@app.route('/status')
def status():
    global capture_done
    return {'done': capture_done}

@app.route('/qr_view')
def qr_view():
    global latest_filename, latest_topic
    if not latest_filename:
        return "No file yet", 400

    qr_filename = latest_filename.replace('.jpg', '.png')
    qr_path = os.path.join(QR_DIR, qr_filename)
    photo_path = f"/static/photos/{latest_topic}/{latest_filename}"
    photo_full_path = os.path.join(PHOTO_DIR, latest_topic, latest_filename)

    # MQTT
    try:
        import paho.mqtt.client as mqtt
        import base64
        BROKER = "broker.hivemq.com"
        PORT = 1883
        TOPIC = f"test/hivemq/{latest_topic}"

        client = mqtt.Client()
        client.connect(BROKER, PORT)
        client.loop_start()

        with open(photo_full_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode("utf-8")
            client.publish(TOPIC, encoded)
            print(f"[MQTT] Sent from /qr_view to {TOPIC}")

        import time
        time.sleep(1)
        client.loop_stop()
        client.disconnect()

    except Exception as e:
        print(f"[MQTT] Failed in /qr_view: {e}")

    if not os.path.exists(qr_path):
        return f"QR file not found: {qr_path}", 404

    return render_template('qr_view.html',
                           qr_filename=qr_filename,
                           photo_path=photo_path)


if __name__ == '__main__':
    threading.Thread(target=button_listener, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
