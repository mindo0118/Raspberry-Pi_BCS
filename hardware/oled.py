import board
import busio
import digitalio
import adafruit_ssd1306
from PIL import Image
import time
import threading

# bitbangio 소프트웨어 I2c용
from adafruit_bitbangio import I2C as BitbangI2C

# OLED 1: 하드웨어 I2C (GPIO2=SDA, GPIO3=SCL)
i2c1 = busio.I2C(board.SCL, board.SDA)
oled1 = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c1)

# OLED 2: 소프트웨어 I2C (GPIO5=SDA, GPIO6=SCL)
i2c2 = BitbangI2C(board.D6, board.D5)
oled2 = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c2)

images1 = ["logo.jpeg", "wink.png", "sad.jpeg"]
images2 = ["v.jpg", "group pose.jpg", "heart pose.jpg"]

def slide_show(oled, images, delay):
    while True:
        for path in images:
            try:
                img = Image.open(path).convert("1").resize((128, 64))
                oled.fill(0)
                oled.image(img)
                oled.show()
            except Exception as e:
                print(f"{oled=} 이미지 로딩 실패: {e}")
            time.sleep(delay)

#OLED별 슬라이드 스레드 시작
thread1 = threading.Thread(target=slide_show, args=(oled1, images1, 3))
thread2 = threading.Thread(target=slide_show, args=(oled2, images2, 3))

thread1.start()
thread2.start()
