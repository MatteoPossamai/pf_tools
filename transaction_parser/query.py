import argparse
from datetime import datetime

import pandas as pd

from constants import CONVERSION_RATES, TRANSACTIONS_FILE_PATH


def get_df(file: str):
    df = pd.read_csv(file, names=["date", "category", "issuer", "amount", "currency"], skiprows=1)
    return df


def filter_transactions(
    df_in: pd.DataFrame,
    start_date=None,
    end_date=None,
    category=None,
    transaction_type=None,
    currency="GBP",
):
    """
    Filter transactions based on optional parameters.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: [timestamp, category, merchant, amount, currency]
    start_date : str or datetime, optional
        Start date for filtering (format: 'YYYY-MM-DD'). Default: 2000-01-01
    end_date : str or datetime, optional
        End date for filtering (format: 'YYYY-MM-DD'). Default: 2099-12-31
    category : str, optional
        Specific category to filter by (e.g., 'food', 'bills'). Default: None (all categories)
    transaction_type : str, optional
        'i' for income (positive amounts) or 'e' for expense (negative amounts). Default: None (all)

    Returns:
    --------
    pandas.DataFrame
        Filtered transactions matching all specified criteria
    """

    df: pd.DataFrame = df_in.copy()
    df["amount"] = df["amount"].astype(float)

    if start_date is None:
        start_date = "2000-1-1"

    if end_date is None:
        end_date = "2099-12-31"

    mask = (df["date"] >= start_date) & (df["date"] <= end_date)

    if category is not None:
        mask &= df["category"] == category

    if transaction_type is not None:
        if transaction_type.lower() == "i":
            mask &= df["amount"] > 0
        elif transaction_type.lower() == "e":
            mask &= df["amount"] < 0

    df = df[mask]
    df["amount"] = df.apply(
        lambda row: float(row["amount"]) * CONVERSION_RATES[row["currency"]][currency], axis=1
    )
    df["currency"] = currency
    return df


def summarize_transactions(df: pd.DataFrame):
    """
    Prints the transactions in a readable tabular format,
    along with the total amount and number of transactions.
    """
    # Print the table
    print("\n--- Transactions ---")
    print(df.to_string(index=False))

    # Compute summary
    total_amount = df["amount"].sum()
    num_transactions = len(df)

    # Print summary
    print("\n--- Summary ---")
    print(f"Total transactions: {num_transactions}")
    if num_transactions > 0:
        print(f"Total amount: {total_amount:.2f} {df['currency'].iloc[0]}")
    else:
        print(f"Total amount: 0")


def main():
    parser = argparse.ArgumentParser(
        description="Summarize financial transactions from a CSV file."
    )

    parser.add_argument(
        "--start_date",
        type=str,
        default=None,
        help="Filter transactions from this date (inclusive)",
    )
    parser.add_argument(
        "--end_date", type=str, default=None, help="Filter transactions up to this date (inclusive)"
    )
    parser.add_argument("--category", type=str, default=None, help="Filter by category")
    parser.add_argument(
        "--transaction_type", type=str, default=None, help="Filter by transaction type"
    )
    parser.add_argument(
        "--currency", type=str, default="GBP", help="Target currency (default: GBP)"
    )

    args = parser.parse_args()
    df = get_df(TRANSACTIONS_FILE_PATH)

    transaction_df = filter_transactions(
        df, args.start_date, args.end_date, args.category, args.transaction_type, args.currency
    )
    summarize_transactions(transaction_df)


if __name__ == "__main__":
    main()
