"""
solution_KaushikKarmakar.py
Student Quiz Score Summary — Udhyam Learning Foundation recruiting assignment.

Usage:
    python solution_KaushikKarmakar.py               # reads quiz_scores.csv from same directory
    python solution_KaushikKarmakar.py path/to/file  # explicit file path
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from statistics import mean


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Print a quiz score summary report.")
    parser.add_argument(
        "filepath",
        nargs="?",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_scores.csv"),
        help="Path to the CSV file (default: quiz_scores.csv in the same directory as this script)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------

def load_csv(filepath):
    """Read the CSV and return (headers, list-of-dicts). Raises on file errors."""
    if not os.path.exists(filepath):
        sys.exit(f"Error: File not found — {filepath}")

    with open(filepath, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)

        if reader.fieldnames is None:
            sys.exit("Error: The CSV file is empty.")

        # Normalise headers: strip surrounding whitespace
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        rows = [
            {k.strip(): v.strip() for k, v in row.items() if k is not None}
            for row in reader
            if any(v and v.strip() for v in row.values())  # skip entirely blank rows
        ]

    if not rows:
        sys.exit("Error: The CSV file contains no data rows.")

    return reader.fieldnames, rows


# ---------------------------------------------------------------------------
# Column detection
# ---------------------------------------------------------------------------

def detect_columns(headers):
    """
    Detect which columns hold the student identifier, display name, quiz label,
    and numeric score in a long-format CSV (one score per row).

    Returns a dict with keys: id_col, name_col (optional), quiz_col, score_col.
    Exits with a helpful message if required columns cannot be found.
    """
    lower = {h: h.lower() for h in headers}

    def find(candidates):
        for h, hl in lower.items():
            for c in candidates:
                if c in hl:
                    return h
        return None

    id_col    = find(["student_id", "id", "student"])
    name_col  = find(["name"])
    quiz_col  = find(["quiz", "quiz_name", "quiz_label", "assessment"])
    score_col = find(["score", "mark", "grade", "result", "points"])

    # We need at least a student identifier and a score column.
    missing = []
    if id_col is None and name_col is None:
        missing.append("student identifier (e.g. 'student_id' or 'name')")
    if score_col is None:
        missing.append("score column (e.g. 'score' or 'marks')")

    if missing:
        sys.exit(
            "Error: Could not detect required columns.\n"
            "Missing: " + ", ".join(missing) + "\n"
            f"Found headers: {headers}"
        )

    return {
        "id_col":    id_col,
        "name_col":  name_col,
        "quiz_col":  quiz_col,
        "score_col": score_col,
    }


# ---------------------------------------------------------------------------
# Data aggregation
# ---------------------------------------------------------------------------

def safe_float(value):
    """Return float if value is a valid number, else None."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def aggregate(rows, cols):
    """
    Build an ordered dict keyed by student identifier.

    Each entry:
        {
            "name": str,
            "quiz_scores": defaultdict(list),   # quiz_label -> [valid floats]
        }

    Multiple rows for the same student+quiz are averaged together.
    """
    # Preserve insertion order (student order in the file)
    students = {}

    id_col    = cols["id_col"]
    name_col  = cols["name_col"]
    quiz_col  = cols["quiz_col"]
    score_col = cols["score_col"]

    for row in rows:
        # Determine the student key; fall back to name if no id column detected
        student_key = row.get(id_col, "").strip() if id_col else ""
        display_name = row.get(name_col, "").strip() if name_col else ""

        # Use whichever gives a non-empty key
        key = student_key or display_name
        if not key:
            continue  # skip rows with no identifiable student

        if key not in students:
            # Prefer "Name (ID)" if both are present, otherwise whichever exists
            if display_name and student_key and display_name != student_key:
                label = f"{display_name} ({student_key})"
            else:
                label = display_name or student_key
            students[key] = {"label": label, "quiz_scores": defaultdict(list)}

        # Quiz label (use "Score" as a fallback when no quiz column exists)
        quiz = row.get(quiz_col, "").strip() if quiz_col else "Score"
        if not quiz:
            quiz = "Score"

        score = safe_float(row.get(score_col, ""))
        if score is not None:
            students[key]["quiz_scores"][quiz].append(score)
        # Blank / non-numeric scores are silently skipped (logged below via "N/A")

    return students


# ---------------------------------------------------------------------------
# Report printing
# ---------------------------------------------------------------------------

def fmt(value):
    """Format a float to 2 decimal places, or return 'N/A'."""
    return f"{value:.2f}" if value is not None else "N/A"


def print_report(students):
    """Print the formatted summary report to stdout."""
    print("\nStudent Quiz Score Summary")
    print("==========================\n")

    if not students:
        print("No student data found.")
        return

    for data in students.values():
        print(f"Student: {data['label']}")

        quiz_scores = data["quiz_scores"]
        all_valid_scores = []

        # Sort quiz labels for deterministic output
        for quiz in sorted(quiz_scores.keys()):
            scores = quiz_scores[quiz]
            if scores:
                avg = mean(scores)
                all_valid_scores.extend(scores)
                print(f"  {quiz} Average: {fmt(avg)}")
            else:
                print(f"  {quiz} Average: N/A")

        overall = mean(all_valid_scores) if all_valid_scores else None
        print(f"  Overall Average: {fmt(overall)}")
        print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    headers, rows = load_csv(args.filepath)
    cols = detect_columns(headers)
    students = aggregate(rows, cols)
    print_report(students)


if __name__ == "__main__":
    main()
