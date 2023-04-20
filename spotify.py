import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import requests
import os
import time



# authenticate with Spotipy using client ID and secret
client_id = '35a59c0bdc734f3bbcd14555e527ebaf'
client_secret = '0888a300374e42d19c442b2f91bc72d1'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Connect to the SQLite database
conn = sqlite3.connect('top_artists.db')
c = conn.cursor()

# Create the "top_artists" table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS top_artists
             (id TEXT PRIMARY KEY,
              name TEXT NOT NULL,
              streams INTEGER NOT NULL,
              followers INTEGER)''')

# Check how many rows are already in the table
c.execute("SELECT COUNT(*) FROM top_artists")
num_rows = c.fetchone()[0]

if num_rows < 100:
    # Retrieve the top 50 most streamed artists of 2021
    results = sp.search(q='year:2022', type='artist', limit=50)
    print()

    # Insert each artist into the "top_artists" table
    count = 0
    for item in results['artists']['items']:
        # Check if we have already inserted 100 items
        if num_rows + count >= 100:
            break

        artist_id = item['id']
        artist_name = item['name']
        artist_streams = item['popularity']
        artist_info = sp.artist(artist_id)
        followers = artist_info['followers']['total']
        c.execute("INSERT OR IGNORE INTO top_artists (id, name, streams,followers) VALUES (?, ?, ?, ?)",
                  (artist_id, artist_name, artist_streams,followers))
        count += 1

    # Retrieve the next 50 most streamed artists of 2021
    results = sp.search(q='year:2022', type='artist', limit=50, offset=50)

    # Insert each artist into the "top_artists" table
    count = 0
    for item in results['artists']['items']:
        # Check if we have already inserted 100 items
        if num_rows + count >= 100:
            break

        artist_id = item['id']
        artist_name = item['name']
        artist_streams = item['popularity']
        artist_info = sp.artist(artist_id)
        followers = artist_info['followers']['total']
        c.execute("INSERT OR IGNORE INTO top_artists (id, name, streams,followers) VALUES (?, ?, ?, ?)",
                  (artist_id, artist_name, artist_streams,followers))

        count += 1

# Commit the changes to the database and close the connection
conn.commit()
conn.close()

# Connect to the SQLite database
conn = sqlite3.connect('top_artists.db')
c = conn.cursor()

# Select all rows from the top_artists table
c.execute('SELECT * FROM top_artists')
rows = c.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()


# # connect to the SQLite database
# conn = sqlite3.connect('spotify.db')
# c = conn.cursor()

# # create the songs table if it doesn't exist
# c.execute('''CREATE TABLE IF NOT EXISTS songs
#              (title TEXT, artist TEXT, album TEXT, streams INTEGER, PRIMARY KEY(title, artist, album))''')

# # Retrieve top 100 streamed songs in 2022
# playlist_id = "37i9dQZEVXbLRQDuF5jeBp"
# offset = 0
# batch_size = 25
# song_data = []

# while True:
#     tracks = sp.playlist_tracks(playlist_id, limit=batch_size, offset=offset)
#     if not tracks["items"]:
#         break
    
#     # Extract relevant information from API response
#     for track in tracks["items"]:
#         song_info = {
#             "song_title": track["track"]["name"],
#             "artist_name": track["track"]["artists"][0]["name"],
#             "album_name": track["track"]["album"]["name"],
#             "number_of_streams": track["track"]["popularity"]
#         }
#         song_data.append(song_info)
#     print(song_info)

#     offset += batch_size

#     # Store data in SQLite database
#     if len(song_data) >= batch_size or not tracks["next"]:
#         conn = sqlite3.connect("mydatabase.db")
#         c = conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS top_100_streamed_songs_in_2022
#                      (song_title text, artist_name text, album_name text, number_of_streams integer)''')
#         for song in song_data:
#             c.execute("INSERT INTO top_100_streamed_songs_in_2022 VALUES (?, ?, ?, ?)",
#                       (song["song_title"], song["artist_name"], song["album_name"], song["number_of_streams"]))
#         conn.commit()
#         conn.close()
#         song_data = []

# results = sp.search(q='year:2022', type='track', limit=50, market='US')
# for i, track in enumerate(results['tracks']['items']):
#     track_name = track['name']
#     artist_name = track['artists'][0]['name']
#     num_streams = track['popularity']
#     print(f"{i+1}. {track_name} - {artist_name} ({num_streams} streams)")


# # Get the top 10 artists across all genres
# results1 = sp.search(q='year:2022', type='artist', limit=10)

# # Loop through the artists and get their information
# for i, artist in enumerate(results1['artists']['items']):
#     artist_name = artist['name']
#     artist_id = artist['id']
#     artist_info = sp.artist(artist_id)
#     num_followers = artist_info['followers']['total']
#     num_monthly_listeners = num_streams * 1000
#     print(f"{i+1}. {artist_name} - Followers: {num_followers} | Monthly Listeners: {num_monthly_listeners}")