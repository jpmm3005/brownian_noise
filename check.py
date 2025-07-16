import requests

def check_token_scopes(token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return

    scopes = response.headers.get("scope")
    print(f"Token scopes: {scopes}")
    print(f"User info: {response.json()}")

# Example usage:
with open("static/access_token.txt") as f:
    token = f.read().strip()

check_token_scopes(token)
