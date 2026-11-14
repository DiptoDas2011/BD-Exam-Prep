#!/usr/bin/env python3
"""Turn a quiz JSON into a printable HTML page (questions first, answer key on a separate page).

Usage:
  python3 scripts/make_quiz_html.py quiz.json -o quiz.html [--no-answers]

Open the HTML in a browser and use Print → Save as PDF. No extra libraries needed.
"""
import argparse
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import LABELS, choice_index, load_json, write_text  # noqa: E402

CSS = """
@page { size: A4; margin: 16mm; }
body { font-family: "Noto Sans Bengali", "Kalpurush", "SolaimanLipi", "Nirmala UI", "Vrinda", sans-serif;
       font-size: 13pt; line-height: 1.6; color: #111; max-width: 800px; margin: 0 auto; padding: 16px; }
h1 { font-size: 20pt; margin: 0 0 4px; }
h2 { font-size: 15pt; border-bottom: 2px solid #333; padding-bottom: 2px; margin-top: 26px; }
.meta { color: #444; font-size: 11pt; margin-bottom: 10px; }
.sheet-head { display: flex; gap: 24px; font-size: 11pt; margin: 8px 0 14px; }
.sheet-head span { flex: 1; border-bottom: 1px solid #333; padding-bottom: 14px; }
.q { margin: 12px 0; page-break-inside: avoid; }
.opts { margin: 4px 0 0 18px; }
.opts div { margin: 2px 0; }
.stim { background: #f3f3f3; border-left: 4px solid #555; padding: 8px 12px; margin: 6px 0; }
.part { margin: 6px 0 6px 12px; }
.marks { float: right; color: #444; }
.ans { color: #064; }
.key { page-break-before: always; }
.small { font-size: 10.5pt; color: #444; }
pre { white-space: pre-wrap; font: inherit; margin: 0; }
"""


def esc(text):
    return escape(str(text)).replace("\n", "<br>")


def build(quiz, with_answers):
    meta = quiz.get("meta", {})
    out = ["<!doctype html><html lang='bn'><head><meta charset='utf-8'>",
           f"<title>{esc(meta.get('title', 'কুইজ'))}</title><style>{CSS}</style></head><body>"]
    out.append(f"<h1>{esc(meta.get('title', 'কুইজ'))}</h1>")
    bits = [meta.get("class") and f"শ্রেণি: {meta['class']}", meta.get("subject") and f"বিষয়: {meta['subject']}",
            meta.get("time_minutes") and f"সময়: {meta['time_minutes']} মিনিট"]
    out.append(f"<div class='meta'>{esc(' | '.join(b for b in bits if b))}</div>")
    if meta.get("source") == "original-board-style":
        out.append("<div class='small'>মৌলিক, বোর্ড-স্টাইল প্রশ্ন (কোনো বোর্ড বা সালের প্রশ্ন নয়)</div>")
    out.append("<div class='sheet-head'><span>নাম:</span><span>রোল:</span><span>তারিখ:</span></div>")

    mcqs, cqs = quiz.get("mcq", []), quiz.get("cq", [])
    n = 0
    if mcqs:
        out.append(f"<h2>বহুনির্বাচনি প্রশ্ন ({len(mcqs)}টি, প্রতিটি ১ নম্বর)</h2>")
        for m in mcqs:
            n += 1
            opts = "".join(f"<div>{LABELS[i]}. {esc(o)}</div>" for i, o in enumerate(m["options"]))
            out.append(f"<div class='q'><div>{n}. {esc(m['q'])}</div><div class='opts'>{opts}</div></div>")
    if cqs:
        out.append("<h2>সৃজনশীল প্রশ্ন</h2>")
        for k, c in enumerate(cqs, 1):
            total = sum(p["marks"] for p in c["parts"])
            out.append(f"<div class='q'><b>প্রশ্ন {k}</b> <span class='marks'>[{total}]</span>"
                       f"<div class='stim'>{esc(c['stimulus'])}</div>")
            for p in c["parts"]:
                out.append(f"<div class='part'>{p['label']}. {esc(p['q'])} <span class='marks'>({p['marks']})</span></div>")
            out.append("</div>")

    if with_answers:
        out.append("<div class='key'><h1>উত্তরমালা</h1>")
        if mcqs:
            out.append("<h2>MCQ</h2>")
            for i, m in enumerate(mcqs, 1):
                lab = LABELS[choice_index(m["answer"])]
                out.append(f"<div class='q'>{i}. <b class='ans'>{lab}</b> &nbsp; {esc(m.get('explanation', ''))}</div>")
        if cqs:
            out.append("<h2>সৃজনশীল প্রশ্ন</h2>")
            for k, c in enumerate(cqs, 1):
                out.append(f"<div class='q'><b>উত্তর {k}</b>")
                for p in c["parts"]:
                    out.append(f"<div class='part'><b>{p['label']}.</b> {esc(p['model_answer'])}"
                               f"<div class='small'>নম্বর বণ্টন: {esc(p.get('rubric', ''))}</div></div>")
                out.append("</div>")
        out.append("</div>")
    out.append("</body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("quiz")
    ap.add_argument("-o", "--out", default="quiz.html")
    ap.add_argument("--no-answers", action="store_true", help="leave out the answer key page")
    args = ap.parse_args()
    quiz = load_json(args.quiz)
    write_text(args.out, build(quiz, not args.no_answers))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
