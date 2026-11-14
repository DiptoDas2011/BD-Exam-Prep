# Verified past questions (optional)

Leave this folder empty unless you have **permission** to store the questions.

If you add questions, use the same JSON schema as `data/sample_quiz.json`, but set:

```json
"meta": {
  "source": "verified-past-paper",
  "provenance": {
    "exam": "SSC",
    "board": "Dhaka",
    "year": 2023,
    "subject": "...",
    "verified_by": "your-name",
    "verified_on": "2026-11-14",
    "permission": "describe how you have the right to store this"
  }
}
```

`scripts/validate_quiz.py` rejects a `verified-past-paper` quiz that is missing any of these fields. The skill may only say a question came from a particular board and year when it is in a file like this.

Safer alternative: keep the papers elsewhere, and store only your own statistics in `data/topic_frequency.csv`.
