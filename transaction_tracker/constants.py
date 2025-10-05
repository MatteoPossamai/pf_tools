import os

from dotenv import load_dotenv

load_dotenv("../.env")

# MONZO
MONZO_USER_ID = os.getenv("MONZO_USER_ID")
MONZO_ACCOUNT_ID = os.getenv("MONZO_ACCOUNT_ID")
MONZO_ACCESS_TOKEN = os.getenv("MONZO_ACCESS_TOKEN")
MONZO_API_URL = "https://api.monzo.com"
MONZO_API_TRANSACTION_ENDPOINT = "transactions"

# PATHS
BASE_PATH = "/home/matteopossamai/Dropbox/personal_data"
TRANSACTIONS_FILE_PATH = f"{BASE_PATH}/transactions.csv"