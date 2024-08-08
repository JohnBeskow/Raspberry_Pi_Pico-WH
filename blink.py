import machine
import time

led = machine.Pin('LED', machine.Pin.OUT)

def failed_blink():
    count = 0
    while count < 3:
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
        count += 1

def connected_blink():
    for _ in range(3):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

