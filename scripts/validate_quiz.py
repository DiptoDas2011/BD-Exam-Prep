#!/usr/bin/env python3
"""Validate a quiz JSON file before using or printing it.

Usage: python3 scripts/validate_quiz.py quiz.json

Exit code 0 = no errors (warnings are allowed), 1 = errors found.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CQ_LEVELS, LABELS, choice_index, load_json  # noqa: E402

ALLOWED_SOURCES = {"original-board-style", "verified-past-paper"}
PROVENANCE_FIELDS = ["exam", "board", "year", "verified_by", "verified_on", "permission"]
EXPECTED_CQ_MARKS = [1, 2, 3, 4]


def validate(quiz):
    errors, warnings = [], []
    meta = quiz.get("meta", {})

    # --- provenance ---
    source = meta.get("source")
    if source not in ALLOWED_SOURCES:
        errors.append(f"meta.source must be one of {sorted(ALLOWED_SOURCES)} (got {source!r})")
    if source == "verified-past-paper":
        prov = meta.get("provenance", {})
        missing = [k for k in PROVENANCE_FIELDS if not prov.get(k)]
        if missing:
            errors.append(f"verified-past-paper needs meta.provenance fields: {', '.join(missing)}")
    if source == "original-board-style" and "provenance" in meta:
        errors.append("original-board-style quizzes must not carry board/year provenance")
    for field in ("title", "subject"):
        if not meta.get(field):
            warnings.append(f"meta.{field} is empty")

    mcqs = quiz.get("mcq", [])
    cqs = quiz.get("cq", [])
    if not mcqs and not cqs:
        errors.append("quiz has no mcq and no cq items")

    seen = set()

    # --- MCQ ---
    for i, m in enumerate(mcqs, 1):
        mid = m.get("id") or f"mcq#{i}"
        if mid in seen:
            errors.append(f"{mid}: duplicate id")
        seen.add(mid)
        if not m.get("q", "").strip():
            errors.append(f"{mid}: empty question")
        opts = m.get("options", [])
        if len(opts) != 4:
            errors.append(f"{mid}: needs exactly 4 options (has {len(opts)})")
        elif len({str(o).strip() for o in opts}) != 4:
            errors.append(f"{mid}: options are not all different")
        idx = choice_index(m.get("answer"))
        if idx is None:
            errors.append(f"{mid}: answer must be ক/খ/গ/ঘ (got {m.get('answer')!r})")
        if not m.get("explanation", "").strip():
            errors.append(f"{mid}: missing explanation")
        if not m.get("topic"):
            warnings.append(f"{mid}: no topic (weak-topic report will group it as 'অন্যান্য')")
        if m.get("level") and m["level"] not in CQ_LEVELS:
            warnings.append(f"{mid}: unknown level {m['level']!r}")

    if len(mcqs) >= 8:
        answers = [choice_index(m.get("answer")) for m in mcqs]
        counts = [answers.count(k) for k in range(4)]
        if max(counts) > 0.5 * len(mcqs):
            warnings.append(f"correct answers are lopsided across ক/খ/গ/ঘ: {counts}")

    # --- CQ ---
    for i, c in enumerate(cqs, 1):
        cid = c.get("id") or f"cq#{i}"
        if cid in seen:
            errors.append(f"{cid}: duplicate id")
        seen.add(cid)
        if not c.get("stimulus", "").strip():
            errors.append(f"{cid}: missing stimulus (উদ্দীপক)")
        parts = c.get("parts", [])
        labels = [p.get("label") for p in parts]
        if labels != LABELS:
            errors.append(f"{cid}: parts must be ক, খ, গ, ঘ in order (got {labels})")
        marks = [p.get("marks") for p in parts]
        if marks != EXPECTED_CQ_MARKS:
            errors.append(f"{cid}: part marks must be 1,2,3,4 (got {marks})")
        for p in parts:
            tag = f"{cid}.{p.get('label')}"
            if not p.get("q", "").strip():
                errors.append(f"{tag}: empty question")
            if not p.get("model_answer", "").strip():
                errors.append(f"{tag}: missing model_answer")
            if not p.get("rubric", "").strip():
                warnings.append(f"{tag}: missing rubric (marking note)")
            if p.get("level") and p["level"] not in CQ_LEVELS:
                warnings.append(f"{tag}: unknown level {p['level']!r}")
        if not c.get("topic"):
            warnings.append(f"{cid}: no topic")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    quiz = load_json(sys.argv[1])
    errors, warnings = validate(quiz)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    n_mcq, n_cq = len(quiz.get("mcq", [])), len(quiz.get("cq", []))
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s) in {n_mcq} MCQ / {n_cq} CQ")
        sys.exit(1)
    print(f"OK: {n_mcq} MCQ / {n_cq} CQ, {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
