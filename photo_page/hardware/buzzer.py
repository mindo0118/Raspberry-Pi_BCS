import RPi.GPIO as GPIO
import time
import os

# Pin configuration
BUTTON_PIN = 21  # GPIO pin for button
BUZZER_PIN = 20  # GPIO pin for buzzer

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Press the button to sound the buzzer!")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn on buzzer
            print("Button pressed! Buzzer ON")
            os.system("python3 /home/pi/bcsm/cam_still.py")
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)   # Turn off buzzer
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
    
finally:
    GPIO.cleanup()
