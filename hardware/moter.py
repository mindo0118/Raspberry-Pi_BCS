import RPi.GPIO as GPIO
import time

SERVO1 = 24
BTN1_UP = 22
BTN1_DOWN = 27

SERVO2 = 25
BTN2_UP = 17
BTN2_DOWN = 18

LED1_UP = 26
LED1_DOWN = 19
LED2_UP = 16
LED2_DOWN = 12

GPIO.setmode(GPIO.BCM)
for pin in [SERVO1, SERVO2]:
    GPIO.setup(pin, GPIO.OUT)

for pin in [BTN1_UP, BTN1_DOWN, BTN2_UP, BTN2_DOWN]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in [LED1_UP, LED1_DOWN, LED2_UP, LED2_DOWN]:
    GPIO.setup(pin, GPIO.OUT)
    
pwm1 = GPIO.PWM(SERVO1, 50)
pwm2 = GPIO.PWM(SERVO2, 50)
pwm1.start(0)
pwm2.start(0)

angle1 = 90
angle2 = 90


def angle_to_duty(a):
    return 2 + (a / 18.0)

def update_servo(pwm, angle):
    pwm.ChangeDutyCycle(angle_to_duty(angle))
    time.sleep(0.03) 
    pwm.ChangeDutyCycle(0) 

try:
    print("버튼을 눌러서 서보모터 실행")
    while True:
        if GPIO.input(BTN1_UP) == GPIO.LOW and angle1 < 180:
            angle1 += 1
            update_servo(pwm1, angle1)
            GPIO.output(LED1_UP, GPIO.HIGH)
            
        elif GPIO.input(BTN1_DOWN) == GPIO.LOW and angle1 > 0:
            angle1 -= 1
            update_servo(pwm1, angle1)
            GPIO.output(LED1_DOWN, GPIO.HIGH)

        if GPIO.input(BTN2_UP) == GPIO.LOW and angle2 < 180:
            angle2 += 1
            update_servo(pwm2, angle2)
            GPIO.output(LED2_UP, GPIO.HIGH)

        elif GPIO.input(BTN2_DOWN) == GPIO.LOW and angle2 > 0:
            angle2 -= 1
            update_servo(pwm2, angle2)
            GPIO.output(LED2_DOWN, GPIO.HIGH)
            
        else:
             GPIO.output(LED1_UP, GPIO.LOW)
             GPIO.output(LED1_DOWN, GPIO.LOW)
             GPIO.output(LED2_UP, GPIO.LOW)
             GPIO.output(LED2_DOWN, GPIO.LOW)
        
        time.sleep(0.005)

except KeyboardInterrupt:
    print("\n?? 종료")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
