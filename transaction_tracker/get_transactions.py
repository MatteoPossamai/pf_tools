from datetime import datetime, timedelta, timezone
import csv
import requests

from token_backend import (
    TOKEN_FILE,
    TRANSACTIONS_FILE_PATH,
    MONZO_API_TRANSACTION_ENDPOINT,
    MONZO_API_URL,
)
from token_manager import TokenManager


def get_latest_date(path: str) -> str:
    last_line: str = ""
    with open(path, "rb") as f:
        f.seek(-2, 2)
        while f.read(1) != b"\n":
            f.seek(-2, 1)
        last_line = f.readline().decode()

    if not last_line:
        raise Exception(f"Unable to get last line from file {path}")

    last_date = last_line.split(",")[0]
    return last_date


def plus_one_second(datetime_info: str) -> str:
    dt = datetime.strptime(datetime_info, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    dt_plus_one = dt + timedelta(seconds=1)
    return dt_plus_one.isoformat().replace("+00:00", "Z")


def get_transactions_after(
    token_manager: TokenManager,
    datetime_info: str,
) -> list:
    retries = 0
    account_id = token_manager.monzo_data.account_id
    
    while retries < 3:
        access_token = token_manager.monzo_data.access_token
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"account_id": account_id, "since": datetime_info}
        response = requests.get(
            f"{MONZO_API_URL}/{MONZO_API_TRANSACTION_ENDPOINT}", headers=headers, params=params
        )
        if response.status_code != 200:
            token_manager.monzo_auth.refresh_access()
            retries += 1
            print(response, response.status_code)
        else:
            data: dict = response.json()
            if len(data.keys()) > 0:
                return data["transactions"]
            else:
                return []
            
    raise Exception(
        f"Unable to query endpoint."
    )




def serialize_and_write(transactions: list, path: str):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        for transaction in transactions:
            date = transaction["created"]
            tmp_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            date = tmp_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            category = transaction["category"]
            currency = transaction["local_currency"]
            amount = str(int(transaction["local_amount"]) / 100)
            issuer = transaction.get("counterparty", {}).get("name")
            if issuer:
                issuer = issuer.upper().replace(" ", "_")
            else:
                issuer = transaction.get("description").split("  ")[0].upper().replace(" ", "_")

            if "212" not in issuer and not issuer.startswith("POT_"):
                writer.writerow([date, category, issuer, amount, currency])


def update_with_latest_trades(path: str):
    datetime_from = plus_one_second(get_latest_date(path))
    token_manager = TokenManager(TOKEN_FILE)
    transactions = get_transactions_after(token_manager, datetime_from)
    serialize_and_write(transactions, path)


if __name__ == "__main__":
    update_with_latest_trades(TRANSACTIONS_FILE_PATH)
