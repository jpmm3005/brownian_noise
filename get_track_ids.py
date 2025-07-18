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

track_names = df.iloc[:, 1].dropna().astype(str).str.strip().unique().tolist()
track_artist = df.iloc[:,2].dropna().astype(str).str.strip().unique().tolist()

