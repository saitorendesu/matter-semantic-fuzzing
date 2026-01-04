import RPi.GPIO as GPIO
import time
import sys

LED_PIN = 21  # GPIO 21 (Pin 40)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

if __name__ == "__main__":
    setup()
    try:
        # 引数: alert=長点灯(BUG), heartbeat=点滅(正常)
        mode = sys.argv[1] if len(sys.argv) > 1 else "heartbeat"
        if mode == "alert":
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(LED_PIN, GPIO.LOW)
        else:
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(LED_PIN, GPIO.LOW)
    finally:
        GPIO.cleanup()