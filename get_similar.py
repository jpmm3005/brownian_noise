import requests
import get_track_ids
import pandas as pd

# Input from Spotify
track_name = get_track_ids.track_names[0]
artist_name = get_track_ids.track_artist[0]

key_file = pd.read_csv("/Users/jpxmaestas/Desktop/last_fm_key.txt")
api_key = key_file.iloc[0,0]


print(track_name)
print(artist_name)



# Build the Last.fm API request
url = "http://ws.audioscrobbler.com/2.0/"
params = {
    "method": "track.getSimilar",
    "track": track_name,
    "artist": artist_name,
    "api_key": api_key,
    "format": "json",
    "limit": 10  # adjust as needed
}

# Fetch similar tracks
response = requests.get(url, params=params)
data = response.json()

# Display results
similar_tracks = data.get("similartracks", {}).get("track", [])
for i, track in enumerate(similar_tracks, 1):
    name = track.get("name")
    artist = track.get("artist", {}).get("name")
    print(f"{i}. {name} by {artist}")
