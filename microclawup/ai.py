# microclawup/ai.py
# Groq API integration for MicroPython / ESP32

import urequests
import ujson
from microclawup.config import GROQ_API_KEY

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"  # Free + ultra fast

SYSTEM_PROMPT = 'Reply ONLY with JSON. No extra text. Actions: led_on, led_off, blink, gpio_high, gpio_low, unknown. Examples: {"action":"led_on","pin":2} {"action":"blink","pin":2,"times":3} {"action":"gpio_high","pin":5} {"action":"unknown","message":"?"}. Default pin=2.'

def ask_grok(user_message):
    body = ujson.dumps({
        "model": MODEL,
        "max_tokens": 60,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + GROQ_API_KEY,
        "Content-Length": str(len(body))
    }
    try:
        r = urequests.post(GROQ_URL, headers=headers, data=body)
        raw_text = r.text
        print("AI raw:", raw_text)
        r.close()
        data = ujson.loads(raw_text)
        reply = data["choices"][0]["message"]["content"].strip()
        return reply
    except Exception as e:
        print("Groq API error:", e)
        return '{"action":"unknown","message":"API error"}'