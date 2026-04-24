# Student Quiz Score Summary

A Python script that reads a CSV file of student quiz scores and prints a clean,
readable summary report — built as a recruiting assignment for **Udhyam Learning Foundation**.

---

## Files

| File | Description |
|---|---|
| `solution_KaushikKarmakar.py` | Main Python script |
| `quiz_scores.csv` | Sample input data |
| `SUBMISSION_NOTE.md` | Assumptions, edge cases, and improvement notes |

---

## Requirements

- Python 3.7+
- Standard library only (`csv`, `argparse`, `statistics`, `collections`, `os`, `sys`)

---

## Usage

```bash
# Default: reads quiz_scores.csv from the same directory
python solution_KaushikKarmakar.py

# Or pass an explicit file path
python solution_KaushikKarmakar.py path/to/your/file.csv
```

---

## Sample Output

```
Student Quiz Score Summary
==========================

Student: Aisha (S001)
  Q1 Average: 82.00
  Q2 Average: 83.00
  Overall Average: 82.67

Student: Arjun (S006)
  Q2 Average: 49.00
  Q3 Average: 73.00
  Overall Average: 61.00
```

> Arjun's Q1 score was blank in the CSV — it is silently skipped and omitted from the report.

---

## CSV Format Expected

The script expects a **long/tall format** CSV with columns:

```
student_id, name, quiz, score
```

Multiple rows per student × quiz are averaged together.
Column names are detected automatically (case-insensitive, whitespace-tolerant).

---

## Author

**Kaushik Karmakar**
