import pandas as pd
import requests
import base64

# Replace these with your actual client credentials
client_id = "b64fd8d41ec347fc9920a1549e265fcc"
client_secret = "2352537c1c6841188786b761450556e3"

# Encode credentials
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Get token from client credentials flow
auth_response = requests.post(
    "https://accounts.spotify.com/api/token",
    data={"grant_type": "client_credentials"},
    headers={"Authorization": f"Basic {auth_header}"}
)

token = auth_response.json().get("access_token")

if not token:
    print("❌ Could not retrieve access token.")
    print(auth_response.text)
    exit()

headers = {
    "Authorization": f"Bearer {token}"
}

# Load track IDs
df = pd.read_csv("static/top_tracks.csv")
track_ids = df.iloc[:, 0].dropna().astype(str).str.strip().unique().tolist()

audio_features = []
failed_ids = []

# Query in batches
for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i + 100]
    ids_param = ",".join(batch)
    url = f"https://api.spotify.com/v1/audio-features?ids={ids_param}"

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        audio_features.extend([f for f in data["audio_features"] if f is not None])
    else:
        print(f"❌ Batch failed with status {response.status_code}")
        print(f"Response: {response.text}")
        failed_ids.extend(batch)

# Save results
pd.DataFrame(audio_features).to_csv("audio_features.csv", index=False)
print(f"✅ Saved {len(audio_features)} audio features.")

if failed_ids:
    pd.DataFrame(failed_ids, columns=["track_id"]).to_csv("failed_track_ids.csv", index=False)
    print(f"⚠️ Saved {len(failed_ids)} failed IDs.")
