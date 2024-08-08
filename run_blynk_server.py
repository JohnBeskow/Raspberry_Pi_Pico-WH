import BlynkLib
import time
from machine import Pin, ADC, reset
import gc

# Initialize ADC (Analog to Digital Converter) on pin 26
adc = ADC(Pin(26))

# Constants for voltage calculation
V_REF = 3.3
ADC_RESOLUTION = 65535

def read_temperature():
    adc_value = adc.read_u16()
    voltage = adc_value / ADC_RESOLUTION * V_REF
    temperature = (voltage - 0.5) * 100  # Assuming 10mV per degree with a 500mV offset
    return adc_value, voltage, temperature

def fan_on():
    # Code to turn on the fan using MOSFET
    print("Fan is ON")
    fan_pin = Pin(16, Pin.OUT)
    fan_pin.on()

def fan_off():
    # Code to turn off the fan using MOSFET
    print("Fan is OFF")
    fan_pin = Pin(16, Pin.OUT)
    fan_pin.off()

class ConnectToBlynk:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.blynk = None
        self.connect()

    def connect(self):
        print("Connecting to Blynk...")
        try:
            self.blynk = BlynkLib.Blynk(self.auth_token)
        except MemoryError:
            print("Memory error during connection setup")
            time.sleep(10)  # Delay to allow memory recovery
            self.blynk = None

    def run(self):
        try:
            while True:
                if self.blynk is not None:
                    try:
                        self.blynk.run()
                        adc_value, voltage, temperature = read_temperature()
                        print(f"ADC Value: {adc_value}")
                        print(f"Voltage: {voltage:.2f}V")
                        print(f"Temperature: {temperature:.1f} C")
                        self.blynk.virtual_write(1, temperature)
                        if temperature > 25:
                            fan_on()
                        else:
                            fan_off()
                        time.sleep(10)
                    except Exception as e:
                        print("Exception occurred in run loop:", e)
                        self.blynk = None
                        time.sleep(5)  # Wait before attempting reconnection
                        self.reconnect()
                else:
                    self.reconnect()
        except Exception as e:
            print("Unhandled exception:", e)
            reset()  # Reset the microcontroller to clear state

    def reconnect(self):
        print("Reconnecting to Blynk...")
        try:
            gc.collect()  # Explicitly run garbage collection to free memory
            if self.blynk is not None:
                try:
                    self.blynk.disconnect()  # Explicitly disconnect
                except:
                    pass
            self.blynk = None
            self.connect()
            if self.blynk is None:
                raise Exception("Failed to allocate memory for Blynk connection")
        except Exception as e:
            print("Error during reconnection:", e)
            time.sleep(10)  # Wait before retrying connection to avoid rapid failure loops
            reset()  # Reset the microcontroller if memory error persists to clear state

