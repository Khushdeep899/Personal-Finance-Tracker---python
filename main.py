from matplotlib import pyplot as plt
import pandas as pd
import csv
from datetime import date, datetime
import logging
from data_entry import get_date, get_amount, get_category, get_description

#Logging setup
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

#Custom exceptions
class FinanceError(Exception):
    """Base exception for finance related error."""
    pass

class ValidationError(FinanceError):
    """Raised when validation fails."""
    pass

class CSVFileError(FinanceError):
    """Raised when CSV file operations fail."""
    pass



class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
            logging.info(f"CSV file '{cls.CSV_FILE}' found and loaded successfully.")
        except FileNotFoundError:
            try:
                df = pd.DataFrame(columns=cls.COLUMNS)
                df.to_csv(cls.CSV_FILE, index=False)
                logging.info(f"CSV file '{cls.CSV_FILE}' created successfully.")
            except Exception as e:
                logging.error(f"Failed to create CSV file '{cls.CSV_FILE}': {e}")
                raise CSVFileError(f"Failed to create CSV file: {e}")    

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date" : date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        logging
        print("Entry added successfully.")


    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df.columns = [c.lower() for c in df.columns]
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date   = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found for the specified date range.")
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to "
                  f"{end_date.strftime(cls.FORMAT)}:")
            print(filtered_df.to_string(index=False,
                                       formatters={"date": lambda x: x.strftime(cls.FORMAT)}))

        total_income  = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
        print("\nSummary:")
        print(f"Total Income:  {total_income:.2f}")
        print(f"Total Expense: {total_expense:.2f}")
        print(f"Net Savings:   {total_income - total_expense:.2f}")


 

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (DD-MM-YYYY):", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df = pd.read_csv(CSV.CSV_FILE)
    df.columns = [c.lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
    df.dropna(subset=["amount"], inplace=True)

    income_df = df[df["category"] == "Income"].groupby("date")["amount"].sum()
    expense_df = df[df["category"] == "Expense"].groupby("date")["amount"].sum()

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df.values, label="Income", marker='o')
    plt.plot(expense_df.index, expense_df.values, label="Expense", marker='o')
    plt.title("Income and Expense Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add a new entry")
        print("2. View transactions")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (DD-MM-YYYY): ")
            end_date = get_date("Enter the end date (DD-MM-YYYY): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").strip().lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
                    

if __name__ == "__main__":
    main()
