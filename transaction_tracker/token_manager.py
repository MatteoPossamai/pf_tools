from token_backend import MonzoData

from datetime import datetime
from monzo.authentication import Authentication


class TokenManager:
    file: str
    monzo_data: MonzoData
    monzo_auth: Authentication

    def __init__(self, file: str) -> None:
        self.file = file
        self.monzo_data = MonzoData.from_file(file)

        if any(
            data is None
            for data in [
                self.monzo_data.access_token,
                self.monzo_data.access_token_expiry,
                self.monzo_data.refresh_token,
            ]
        ):
            self._bootstrap()

        assert self.monzo_data.access_token is not None
        assert self.monzo_data.access_token_expiry is not None
        assert self.monzo_data.refresh_token is not None
        self.monzo_auth = Authentication(
            client_id=self.monzo_data.client_id,
            client_secret=self.monzo_data.secret,
            redirect_url=self.monzo_data.redirect_uri,
            access_token=self.monzo_data.access_token,
            access_token_expiry=self.monzo_data.access_token_expiry,
            refresh_token=self.monzo_data.refresh_token,
        )

    def _bootstrap(self):

        monzo = Authentication(
            client_id=self.monzo_data.client_id,
            client_secret=self.monzo_data.secret,
            redirect_url=self.monzo_data.redirect_uri,
        )

        print("\n1. Go to this URL and approve the app:\n")
        auth_url = monzo.authentication_url + "&access_type=offline"
        print(auth_url)

        print("\n2. After approval, you'll be redirected. Copy the URL from your browser.")
        redirect_url = input("\nPaste the full redirect URL here: ").strip()

        try:
            from urllib.parse import urlparse, parse_qs

            parsed = urlparse(redirect_url)
            params = parse_qs(parsed.query)
            code = params.get("code", [None])[0]
            state = params.get("state", [None])[0]

            if not code or not state:
                print("❌ Could not extract code or state from URL")
                exit(1)

            monzo.authenticate(authorization_token=code, state_token=state)
        except Exception as e:
            print(f"❌ Error parsing redirect URL: {e}")
            exit(1)

        print("\n✓ Authentication successful!")
        print(f"Access Token: {monzo.access_token[:20]}...")
        print(f"Refresh Token: {monzo.refresh_token[:20]}...")
        print(f"Expires at: {datetime.fromtimestamp(monzo.access_token_expiry)}")

        self.monzo_data = MonzoData(
            self.monzo_data.client_id,
            self.monzo_data.secret,
            self.monzo_data.redirect_uri,
            self.monzo_data.account_id,
            monzo.access_token,
            monzo.access_token_expiry,
            monzo.refresh_token,
        )
        self.monzo_data.to_file(self.file)

        self.monzo_auth = monzo
