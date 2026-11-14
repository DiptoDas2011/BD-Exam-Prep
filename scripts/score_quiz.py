#!/usr/bin/env python3
"""Score a student's answers against a quiz JSON and list weak topics.

Usage:
  python3 scripts/score_quiz.py quiz.json answers.json [--out report.md] [--weak-json weak.json]

answers.json format (CQ marks are self-marked or marked by Claude):
{
  "mcq": {"m1": "খ", "m2": "b", "m3": "3"},
  "cq":  {"c1": {"ক": 1, "খ": 1, "গ": 3, "ঘ": 2}}
}
MCQ choices may be ক/খ/গ/ঘ, a/b/c/d, or 1-4. Unanswered items count as wrong.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CQ_LEVELS, LABELS, choice_index, load_json, write_text  # noqa: E402

WEAK_BELOW = 0.60
STRONG_ABOVE = 0.80
EARLY_SIGNAL_MAX_MARKS = 2  # topics with <= this many marks possible are only an early signal


def status(ratio):
    if ratio < WEAK_BELOW:
        return "দুর্বল"
    if ratio <= STRONG_ABOVE:
        return "মোটামুটি"
    return "ভালো"


def pct(a, b):
    return f"{round(100 * a / b)}%" if b else "-"


def score(quiz, answers):
    topics = defaultdict(lambda: [0, 0])      # topic -> [got, possible]
    levels = defaultdict(lambda: [0, 0])      # level -> [got, possible]
    wrong_mcq, cq_rows = [], []
    mcq_got = mcq_total = cq_got = cq_total = 0

    for m in quiz.get("mcq", []):
        topic = m.get("topic") or "অন্যান্য"
        given = answers.get("mcq", {}).get(m["id"])
        correct_idx = choice_index(m.get("answer"))
        ok = given is not None and choice_index(given) == correct_idx
        mcq_total += 1
        topics[topic][1] += 1
        if m.get("level"):
            levels[m["level"]][1] += 1
        if ok:
            mcq_got += 1
            topics[topic][0] += 1
            if m.get("level"):
                levels[m["level"]][0] += 1
        else:
            wrong_mcq.append((m, given))

    for c in quiz.get("cq", []):
        topic = c.get("topic") or "অন্যান্য"
        given = answers.get("cq", {}).get(c["id"], {})
        row = {"id": c["id"], "topic": topic, "parts": []}
        for p in c.get("parts", []):
            got = given.get(p["label"], 0) or 0
            try:
                got = float(got)
            except (TypeError, ValueError):
                got = 0.0
            got = max(0.0, min(got, float(p["marks"])))
            cq_total += p["marks"]
            cq_got += got
            topics[topic][0] += got
            topics[topic][1] += p["marks"]
            lvl = p.get("level")
            if lvl:
                levels[lvl][0] += got
                levels[lvl][1] += p["marks"]
            row["parts"].append((p["label"], got, p["marks"], lvl))
        cq_rows.append(row)

    return {
        "topics": dict(topics), "levels": dict(levels), "wrong_mcq": wrong_mcq, "cq_rows": cq_rows,
        "mcq": (mcq_got, mcq_total), "cq": (cq_got, cq_total),
    }


def fmt(x):
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}"


def render(quiz, r):
    mcq_got, mcq_total = r["mcq"]
    cq_got, cq_total = r["cq"]
    got, total = mcq_got + cq_got, mcq_total + cq_total
    lines = ["# ফলাফল", ""]
    parts = []
    if mcq_total:
        parts.append(f"MCQ {fmt(mcq_got)}/{mcq_total}")
    if cq_total:
        parts.append(f"CQ {fmt(cq_got)}/{cq_total}")
    lines.append(" | ".join(parts) + f" | মোট {fmt(got)}/{total} ({pct(got, total)})")
    lines.append("")

    lines += ["## টপিক অনুযায়ী", "", "| টপিক | নম্বর | শতাংশ | অবস্থা |", "|---|---|---|---|"]
    ranked = sorted(r["topics"].items(), key=lambda kv: (kv[1][0] / kv[1][1]) if kv[1][1] else 1)
    for t, (g, p) in ranked:
        st = status(g / p) if p else "-"
        if p <= EARLY_SIGNAL_MAX_MARKS:
            st += " (প্রাথমিক ইঙ্গিত)"
        lines.append(f"| {t} | {fmt(g)}/{fmt(p)} | {pct(g, p)} | {st} |")
    lines.append("")

    weak = [t for t, (g, p) in ranked if p and g / p < WEAK_BELOW][:3]
    if weak:
        lines += ["## সবচেয়ে দুর্বল টপিক", ""] + [f"{i}. {t}" for i, t in enumerate(weak, 1)] + [""]

    if r["levels"]:
        lines += ["## দক্ষতার স্তর অনুযায়ী", "", "| স্তর | নম্বর | শতাংশ |", "|---|---|---|"]
        for lvl in CQ_LEVELS:
            if lvl in r["levels"]:
                g, p = r["levels"][lvl]
                lines.append(f"| {lvl} | {fmt(g)}/{fmt(p)} | {pct(g, p)} |")
        lines.append("")

    if r["cq_rows"]:
        lines += ["## CQ অংশভিত্তিক", ""]
        for row in r["cq_rows"]:
            cells = ", ".join(f"{lab} {fmt(g)}/{m}" for lab, g, m, _ in row["parts"])
            lines.append(f"- {row['id']} ({row['topic']}): {cells}")
        lines.append("")

    if r["wrong_mcq"]:
        lines += ["## যে MCQ ভুল হয়েছে", ""]
        for m, given in r["wrong_mcq"]:
            correct = LABELS[choice_index(m["answer"])]
            you = "উত্তর দাওনি" if given is None else str(given)
            lines.append(f"- **{m['id']}** ({m.get('topic', 'অন্যান্য')}): তোমার উত্তর {you}, সঠিক {correct}। {m.get('explanation', '')}")
        lines.append("")

    lines.append("পরের রাউন্ড: দুর্বল টপিক থেকে নতুন প্রশ্ন (৬০% দুর্বল, ২৫% মোটামুটি, ১৫% ভালো)।")
    return "\n".join(lines) + "\n", weak


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("quiz")
    ap.add_argument("answers")
    ap.add_argument("--out", help="write the Markdown report to this file")
    ap.add_argument("--weak-json", help="write weak topics (JSON) to this file")
    args = ap.parse_args()

    quiz = load_json(args.quiz)
    answers = load_json(args.answers)
    r = score(quiz, answers)
    report, weak = render(quiz, r)
    print(report)
    if args.out:
        write_text(args.out, report)
    if args.weak_json:
        data = {
            "weak": weak,
            "topics": {t: {"got": g, "possible": p} for t, (g, p) in r["topics"].items()},
        }
        write_text(args.weak_json, json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
