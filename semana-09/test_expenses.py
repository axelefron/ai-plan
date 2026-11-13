"""Tests for the expense analyzer. Run from semana-09: python3 -m pytest -v"""

import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from expenses import classify, format_markdown, main, read_expenses, summarize

HEADER = "date,description,amount\n"


def filesystem_is_case_insensitive():
    """True if the temp folder's disk treats "probe.txt" and "PROBE.TXT" as the same file."""
    with tempfile.TemporaryDirectory() as folder:
        (Path(folder) / "probe.txt").touch()
        return (Path(folder) / "PROBE.TXT").exists()


def write_csv(folder, content, name="expenses.csv"):
    path = folder / name
    path.write_text(content, encoding="utf-8")
    return path


# ---------- classify ----------

@pytest.mark.parametrize(
    "description, expected",
    [
        ("Walmart Supercenter", "groceries"),
        ("Trader Joe's", "groceries"),
        ("Lyft ride downtown", "transportation"),
        ("Netflix", "subscriptions"),
        ("Comcast internet", "utilities"),
        ("CVS Pharmacy", "health"),
        ("Chipotle", "dining"),
    ],
)
def test_classify_known_keyword(description, expected):
    assert classify(description) == expected


def test_classify_ignores_case_and_accents():
    assert classify("CAFÉ LATTE") == "dining"
    assert classify("walgreens") == "health"


def test_classify_no_match_is_other():
    assert classify("Birthday gift") == "other"


def test_classify_does_not_match_substrings():
    # "Targeted" contains "target" and "Vegas" contains "gas", but neither is the whole word.
    assert classify("Targeted ad") == "other"
    assert classify("Las Vegas trip") == "other"


def test_classify_first_category_wins():
    # "Uber Eats" matches dining ("uber eats") and transportation ("uber"); dining comes first.
    assert classify("Uber Eats") == "dining"
    categories = {"first": ["coffee"], "second": ["coffee"]}
    assert classify("Coffee to go", categories) == "first"


# ---------- read_expenses ----------

def test_read_valid_csv(tmp_path):
    path = write_csv(tmp_path, HEADER + "2026-10-01,Publix,100.50\n")
    assert read_expenses(path) == [
        {"date": date(2026, 10, 1), "description": "Publix", "amount": Decimal("100.50")}
    ]


def test_read_missing_column(tmp_path):
    path = write_csv(tmp_path, "date,description\n2026-10-01,Publix\n")
    with pytest.raises(ValueError, match="amount"):
        read_expenses(path)


@pytest.mark.parametrize(
    "row",
    ["2026-10-01,Publix,abc\n", "10/01/2026,Publix,100\n", "2026-13-01,Publix,100\n", "2026-10-01,Publix,NaN\n"],
)
def test_read_invalid_row_mentions_line(tmp_path, row):
    path = write_csv(tmp_path, HEADER + row)
    with pytest.raises(ValueError, match="line 2"):
        read_expenses(path)


def test_read_reports_all_invalid_rows(tmp_path):
    content = HEADER + "2026-10-01,Publix,abc\n2026-10-02,Lyft,50\nbad,Netflix,10\n"
    path = write_csv(tmp_path, content)
    with pytest.raises(ValueError) as error:
        read_expenses(path)
    assert "line 2" in str(error.value)
    assert "line 4" in str(error.value)


def test_read_csv_with_bom(tmp_path):
    # Excel's "CSV UTF-8" adds a BOM at the start; the header must still be read as "date".
    path = tmp_path / "bom.csv"
    path.write_text(HEADER + "2026-10-01,Publix,100.50\n", encoding="utf-8-sig")
    assert read_expenses(path) == [
        {"date": date(2026, 10, 1), "description": "Publix", "amount": Decimal("100.50")}
    ]


def test_read_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_expenses(tmp_path / "does_not_exist.csv")


def test_read_empty_csv(tmp_path):
    path = write_csv(tmp_path, HEADER)
    assert read_expenses(path) == []


# ---------- summarize ----------

