import requests
import base64

client_id = 'b64fd8d41ec347fc9920a1549e265fcc'
client_secret = '2352537c1c6841188786b761450556e3'

auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Step 1: Request token using Client Credentials Flow
token_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={'grant_type': 'client_credentials'},
    headers={'Authorization': f'Basic {auth_header}'}
)

print("Token response:", token_response.json())

access_token = token_response.json().get("access_token")

# Step 2: Query known valid audio feature
test_track_id = '3n3Ppam7vgaVa1iaRUc9Lp'  # Red Hot Chili Peppers – Californication

r = requests.get(
    f'https://api.spotify.com/v1/audio-features/{test_track_id}',
    headers={'Authorization': f'Bearer {access_token}'}
)

print("Audio features response:", r.status_code, r.text)
