# microclawup/agent_core.py
import ujson
from microclawup.hal import led_on, led_off, led_blink, gpio_high, gpio_low
from microclawup.storage import save_data, load_data
from microclawup.ai import ask_grok

_pin_state = {}

def _set_state(pin, state):
    _pin_state[pin] = state
    save_data("pin_{}".format(pin), state)

def get_status():
    if not _pin_state:
        for pin in [2, 4, 5, 12, 13]:
            val = load_data("pin_{}".format(pin))
            if val:
                _pin_state[pin] = val
    if not _pin_state:
        return "No pins active yet"
    lines = ["PIN STATUS"]
    for pin, state in _pin_state.items():
        lines.append("Pin {}: {}".format(pin, state))
    return "\n".join(lines)

def execute(user_input):
    if user_input.strip() == "/status":
        return get_status()

    if user_input.strip() == "/help":
        return (
            "MicroClawUP Commands:\n"
            "- Natural language: turn on light, blink 3 times, pin 5 high\n"
            "- /status - pin states\n"
            "- /help - this message"
        )

    print("User said:", user_input)
    raw = ask_grok(user_input)
    print("AI replied:", raw)

    try:
        cmd = ujson.loads(raw)
    except Exception as e:
        print("JSON parse error:", e)
        return "Try again"

    action = cmd.get("action", "unknown")
    pin = cmd.get("pin", 2)

    if action == "led_on":
        led_on(pin)
        _set_state(pin, "ON")
        return "LED ON | Pin {}".format(pin)

    elif action == "led_off":
        led_off(pin)
        _set_state(pin, "OFF")
        return "LED OFF | Pin {}".format(pin)

    elif action == "blink":
        times = cmd.get("times", 3)
        led_blink(pin, times)
        _set_state(pin, "OFF")
        return "Blink x{} | Pin {}".format(times, pin)

    elif action == "gpio_high":
        gpio_high(pin)
        _set_state(pin, "HIGH")
        return "GPIO HIGH | Pin {}".format(pin)

    elif action == "gpio_low":
        gpio_low(pin)
        _set_state(pin, "LOW")
        return "GPIO LOW | Pin {}".format(pin)

    elif action == "unknown":
        return "Unknown: " + cmd.get("message", "Try again")

    return "Unknown action"