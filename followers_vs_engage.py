import sqlite3

# Connect to the spotify database
spotify_conn = sqlite3.connect('spotify.db')
spotify_c = spotify_conn.cursor()

# Attach the artist_twt database to the spotify database
spotify_c.execute("ATTACH DATABASE 'artist_twt.db' AS artist_twt")

# Query the combined databases using JOIN
spotify_c.execute('''SELECT song_info.popularity, artist_twt.tweet 
                     FROM song_info 
                     JOIN artist_twt.artist_twt ON song_info.artist_id = artist_twt.id''')

# Retrieve the results
results = spotify_c.fetchall()

# Close the connection to the databases
spotify_conn.close()

# Visualize the results using matplotlib
import matplotlib.pyplot as plt

x = [result[0] for result in results]
y = [result[1] for result in results]

plt.scatter(x, y)
plt.xlabel('Spotify Popularity')
plt.ylabel('Twitter Tweet')
plt.title("Twitter Tweet vs Spotify Popularity")
plt.show()
