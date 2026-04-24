# Submission Note — Kaushik Karmakar

## Assumptions

- The CSV uses a **long/tall format**: one row per `(student, quiz, score)` triple, as seen in `quiz_scores.csv`.
- `student_id` is the primary key; `name` is used for the display label. Both are combined as `"Name (ID)"` in the report.
- A score of `0` is **valid** and counted — it is legitimate data, not a missing value.
- Multiple entries for the same student + quiz are **averaged together** (e.g. Aisha has two Q2 rows → averaged to 83.00).
- File encoding is assumed to be UTF-8 (with optional BOM, handled via `utf-8-sig`).
- Column names are detected automatically using keyword matching (case-insensitive, whitespace-tolerant), so minor variations like `"Score"` vs `"score"` are handled.

---

## Edge Cases Handled

| Case | How It's Handled |
|---|---|
| Blank score (e.g. Arjun Q1) | Silently skipped; quiz label omitted from that student's report |
| Non-numeric score value | `safe_float()` returns `None` — ignored without crashing |
| Student with zero valid scores | Overall Average displays `N/A` |
| Extra whitespace in headers or values | Stripped on load for all rows |
| Missing input file | Exits with a clear error message |
| Empty CSV file | Exits with a clear error message |
| No detectable score column | Exits and lists the headers it found |
| Score of `0` | Counted as a valid score (0.00 is displayed correctly) |
| Duplicate student + quiz rows | All valid scores are collected and averaged |

---

## Improvements With More Time

- **Output to file**: Add an `--output report.txt` flag to save the report alongside printing it.
- **Wide-format CSV support**: Auto-detect and handle layouts like `student, Q1, Q2, Q3` (one column per quiz).
- **Unit tests**: `pytest` suite covering missing file, blank scores, all-invalid rows, and zero scores.
- **Sorting options**: `--sort name|average` CLI flag for different report orderings.
- **Configurable column mapping**: Let users specify column roles via CLI flags for non-standard CSV schemas.
- **Richer output formats**: Optional JSON or Markdown output for downstream tooling.
