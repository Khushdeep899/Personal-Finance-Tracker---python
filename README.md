# Personal Finance Tracker (Python)

A simple command-line personal finance tracker that stores income and expense entries in CSV and provides transaction summaries and plots.

## Features

- Add dated finance entries with:
  - Amount
  - Category (Income/Expense)
  - Description
- View transactions for a custom date range
- Get income/expense/net summary for that range
- Optional time-series plot for Income and Expense
- CSV-based persistence (`finance_data.csv`)

## Project Structure

- `main.py` - Main CLI app, CSV handling, transaction listing, and plotting
- `data_entry.py` - User input validation helpers (date, amount, category, description)
- `finance_data.csv` - Stored entries (created automatically if missing)

## Requirements

- Python 3.8+
- `pandas`
- `matplotlib`

## Setup

1. Clone or download this folder.
2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install pandas matplotlib
```

## Run the App

```bash
python main.py
```

Follow the menu:
1. Add a new entry
2. View transactions (with date range)
3. Exit

##  Usage Notes

- Date format is always `DD-MM-YYYY`.
- Category input is `I` for Income and `E` for Expense.
- On transaction view, the app prints totals and net savings.
- You can choose to plot income vs expense over time after viewing.


##  Example Data

`finance_data.csv` is pre-populated with entries like:

- `20-02-2026,100,Income,Salary for June`
- `12-03-2026,150.0,Expense,travel`

##  How it Works 

1. `main.py` initializes the CSV if missing.
2. `add()` collects validated input from `data_entry.py`.
3. `CSV.add_entry()` appends rows to CSV.
4. `CSV.get_transactions()` filters rows by date and computes totals.
5. `plot_transactions()` displays an income/expense trend plot.

