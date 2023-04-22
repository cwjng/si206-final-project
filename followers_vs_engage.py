import sqlite3
import matplotlib.pyplot as plt

# Connect to the databases
spotify_conn = sqlite3.connect('spotify.db')
spotify_c = spotify_conn.cursor()

twitter_conn = sqlite3.connect('artist_twt.db')
twitter_c = twitter_conn.cursor()

# Join the tables
spotify_c.execute('''SELECT song_info.popularity, artist_twt.engagement 
                     FROM song_info JOIN artist_twt ON song_info.artist_id = artist_twt.artist_id''')
rows = spotify_c.fetchall()

# Extract the data
x = [row[0] for row in rows] # Spotify popularity
y = [row[1] for row in rows] # Twitter engagement

# Create the scatterplot
fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.5)

ax.set_xlabel('Spotify Popularity')
ax.set_ylabel('Twitter Engagement')

plt.show()

# Close the connections
spotify_conn.close()
twitter_conn.close()
