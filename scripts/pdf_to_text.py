#!/usr/bin/env python3
"""Extract text from a Bangla/English textbook PDF, page by page, falling back to OCR.

Many NCTB PDFs use legacy font encodings, so the embedded text layer comes out garbled.
This script tries the text layer first (pdftotext), checks whether it looks like real
Bangla, and OCRs the page (tesseract) when it does not.

Requires (system tools, not Python packages):
  poppler-utils   -> pdftotext, pdfinfo, pdftoppm
  tesseract-ocr + the Bengali data (tesseract-ocr-ben) for OCR

Usage:
  python3 scripts/pdf_to_text.py book.pdf build/book --lang ben+eng
  python3 scripts/pdf_to_text.py book.pdf build/book --mode ocr --first 10 --last 40

Output:
  <outdir>/pages/page-0001.txt ...   one file per page
  <outdir>/book.md                   all pages with <!-- page N (text|ocr) --> markers

ALWAYS proofread the output by hand. OCR of Bangla conjuncts, maths and formulas makes mistakes.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"Missing tool: {tool}. Install poppler-utils / tesseract-ocr (with the 'ben' language pack).")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def page_count(pdf):
    out = run(["pdfinfo", str(pdf)]).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    if not m:
        sys.exit("Could not read the page count (is this a valid PDF?)")
    return int(m.group(1))


def text_layer(pdf, page):
    return run(["pdftotext", "-f", str(page), "-l", str(page), "-enc", "UTF-8", str(pdf), "-"]).stdout


def bengali_ratio(text):
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if 0x0980 <= ord(c) <= 0x09FF) / len(letters)


def looks_bad(text, lang, min_bengali):
    """True when the text layer is empty or garbled and OCR should be used."""
    if len(text.strip()) < 40:
        return True
    junk = sum(1 for c in text if c == "�" or 0xE000 <= ord(c) <= 0xF8FF)
    if junk > 0.02 * len(text):
        return True
    if "ben" in lang and bengali_ratio(text) < min_bengali:
        return True
    return False


def ocr_page(pdf, page, lang, dpi):
    with tempfile.TemporaryDirectory() as tmp:
        prefix = str(Path(tmp) / "p")
        r = run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), "-png", str(pdf), prefix])
        if r.returncode != 0:
            return ""
        images = sorted(Path(tmp).glob("p*.png"))
        if not images:
            return ""
        t = run(["tesseract", str(images[0]), "stdout", "-l", lang, "--psm", "3"])
        return t.stdout


def check_ocr_lang(lang):
    have = set(run(["tesseract", "--list-langs"]).stdout.split()[1:])
    missing = [l for l in lang.split("+") if l not in have]
    if missing:
        sys.exit(f"Tesseract language data missing: {', '.join(missing)}. "
                 f"Install it (for Bengali: the 'ben' traineddata, e.g. package tesseract-ocr-ben).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--lang", default="ben+eng", help="tesseract languages, e.g. ben, eng, ben+eng (default ben+eng)")
    ap.add_argument("--mode", choices=["auto", "text", "ocr"], default="auto",
                    help="auto = text layer, OCR when it looks garbled; text = never OCR; ocr = always OCR")
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--last", type=int, default=0, help="0 = last page")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--min-bengali", type=float, default=None,
                    help="min share of Bengali letters for a page to count as good text "
                         "(default 0.30 for 'ben', 0.10 for 'ben+eng')")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.is_file():
        sys.exit(f"PDF not found: {pdf}")
    for tool in ("pdfinfo", "pdftotext"):
        need(tool)
    if args.mode != "text":
        need("pdftoppm")
        need("tesseract")
        check_ocr_lang(args.lang)

    min_bn = args.min_bengali
    if min_bn is None:
        min_bn = 0.30 if args.lang == "ben" else 0.10

    total = page_count(pdf)
    last = args.last or total
    first = max(1, args.first)
    last = min(last, total)

    out = Path(args.outdir)
    (out / "pages").mkdir(parents=True, exist_ok=True)

    chunks, n_text, n_ocr = [], 0, 0
    for p in range(first, last + 1):
        method, text = "text", ""
        if args.mode != "ocr":
            text = text_layer(pdf, p)
        if args.mode == "ocr" or (args.mode == "auto" and looks_bad(text, args.lang, min_bn)):
            text, method = ocr_page(pdf, p, args.lang, args.dpi), "ocr"
        n_ocr += method == "ocr"
        n_text += method == "text"
        (out / "pages" / f"page-{p:04d}.txt").write_text(text, encoding="utf-8")
        chunks.append(f"<!-- page {p} ({method}) -->\n{text.strip()}\n")
        print(f"page {p}/{last} [{method}]", file=sys.stderr)

    book = out / "book.md"
    book.write_text("\n".join(chunks), encoding="utf-8")
    print(f"\nDone: {last - first + 1} pages ({n_text} text layer, {n_ocr} OCR) -> {book}")
    print("Next: proofread by hand, then run scripts/split_chapters.py")


if __name__ == "__main__":
    main()
