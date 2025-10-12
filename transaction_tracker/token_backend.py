import json
from dataclasses import dataclass, asdict
from typing import Optional

MONZO_API_URL = "https://api.monzo.com"
MONZO_API_TRANSACTION_ENDPOINT = "transactions"
BASE_PATH = "/home/matteopossamai/Dropbox/personal_data"
TRANSACTIONS_FILE_PATH = f"{BASE_PATH}/transactions.csv"
TOKEN_FILE = "monzo_tokens.json"


@dataclass
class MonzoData:
    client_id: str
    secret: str
    redirect_uri: str
    account_id: str
    access_token: Optional[str]
    access_token_expiry: Optional[int]
    refresh_token: Optional[str]

    @staticmethod
    def from_file(file: str) -> "MonzoData":
        with open(file, "r") as f:
            data = json.load(f)
            return MonzoData(**data)

    def to_file(self, file: str) -> None:
        with open(file, "w") as f:
            json.dump(asdict(self), f)
