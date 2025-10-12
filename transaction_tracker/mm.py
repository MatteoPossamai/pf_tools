import json
import os
from datetime import datetime
from monzo.authentication import Authentication, MonzoAuthenticationError, MonzoError

MONZO_CLIENT_ID = "XXX"
MONZO_SECRET = "XXX"
REDIRECT_URI = "https://developers.monzo.com"
TOKEN_FILE = "monzo_tokens.json"


def save_tokens(monzo):
    """Save tokens to a JSON file for future use"""
    tokens = {
        "access_token": monzo.access_token,
        "access_token_expiry": monzo.access_token_expiry,
        "refresh_token": monzo.refresh_token,
        "saved_at": datetime.now().isoformat()
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"✓ Tokens saved to {TOKEN_FILE}")


def load_tokens():
    """Load tokens from file if they exist"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def initial_authentication():
    """First-time setup: authenticate and get initial tokens"""
    print("=" * 60)
    print("FIRST-TIME SETUP: Initial Monzo Authentication")
    print("=" * 60)
    
    monzo = Authentication(
        client_id=MONZO_CLIENT_ID,
        client_secret=MONZO_SECRET,
        redirect_url=REDIRECT_URI
    )
    
    print("\n1. Go to this URL and approve the app:\n")
    auth_url = monzo.authentication_url + "&access_type=offline"
    print(auth_url)
    
    print("\n2. After approval, you'll be redirected. Copy the URL from your browser.")
    redirect_url = input("\nPaste the full redirect URL here: ").strip()
    
    # Extract code and state from redirect URL
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
    
    save_tokens(monzo)
    return monzo


def get_authenticated_client():
    """
    Get an authenticated Monzo client, either by loading saved tokens
    or by doing initial authentication
    """
    tokens = load_tokens()
    
    if tokens:
        print("=" * 60)
        print("Using saved tokens...")
        print("=" * 60)
        
        monzo = Authentication(
            client_id=MONZO_CLIENT_ID,
            client_secret=MONZO_SECRET,
            redirect_url=REDIRECT_URI,
            access_token=tokens["access_token"],
            access_token_expiry=tokens["access_token_expiry"],
            refresh_token=tokens["refresh_token"]
        )
        
        # Check if token is expired and needs refresh
        if tokens["access_token_expiry"] < datetime.now().timestamp():
            print("⚠ Access token expired. Refreshing...")
            try:
                monzo.refresh_access()
                print("✓ Token refreshed successfully")
                save_tokens(monzo)
            except (MonzoAuthenticationError, MonzoError) as e:
                print(f"❌ Failed to refresh token: {e}")
                print("Please authenticate again...")
                return initial_authentication()
        else:
            time_left = tokens["access_token_expiry"] - datetime.now().timestamp()
            hours_left = int(time_left / 3600)
            print(f"✓ Token valid for {hours_left} more hours")
        
        return monzo
    else:
        print("No saved tokens found. Starting initial authentication...")
        return initial_authentication()


def example_usage():
    """Example of using the authenticated client"""
    monzo = get_authenticated_client()
    
    # Make your API calls here
    print("\n" + "=" * 60)
    print("Ready to make API calls!")
    print("=" * 60)
    print(f"Current Access Token: {monzo.access_token[:20]}...")
    print(f"Expires at: {datetime.fromtimestamp(monzo.access_token_expiry)}")
    
    # After making API calls, save tokens again (in case they were refreshed)
    save_tokens(monzo)


if __name__ == "__main__":
    example_usage()