import requests

with open("static/access_token.txt") as f:
    token = f.read().strip()

headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.spotify.com/v1/me", headers=headers)
print(response.json())
