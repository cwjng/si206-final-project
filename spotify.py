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
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

# Create the "top_artists" table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS top_artists
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              artist_id TEXT NOT NULL,
              name TEXT NOT NULL,
              popularity INTEGER NOT NULL,
              followers INTEGER)''')

# Create the "song_info" table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS song_info
             (id INTEGER PRIMARY KEY,
              artist_id INTEGER NOT NULL,
              name TEXT NOT NULL,
              top_song TEXT NOT NULL,
              popularity INTEGER NOT NULL,
              FOREIGN KEY (artist_id) REFERENCES top_artists(id))''')

# Check how many rows are already in the table
c.execute("SELECT COUNT(*) FROM top_artists")
num_rows = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM song_info")
num_rows2 = c.fetchone()[0]

if num_rows < 100:
    # Retrieve the top 25 most streamed artists of 2021
    results = sp.search(q='year:2021', type='artist', limit=25, offset=num_rows)

    # Insert each artist into the "top_artists" table
    for item in results['artists']['items']:
        artist_id = item['id']
        artist_name = item['name']
        artist_popularity = item['popularity']
        artist_info = sp.artist(artist_id)
        followers = artist_info['followers']['total']

        c.execute("INSERT OR IGNORE INTO top_artists (artist_id, name, popularity, followers) VALUES (?, ?, ?, ?)",
                  (artist_id, artist_name, artist_popularity, followers))
        artist_row_id = c.lastrowid

        # Check if the number of rows in song_info is less than 100 before inserting data
        if num_rows2 < 100:
            top_tracks = sp.artist_top_tracks(artist_id)
            top_track = top_tracks['tracks'][0]
            top_track_name = top_track['name']
            top_track_popularity = top_track['popularity']

            c.execute("INSERT INTO song_info (artist_id, name, top_song, popularity) VALUES (?, ?, ?, ?)",
                      (artist_row_id, artist_name, top_track_name, top_track_popularity))
            num_rows2 += 1
        else:
            break

        num_rows += 1

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()



# # Connect to the SQLite database
# conn = sqlite3.connect('top_artists.db')
# c = conn.cursor()

# # Select all rows from the top_artists table
# c.execute('SELECT * FROM top_artists')
# rows = c.fetchall()

# # Print the results
# for row in rows:
#     print(row)

# # Close the connection
# conn.close()

