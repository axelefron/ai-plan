"""Expense analyzer for a CSV file.

Usage:
    python3 expenses.py sample_expenses.csv [--output summary.md]

Reads a CSV with date, description and amount columns, classifies each
expense into a category, totals by category and by month, prints the
summary and saves it as Markdown. The input CSV is only read, never modified.
"""

import argparse
import csv
import os
import re
import sys
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from categories import CATEGORIES, DEFAULT_CATEGORY

COLUMNS = ("date", "description", "amount")
DEFAULT_OUTPUT = Path(__file__).parent / "summary.md"


def normalize(text):
    """Lowercase the text and strip accents ("CAFÉ" -> "cafe")."""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(c for c in decomposed if not unicodedata.combining(c))
    return without_accents.lower()


def classify(description, categories=CATEGORIES):
    """Return the first category with a keyword that appears as a whole word."""
    text = normalize(description)
    for category, keywords in categories.items():
        for keyword in keywords:
            # \b = word boundary: "gas" matches "Shell gas" but not "Las Vegas".
            if re.search(rf"\b{re.escape(normalize(keyword))}\b", text):
                return category
    return DEFAULT_CATEGORY


def read_expenses(path):
    """Read the CSV and return a list of expenses with date (date) and amount (Decimal).

    Every row is validated. If any row is invalid, raise a single ValueError
    listing all the bad rows (line number + reason).
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    expenses = []
    errors = []
    # utf-8-sig ignores the BOM that Excel adds to "CSV UTF-8" files.
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing columns in CSV: {', '.join(missing)}")

        for row in reader:
            line = reader.line_num
            reasons = []

            raw_date = (row["date"] or "").strip()
            try:
                expense_date = date.fromisoformat(raw_date)
            except ValueError:
                reasons.append(f"invalid date {raw_date!r} (expected YYYY-MM-DD)")

            raw_amount = (row["amount"] or "").strip()
            try:
                amount = Decimal(raw_amount)
                if not amount.is_finite():  # Decimal accepts "NaN" and "Infinity"
                    raise InvalidOperation
            except InvalidOperation:
                reasons.append(f"invalid amount {raw_amount!r}")

            if reasons:
                errors.append(f"line {line}: {'; '.join(reasons)}")
            else:
                description = (row["description"] or "").strip()
                expenses.append({"date": expense_date, "description": description, "amount": amount})

    if errors:
        raise ValueError("The CSV has invalid rows:\n" + "\n".join(errors))
    return expenses


def summarize(expenses):
    """Total the amounts by month and category.

    Returns {"2026-10": {"dining": Decimal, ..., "total": Decimal}, ...}
    with months and categories sorted.
    """
    totals = {}
    for expense in expenses:
        month = expense["date"].strftime("%Y-%m")
        category = classify(expense["description"])
        by_category = totals.setdefault(month, {})
        by_category[category] = by_category.get(category, Decimal("0")) + expense["amount"]

    summary = {}
    for month in sorted(totals):
        categories = dict(sorted(totals[month].items()))
        categories["total"] = sum(categories.values(), Decimal("0"))
        summary[month] = categories
    return summary


def format_markdown(summary):
    """Build the Markdown text: one section per month with a totals table."""
    lines = ["# Expense summary", ""]
    if not summary:
        lines += ["No expenses to summarize.", ""]
    for month, categories in summary.items():
        lines += [f"## {month}", "", "| Category | Total (USD) |", "|---|---:|"]
        for category, total in categories.items():
            if category != "total":
                lines.append(f"| {category} | {total:.2f} |")
        lines.append(f"| **Month total** | **{categories['total']:.2f}** |")
        lines.append("")
    return "\n".join(lines)


def save_summary(text, output_path):
    """Write the summary to the output path (overwrites it if it exists)."""
    Path(output_path).write_text(text, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize expenses from a CSV by category and month.")
    parser.add_argument("csv", help="path to a CSV with date, description, amount columns")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Markdown output file")
    args = parser.parse_args(argv)

    input_path = Path(args.csv).resolve()
    output_path = Path(args.output).resolve()
    # samefile also catches paths that differ only in case on macOS (case-insensitive disk).
    same_file = input_path == output_path or (
        input_path.exists() and output_path.exists() and os.path.samefile(input_path, output_path)
    )
    if same_file:
        print("Error: the output cannot be the same file as the input CSV.", file=sys.stderr)
        return 1

    try:
        expenses = read_expenses(input_path)
    # OSError covers FileNotFoundError, PermissionError, IsADirectoryError, etc.
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    text = format_markdown(summarize(expenses))
    print(text)
    try:
        save_summary(text, output_path)
    except OSError as error:
        print(f"Error: could not save the summary: {error}", file=sys.stderr)
        return 1
    print(f"Summary saved to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
