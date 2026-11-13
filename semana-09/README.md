# Week 9 — Expense analyzer

A small command-line tool that reads a CSV of expenses, classifies each one into a
category by keyword (US merchants such as Publix, Costco, Shell, Netflix), and totals
the amounts by category and by month. It prints the summary as a Markdown table and
saves it to a file.

- Input: a CSV with the columns `date` (YYYY-MM-DD), `description` and `amount`.
- Every row is validated. If any row has a bad date or amount, the tool reports all
  the bad rows (line number + reason) and stops without writing anything.
- Amounts use `Decimal`, so totals have no floating-point rounding errors.
- Categories and keywords live in `categories.py`; the logic lives in `expenses.py`.
  Descriptions that match no keyword go to `other`.

## How to run

From the `semana-09` folder, with the repo's virtual environment active:

```bash
python3 expenses.py sample_expenses.csv [--output file.md]
```

Without `--output`, the summary is saved to `semana-09/summary.md`, which is
git-ignored. The tool refuses to write the output over the input CSV.

## How to run the tests

From the `semana-09` folder:

```bash
python3 -m pytest -v
```

## Example output

Real output of running the tool on `sample_expenses.csv` (fictional data):

```
# Expense summary

## 2026-09

| Category | Total (USD) |
|---|---:|
| dining | 33.75 |
| groceries | 170.94 |
| health | 24.99 |
| other | 40.00 |
| subscriptions | 15.49 |
| transportation | 60.85 |
| utilities | 96.20 |
| **Month total** | **442.22** |

## 2026-10

| Category | Total (USD) |
|---|---:|
| dining | 13.85 |
| groceries | 204.30 |
| health | 30.00 |
| other | 22.50 |
| subscriptions | 11.99 |
| transportation | 12.00 |
| utilities | 79.99 |
| **Month total** | **374.63** |
```

After the summary, the tool prints one more line, `Summary saved to <path>`, with the
absolute path of the output file.

## Limitations

- **Keyword-based classification.** A description is matched against fixed keywords
  as whole words, so variants are missed: `WAL-MART` does not match `walmart` and
  falls into `other`.
- **`--output` inside the repo is not git-ignored.** Only the default
  `semana-09/summary.md` is in `.gitignore`. If `--output` points to any other file
  inside the repo, that file can be committed, so never use it with real data.
- **The input CSV is never modified.** The tool only reads it.
