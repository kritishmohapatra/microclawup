# microclawup/wifi.py
import network
import time
from microclawup.config import WIFI_SSID, WIFI_PASS

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return True

    print("Connecting to WiFi:", WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    for i in range(20):
        if wlan.isconnected():
            print("WiFi Connected:", wlan.ifconfig())
            return True
        print(".", end="")
        time.sleep(1)

    print("\nWiFi Failed!")
    return False