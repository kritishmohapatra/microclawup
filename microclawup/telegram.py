# microclawup/telegram.py
import urequests
import ujson
import network
import time
from microclawup.agent_core import execute
from microclawup.wifi import connect_wifi
import microclawup.config as config

last_update_id = 0

def get_base_url():
    return "https://api.telegram.org/bot" + config.BOT_TOKEN

def send_message(text):
    url = get_base_url() + "/sendMessage"
    body = ujson.dumps({"chat_id": config.CHAT_ID, "text": text})
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body))
    }
    try:
        r = urequests.post(url, headers=headers, data=body)
        print("Send status:", r.status_code)
        print("Send response:", r.text)
        r.close()
    except Exception as e:
        print("Send error:", e)

def get_messages():
    global last_update_id
    url = get_base_url() + "/getUpdates?offset={}&timeout=5".format(last_update_id + 1)
    try:
        r = urequests.get(url)
        data = r.json()
        r.close()
    except Exception as e:
        print("Fetch error:", e)
        return

    results = data.get("result", [])
    if not results:
        return

    for msg in results:
        last_update_id = msg["update_id"]
        text = msg.get("message", {}).get("text", "")
        if not text:
            continue
        print("Telegram CMD:", text)
        response = execute(text)
        print("Sending reply:", response)
        send_message(response)

def start_telegram():
    connect_wifi()
    print("Telegram Agent Started")
    send_message("MicroClawUP Online")

    wlan = network.WLAN(network.STA_IF)

    while True:
        if not wlan.isconnected():
            print("WiFi lost, reconnecting...")
            connect_wifi()
        get_messages()
        time.sleep(2)