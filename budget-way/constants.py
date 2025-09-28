import os

from dotenv import load_dotenv

load_dotenv("../.env")

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

TRANSACTIONS_FILE_PATH = "/expenses.csv"
