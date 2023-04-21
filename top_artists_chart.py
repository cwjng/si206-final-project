import sqlite3
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

# Retrieve the data from the "top_artists" table and extract the top 20 artists by follower count
c.execute("SELECT name, followers FROM top_artists ORDER BY followers DESC LIMIT 20")
rows = c.fetchall()

# Create two lists, one for artist names and another for follower counts
names = [row[0] for row in rows]
followers = [row[1] for row in rows]

# Create a horizontal bar chart with matplotlib
plt.barh(names, followers)

# Customize the chart
plt.title("Top 20 Artists on Spotify by Follower Count")
plt.xlabel("Number of Followers")
plt.ylabel("Artist")
plt.tight_layout()

# Display the chart
plt.show()
