import network
import time
from secrets import secrets
from blink import connected_blink, failed_blink, led

def do_connect(ssid=secrets['ssid'], psk=secrets['password']):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)
    
    # wait for connect or fail
    wait = 10
    while wait > 0:
        led.on()
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        led.off()
    
    # handle connection error
    if wlan.status() != 3:
        failed_blink()
        raise RuntimeError('WiFi connection failed')
    else:
        ip = wlan.ifconfig()[0]
        print('connected')
        print('network config:', ip)
        connected_blink()
        return ip

