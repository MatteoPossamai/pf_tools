import pandas as pd
from constants import corrections

base_path = "/home/matteopossamai/Dropbox/personal_data"
expenses_path = f"{base_path}/expenses.csv"
incomes_path = f"{base_path}/incomes.csv"
merged_path = f"{base_path}/transactions.csv"

expenses = pd.read_csv(expenses_path)
incomes = pd.read_csv(incomes_path)

expenses["amount"] = -expenses["amount"]
merged = pd.concat([expenses, incomes], ignore_index=True)
merged["date"] = pd.to_datetime(merged["date"])
merged = merged.sort_values(by="date", ignore_index=True)
merged = merged.drop(columns=["id"])
merged["issuer"] = merged["issuer"].replace(corrections)
merged.to_csv(merged_path, index=False)

print("Merged and sorted data:")
print(merged)

print("Issuers:", set(merged["issuer"]))
print("Categories:", set(merged["category"]))
print("Currencies:", set(merged["currency"]))