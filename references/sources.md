# Sources and links

This file lists where to find official material. **Do not copy books or past papers into this repo unless you have permission.** Link to them, or store only your own notes, summaries and statistics.

## Official sites (verify links before publishing; sites move)

| What | Where |
|---|---|
| NCTB textbooks (পাঠ্যপুস্তক), all classes | NCTB official website: https://nctb.gov.bd (look for the textbooks / e-book section) |
| Primary education, scholarship notices | Directorate of Primary Education: https://dpe.gov.bd |
| Dhaka Education Board | https://dhakaeducationboard.gov.bd |
| Other education boards | Each board has its own site; see the Bangladesh education board list on the government portal |
| Education statistics and policy | BANBEIS: https://banbeis.gov.bd |

## Past papers (প্রশ্নব্যাংক)

Past papers are usually compiled by third parties and may be copyrighted. Use this table to record **where a student can find them**, not the papers themselves.

| Exam | Years | Link | Permission to copy? | Verified by | Date |
|---|---|---|---|---|---|
| (example) SSC Dhaka Board Physics | 2019-2024 | (add link) | No, link only | (name) | (date) |

## Rules for adding a source

1. Add the link and who verified it.
2. Write whether copying is allowed. If unknown, treat as **not allowed**.
3. If you add questions from a past paper to `data/past_questions/`, you must have permission, and every item needs `board`, `year`, `exam` and `verified_by`.
4. Keep your own statistics (for example topic frequency) in `data/topic_frequency.csv`. Statistics about papers are your own work and are safer to share than the papers themselves.

## Textbook usage

- Students should treat the printed NCTB book as the final authority.
- When you convert a book to text (`scripts/pdf_to_text.py`), keep the output in a private `build/` folder (it is in `.gitignore`). Commit only your own chapter summaries under `references/chapters/`.
