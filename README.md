# bd-exam-prep · শেষ রাতের পরীক্ষা প্রস্তুতি

A [Claude skill](https://docs.claude.com) that helps Bangladeshi students (Class 9 to SSC, plus Primary and Junior scholarship) practise on the last night before an exam.

It asks a few quick questions (class, subject, syllabus, hours left, weak topics), then builds board-style **CQ (সৃজনশীল)** and **MCQ** practice in Bangla, scores the answers, finds weak topics, and runs a focused second round.

> এটি একটি অনুশীলনের সহায়ক। পাঠ্যবই ও শিক্ষকের নির্দেশনাই চূড়ান্ত। এই প্রকল্প NCTB বা কোনো শিক্ষা বোর্ডের সঙ্গে যুক্ত নয়।

## What it does

- Intake: class, subject, exam, school syllabus (text or photo), time left, weak topics
- Generates new CQs (উদ্দীপক + ক/খ/গ/ঘ = 1+2+3+4 marks) and MCQs (simple, multi-statement, shared-stimulus)
- Last-night plans for 3 hours, 1-3 hours, or under 1 hour
- Scores answers, shows weak topics and skill levels (জ্ঞান, অনুধাবন, প্রয়োগ, উচ্চতর দক্ষতা)
- Round 2 from the weak topics
- Printable quiz with an answer key page (HTML → Print → PDF)
- **Never invents** a board or year for a question: only items in a verified dataset may be attributed, everything else is labelled "মৌলিক, বোর্ড-স্টাইল"

## Install

**Claude (web/app):** zip the `bd-exam-prep` folder and upload it in Claude's skill settings. Skill upload may not be available on every plan; check the current Claude documentation.

**Claude Code:**

```bash
git clone https://github.com/<your-username>/BD-Exam-Prep ~/.claude/skills/BD-Exam-Prep
```

## Try it

```
আমি ক্লাস ১০-এর ছাত্র। কাল পদার্থবিজ্ঞান পরীক্ষা। আমার সিলেবাস: বল ও গতি, কাজ ক্ষমতা ও শক্তি। হাতে ৩ ঘণ্টা আছে।
```

```
SSC গণিতের জন্য ২০টি MCQ আর ২টি সৃজনশীল দাও। ত্রিকোণমিতি আমার দুর্বল।
```

```
এই সিলেবাসের ছবিটা দিলাম। এর ভিত্তিতে মডেল টেস্ট বানাও।
```

## Repo layout

```
bd-exam-prep/
├── SKILL.md                    workflow and rules (what Claude reads first)
├── references/
│   ├── question-patterns.md    CQ / MCQ formats, marks, writing rules
│   ├── last-night-mode.md      time-based study plans
│   ├── feedback-loop.md        scoring, weak topics, round 2
│   ├── sources.md              official links and past-paper policy
│   ├── syllabus/               one file per class + subject + year
│   └── chapters/               your own chapter summaries (Bangla)
├── scripts/
│   ├── validate_quiz.py        schema and mark checks
│   ├── score_quiz.py           scoring and weak-topic report
│   ├── make_quiz_html.py       printable quiz + answer key
│   ├── pdf_to_text.py          textbook PDF → text (OCR fallback)
│   └── split_chapters.py       book text → one file per chapter
├── data/
│   ├── sample_quiz.json        quiz format example
│   ├── topic_frequency.template.csv
│   └── past_questions/         optional, verified items only
└── examples/sample-session.md
```

## Building the content library (maintainers)

The skill works out of the box using the student's own syllabus and Claude's knowledge, but it gets better and more accurate with chapter files.

1. Download the NCTB textbook PDF for one subject from the official site (see `references/sources.md`).
2. Extract text. Needs `poppler-utils` and `tesseract-ocr` with Bengali data:
   ```bash
   python3 scripts/pdf_to_text.py book.pdf build/book --lang ben+eng
   python3 scripts/split_chapters.py build/book/book.md build/chapters --prefix class10-physics
   ```
3. **Proofread by hand.** Bangla OCR makes mistakes with conjuncts, numbers and formulas.
4. Write your own short summary for each chapter in `references/chapters/` using `_TEMPLATE.md`.
5. Add the syllabus in `references/syllabus/` and confirm the mark distribution in `references/question-patterns.md`.
6. Write 20 hand-checked sample questions and test the skill with real students.

**Start with one subject** (for example SSC Physics or General Math), get it right, then expand.

## Content and copyright

- Keep raw book text in `build/` (git-ignored). Commit only your own summaries.
- Don't commit past papers unless you have permission. Link to them in `references/sources.md`, or store only your own statistics.
- Code is MIT licensed. Content you add is your own responsibility; see `LICENSE`.

## Test the scripts

```bash
python3 scripts/validate_quiz.py data/sample_quiz.json
python3 scripts/make_quiz_html.py data/sample_quiz.json -o /tmp/quiz.html
python3 scripts/score_quiz.py data/sample_quiz.json examples/sample-answers.json
```

## Contributing

See `CONTRIBUTING.md`. Teachers and students are very welcome to help verify content.
