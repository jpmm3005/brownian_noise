import pandas as pd
import numpy as np
from spotipy import Spotify

# Read token from file
with open('access_token.txt') as f:
    access_token = f.read().strip()

sp = Spotify(auth=access_token)

df = pd.read_csv('top_tracks.csv')
track_ids = df.iloc[:, 0].dropna().unique().tolist()

audio_features = []
for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i + 100]
    features = sp.audio_features(batch)
    audio_features.extend([f for f in features if f])

features_df = pd.DataFrame(audio_features)
features_df.to_csv('audio_features.csv', index=False)
print("✅ Saved audio features to audio_features.csv")
