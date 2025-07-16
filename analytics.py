import pandas as pd
import requests

# Load access token
with open("static/access_token.txt") as f:
    token = f.read().strip()

headers = {
    "Authorization": f"Bearer {token}"
}

# Load track IDs from CSV (assuming first column contains track IDs)
df = pd.read_csv("static/top_tracks.csv")
track_ids = df.iloc[:, 0].dropna().astype(str).str.strip().unique().tolist()

for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i + 100]
    ids_param = ",".join(batch)
    url = f"https://api.spotify.com/v1/audio-features?ids={ids_param}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("This works")
        data = response.json()
        # Optionally print something about data here
    else:
        print(f"this is not working. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
