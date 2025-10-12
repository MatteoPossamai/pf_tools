BASE_PATH = "/home/matteopossamai/Dropbox/personal_data"
TRANSACTIONS_FILE_PATH = f"{BASE_PATH}/transactions.csv"

GBP_GBP = 1
EUR_GBP = 0.87
CONVERSION_RATES = {
    "GBP": {"GBP": 1, "EUR": 1.15, "USD": 1.34},
    "EUR": {"EUR": 1, "GBP": 0.87, "USD": 1.16},
    "USD": {"USD": 1, "GBP": 0.75, "EUR": 0.86},
}
