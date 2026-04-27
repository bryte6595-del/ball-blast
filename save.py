"""
save.py - Persistent storage for high score and ball count.
"""

import json, os
from config import SAVE_FILE


def _load() -> dict:
    if not os.path.exists(SAVE_FILE):
        return {"high_score": 0, "ball_count": 1}
    try:
        with open(SAVE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"high_score": 0, "ball_count": 1}


def _save(data: dict):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_high_score() -> int:
    return _load().get("high_score", 0)


def load_ball_count() -> int:
    return _load().get("ball_count", 1)


def save_high_score(score: int):
    d = _load()
    if score > d.get("high_score", 0):
        d["high_score"] = score
        _save(d)


def save_ball_count(count: int):
    d = _load()
    d["ball_count"] = max(1, count)
    _save(d)


def reset_all():
    _save({"high_score": 0, "ball_count": 1})
