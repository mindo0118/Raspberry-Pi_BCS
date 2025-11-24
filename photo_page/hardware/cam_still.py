from picamera2 import Picamera2
from datetime import datetime
import time
import os
import qrcode

PI_IP = "192.168.1.12"
#"172.16.116.196"  
PORT = 5000                
STATIC_BASE = "/home/pi/bcsm/static/photos"  

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

picam2.start()
time.sleep(2)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"photo_{timestamp}.jpg"

topic = input("select topic (family / friend / couple/ me): ").strip().lower()
folder_path = f"{STATIC_BASE}/{topic}"
os.makedirs(folder_path, exist_ok=True)
save_path = f"{folder_path}/{filename}"

picam2.capture_file(save_path)
picam2.close()

print(f" save complete: {save_path}")

photo_url = f"http://192.168.1.12:5000/static/photos/{topic}/{filename}"
print(f" photo URL: {photo_url}")

qr_filename = filename.replace(".jpg", ".png")
qr_folder = "/home/pi/bcsm/qrcodes"
os.makedirs(qr_folder, exist_ok=True)
qr_path = f"{qr_folder}/{qr_filename}"

qr = qrcode.make(photo_url)
qr.save(f"/home/pi/bcsm/qrcodes/{qr_filename}")
print(f" QR complete: {qr_path}")
