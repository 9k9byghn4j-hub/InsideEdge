import json
import os

_PATH = os.path.join(os.path.dirname(__file__), ".watchlist.json")


def load_pins():
    """Returns {fixtureId (str): {"match": ..., "start": ...}}."""
    try:
        with open(_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save(pins):
    with open(_PATH, "w") as f:
        json.dump(pins, f)


def pin(fixture_id, meta):
    pins = load_pins()
    pins[str(fixture_id)] = meta
    _save(pins)


def unpin(fixture_id):
    pins = load_pins()
    pins.pop(str(fixture_id), None)
    _save(pins)


def is_pinned(fixture_id):
    return str(fixture_id) in load_pins()
