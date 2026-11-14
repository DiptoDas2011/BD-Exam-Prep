# Chapter files

Each chapter gets its own short file so Claude loads only what it needs.

## Naming

```
class<NN>-<subject>-ch<NN>-<slug>.md
class10-physics-ch03-force-and-motion.md
```

## What goes inside

Write **your own** summary, not a copy of the book. Aim for 1-3 pages. Use `_TEMPLATE.md`.

Good content:
- Key definitions in the textbook's wording of the terms (short)
- Formulas with units
- Diagrams described in words
- Common student mistakes
- 5 to 10 possible CQ angles (scenarios that can carry a stimulus)

Avoid:
- Long passages pasted from NCTB books or guidebooks (copyright)
- Questions labelled as from a particular board or year (see the provenance rule in `SKILL.md`)

## Building from a PDF

```bash
python3 scripts/pdf_to_text.py nctb-book.pdf build/book --lang ben+eng
python3 scripts/split_chapters.py build/book/book.md build/chapters --prefix class10-physics
```

Then read each generated file, **fix OCR mistakes by hand**, and write a summary into `references/chapters/`. The raw text stays in `build/`, which is not committed.
