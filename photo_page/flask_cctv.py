from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2
import numpy as np
import time

app = Flask(__name__)

picam2 = None

def initialize_camera():
    global picam2
    if picam2 is None:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
        picam2.configure(config)
        picam2.start()
        time.sleep(2)  # 카메라 초기화 대기
def generate_frames():
    global picam2
    if picam2 is None:
        initialize_camera()
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('flask_cctv.html')

@app.route('/video_feed/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        initialize_camera()
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        if picam2:
            picam2.stop()
            picam2.close()
