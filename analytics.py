import pandas as pd
import numpy as np
df = pd.read_csv('static/top_tracks(2).csv')

df['popularity'] = (df['popularity']).astype(int)

minimum = min(df['popularity'])
maximum = max(df['popularity'])
least_popular = df[df['popularity'] == minimum ]
most_popular = df[df['popularity'] == maximum]

print(str(least_popular))


print(most_popular)
