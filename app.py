from flask import Flask, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

# Load API key
key_file = pd.read_csv("/Users/jpxmaestas/Desktop/last_fm_key.txt")
api_key = key_file.iloc[0, 0]

@app.route("/get_similar", methods=["POST"])
def get_similar():
    data = request.json
    track_name = data.get("track_name")
    artist_name = data.get("artist_name")

    print(f"Received: {track_name} by {artist_name}")

    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getSimilar",
        "track": track_name,
        "artist": artist_name,
        "api_key": api_key,
        "format": "json",
        "limit": 10
    }

    response = requests.get(url, params=params)
    similar_data = response.json()

    similar_tracks = similar_data.get("similartracks", {}).get("track", [])
    results = [
        {"name": t.get("name"), "artist": t.get("artist", {}).get("name")}
        for t in similar_tracks
    ]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
