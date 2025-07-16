import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth


from spotipy import Spotify

access_token = 'BQD2T6GueFt_5KU77n1_zCtDzdG-Z2TLGcSPj_c1X_MAQZEsC0f-TMx0HL01hG5Fk7Dlj7OLykNz9HyVq0CEMOX_HTau04-oz142nPVE0r6zyXa0HN2WlBbu7yiwcjJndy790qgSmijF6mgD5RTnHXpYpoURb8SojEtqEOKjYIP-EPUc5qzhem3EH3vVziM8Zqsc6FQl0yXC-LWSw5RkhTRa0YVbtcDFVOtvTkMdJlaR6hW1BvUCNZ0eiQ'
sp = Spotify(auth=access_token)
#https://accounts.spotify.com/en/authorize?response_type=code&client_id=b64fd8d41ec347fc9920a1549e265fcc&scope=user-top-read&redirect_uri=https%3A%2F%2Fjpmm3005.github.io%2Fbrownian_noise%2F&code_challenge_method=S256&code_challenge=dipfWgeRnRTGvH0pJhb_j8SgEa47YedZH2MqVTHlg_U

df = pd.read_csv('static/top_tracks.csv')
track_ids = df.iloc[:, 0].dropna().unique().tolist()

# Spotify API allows max 100 IDs per request
audio_features = []
for i in range(0, len(track_ids), 100):
    batch = track_ids[i:i + 100]
    features = sp.audio_features(batch)
    # Remove None values (in case of invalid IDs)
    audio_features.extend([f for f in features if f])

# Convert to DataFrame and export
features_df = pd.DataFrame(audio_features)
features_df.to_csv('static/audio_features.csv', index=False)

print("Saved audio features to 'static/audio_features.csv'")

