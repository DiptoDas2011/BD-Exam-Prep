#!/usr/bin/env python3
"""Split a whole-book text/Markdown file into one file per chapter.

Usage:
  python3 scripts/split_chapters.py build/book/book.md build/chapters --prefix class10-physics
  python3 scripts/split_chapters.py book.md out --pattern '^\\s*Unit\\s+(\\d+)'

The default pattern finds headings such as "প্রথম অধ্যায়", "অধ্যায় ৩", "অধ্যায়-৩" and "Chapter 3".
Table-of-contents lines match too, so sections shorter than --min-chars are dropped.
Check the result by hand: chapter detection depends on how the OCR text looks.

Output: <outdir>/<prefix>-chNN.md (with front matter) and <outdir>/index.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ORDINALS = ("প্রথম|দ্বিতীয়|তৃতীয়|চতুর্থ|পঞ্চম|ষষ্ঠ|সপ্তম|অষ্টম|নবম|দশম|একাদশ|দ্বাদশ|ত্রয়োদশ|"
            "চতুর্দশ|পঞ্চদশ|ষোড়শ|সপ্তদশ|অষ্টাদশ|ঊনবিংশ|বিংশ")
DEFAULT_PATTERN = (rf"^\s*(?:#+\s*)?(?:(?:{ORDINALS})\s*অধ্যায়|অধ্যায়\s*[-:]?\s*[0-9০-৯]+|"
                   rf"(?:Chapter|CHAPTER)\s*[-:]?\s*[0-9]+)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("book", help="input text/Markdown file")
    ap.add_argument("outdir")
    ap.add_argument("--prefix", default="chapter", help="filename prefix, e.g. class10-physics")
    ap.add_argument("--pattern", default=DEFAULT_PATTERN, help="regex that matches a chapter heading line")
    ap.add_argument("--min-chars", type=int, default=800, help="drop sections shorter than this (table of contents)")
    args = ap.parse_args()

    src = Path(args.book)
    if not src.is_file():
        sys.exit(f"File not found: {src}")
    lines = src.read_text(encoding="utf-8").splitlines()
    rx = re.compile(args.pattern)

    starts = [i for i, ln in enumerate(lines) if rx.search(ln)]
    if not starts:
        sys.exit("No chapter headings found. Check the OCR text, or pass --pattern with your own regex.")

    sections = []
    for n, s in enumerate(starts):
        e = starts[n + 1] if n + 1 < len(starts) else len(lines)
        body = "\n".join(lines[s:e]).strip()
        if len(body) >= args.min_chars:
            sections.append((lines[s].strip().lstrip("#").strip(), body))

    if not sections:
        sys.exit(f"Headings were found but every section is under {args.min_chars} characters. Lower --min-chars.")

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for n, (title, body) in enumerate(sections, 1):
        name = f"{args.prefix}-ch{n:02d}.md"
        front = f"---\nchapter: {n}\nheading: {json.dumps(title, ensure_ascii=False)}\nstatus: raw, needs proofreading\n---\n\n"
        (out / name).write_text(front + body + "\n", encoding="utf-8")
        index.append({"chapter": n, "file": name, "heading": title, "chars": len(body)})
        print(f"{name}  {title}  ({len(body)} chars)")

    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(sections)} chapter file(s) written to {out}")


if __name__ == "__main__":
    main()
