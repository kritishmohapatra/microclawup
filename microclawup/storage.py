# microclawup/storage.py
import ujson

FILE = "microclawup_data.json"

def _read_file():
    try:
        with open(FILE, "r") as f:
            return ujson.load(f)
    except (OSError, ValueError):
        return {}

def _write_file(data):
    try:
        with open(FILE, "w") as f:
            ujson.dump(data, f)
    except OSError as e:
        print("Storage write error:", e)

def save_data(key, value):
    data = _read_file()
    data[key] = value
    _write_file(data)
    return True

def load_data(key):
    data = _read_file()
    return data.get(key, None)

def delete_data(key):
    data = _read_file()
    if key in data:
        del data[key]
        _write_file(data)
        return True
    return False