def test_summarize_by_month_and_category():
    expenses = [
        {"date": date(2026, 9, 1), "description": "Publix", "amount": Decimal("100")},
        {"date": date(2026, 9, 5), "description": "Lyft", "amount": Decimal("50")},
        {"date": date(2026, 9, 9), "description": "Costco", "amount": Decimal("25")},
        {"date": date(2026, 10, 1), "description": "Netflix", "amount": Decimal("10")},
    ]
    summary = summarize(expenses)
    assert list(summary) == ["2026-09", "2026-10"]
    assert summary["2026-09"]["groceries"] == Decimal("125")
    assert summary["2026-09"]["transportation"] == Decimal("50")
    assert summary["2026-10"] == {"subscriptions": Decimal("10"), "total": Decimal("10")}


def test_summarize_exact_decimals():
    expenses = [
        {"date": date(2026, 10, 1), "description": "Publix", "amount": Decimal("10.10")},
        {"date": date(2026, 10, 2), "description": "Publix", "amount": Decimal("20.20")},
    ]
    assert summarize(expenses)["2026-10"]["groceries"] == Decimal("30.30")


def test_summarize_total_is_sum_of_categories():
    expenses = [
        {"date": date(2026, 10, 1), "description": "Walmart", "amount": Decimal("100.25")},
        {"date": date(2026, 10, 2), "description": "Lyft", "amount": Decimal("40.75")},
        {"date": date(2026, 10, 3), "description": "Gift", "amount": Decimal("9")},
    ]
    month = summarize(expenses)["2026-10"]
    category_sum = sum((v for k, v in month.items() if k != "total"), Decimal("0"))
    assert month["total"] == category_sum == Decimal("150.00")


# ---------- format_markdown and end-to-end ----------

def test_markdown_contains_months_and_categories():
    summary = {
        "2026-09": {"groceries": Decimal("125"), "total": Decimal("125")},
        "2026-10": {"transportation": Decimal("50.5"), "total": Decimal("50.5")},
    }
    text = format_markdown(summary)
    assert "## 2026-09" in text
    assert "## 2026-10" in text
    assert "| groceries | 125.00 |" in text
    assert "| transportation | 50.50 |" in text


def test_main_creates_output_and_leaves_csv_unchanged(tmp_path):
    input_csv = write_csv(tmp_path, HEADER + "2026-10-01,Publix,100\n2026-10-02,Lyft,50\n")
    original = input_csv.read_bytes()
    output = tmp_path / "summary.md"

    assert main([str(input_csv), "--output", str(output)]) == 0

    assert output.exists()
    assert "## 2026-10" in output.read_text(encoding="utf-8")
    assert input_csv.read_bytes() == original


def test_main_invalid_csv_does_not_create_summary(tmp_path):
    input_csv = write_csv(tmp_path, HEADER + "2026-10-01,Publix,abc\n")
    output = tmp_path / "summary.md"
    assert main([str(input_csv), "--output", str(output)]) == 1
    assert not output.exists()


def test_main_output_same_as_input_aborts(tmp_path):
    input_csv = write_csv(tmp_path, HEADER + "2026-10-01,Publix,100\n")
    original = input_csv.read_bytes()
    assert main([str(input_csv), "--output", str(input_csv)]) == 1
    assert input_csv.read_bytes() == original


def test_main_output_in_missing_folder_returns_error(tmp_path, capsys):
    input_csv = write_csv(tmp_path, HEADER + "2026-10-01,Publix,100\n")
    output = tmp_path / "missing_folder" / "summary.md"
    # If save_summary raised instead of being caught, this call would crash the test.
    assert main([str(input_csv), "--output", str(output)]) == 1
    assert "Error: could not save the summary" in capsys.readouterr().err
    assert not output.exists()


@pytest.mark.skipif(not filesystem_is_case_insensitive(), reason="filesystem is case-sensitive")
def test_main_output_same_file_different_case_aborts(tmp_path):
    input_csv = write_csv(tmp_path, HEADER + "2026-10-01,Publix,100\n", name="expenses.csv")
    original = input_csv.read_bytes()
    same_file_other_case = tmp_path / "EXPENSES.csv"
    assert main([str(input_csv), "--output", str(same_file_other_case)]) == 1
    assert input_csv.read_bytes() == original
