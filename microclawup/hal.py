# microclawup/hal.py
# Hardware Abstraction Layer — LED + GPIO control

from machine import Pin
import time

# Pin cache — avoid re-creating Pin objects
_pins = {}

def _get_pin(pin_num, mode=Pin.OUT):
    if pin_num not in _pins:
        _pins[pin_num] = Pin(pin_num, mode)
    return _pins[pin_num]

# ── LED ──────────────────────────────────────────

def led_on(pin=2):
    _get_pin(pin).value(1)
    print("LED ON pin", pin)

def led_off(pin=2):
    _get_pin(pin).value(0)
    print("LED OFF pin", pin)

def led_blink(pin=2, times=3, delay=0.3):
    p = _get_pin(pin)
    for _ in range(times):
        p.value(1)
        time.sleep(delay)
        p.value(0)
        time.sleep(delay)
    print("Blinked {} times on pin {}".format(times, pin))

# ── General GPIO ──────────────────────────────────

def gpio_high(pin):
    _get_pin(pin).value(1)
    print("GPIO {} HIGH".format(pin))

def gpio_low(pin):
    _get_pin(pin).value(0)
    print("GPIO {} LOW".format(pin))

def gpio_read(pin):
    p = Pin(pin, Pin.IN)
    val = p.value()
    print("GPIO {} READ: {}".format(pin, val))
    return val