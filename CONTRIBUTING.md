# Contributing

Thank you for helping students. A few rules keep the skill trustworthy.

## Content rules

1. **Accuracy beats volume.** One verified chapter is worth more than ten unchecked ones. Have a teacher review science and maths content.
2. **Your own words.** Summaries and questions must be your own work. Don't paste textbook passages or guidebook questions.
3. **Provenance.** A question may be attributed to a board and year only if it is stored under `data/past_questions/` with full provenance and permission. Otherwise it is "মৌলিক, বোর্ড-স্টাইল".
4. **Dated syllabi.** Put the year in every syllabus filename and cite the source.
5. **Verify marks.** When you confirm a mark distribution or exam format, update `references/question-patterns.md` and its "Last verified" line.

## Pull requests

- One subject or one feature per PR.
- Run before opening a PR:
  ```bash
  python3 scripts/validate_quiz.py data/sample_quiz.json
  ```
  and validate any quiz JSON you add.
- Keep `SKILL.md` short. Put detail in `references/`.
- Scripts must stay standard-library only so students and teachers can run them easily.

## Reporting a wrong answer

Open an issue with: class, subject, chapter, the question, what is wrong, and the correct answer with a textbook page reference if possible.
