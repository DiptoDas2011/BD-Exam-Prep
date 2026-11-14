"""Shared helpers for bd-exam-prep scripts (standard library only)."""
import json
import sys
from pathlib import Path

LABELS = ["ক", "খ", "গ", "ঘ"]
BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

# Accepted spellings for an MCQ choice -> 0-based option index
_CHOICE_MAP = {
    "ক": 0, "খ": 1, "গ": 2, "ঘ": 3,
    "a": 0, "b": 1, "c": 2, "d": 3,
    "1": 0, "2": 1, "3": 2, "4": 3,
}

CQ_LEVELS = ["জ্ঞান", "অনুধাবন", "প্রয়োগ", "উচ্চতর দক্ষতা"]


def choice_index(value):
    """Turn 'খ', 'b', 'B', 2 or '২' into an option index (0-3). Returns None if invalid."""
    if value is None:
        return None
    key = str(value).strip().translate(BN_DIGITS).lower()
    return _CHOICE_MAP.get(key)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"File not found: {path}")
    except json.JSONDecodeError as e:
        sys.exit(f"Invalid JSON in {path}: {e}")


def write_text(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
