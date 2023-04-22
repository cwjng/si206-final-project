import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('artist_twt.db')
c = conn.cursor()

# Select the top 25 artists with the highest number of Twitter engagements
c.execute("SELECT id, name, popularity, tweets, retweets, mentions, total_engagements FROM artist_twt ORDER BY total_engagements DESC LIMIT 25")
data = c.fetchall()

# Extract the data for the scatter plot
names = [row[1] for row in data]
popularity = [row[2] for row in data]
engagements = [row[6] for row in data]

# Create a scatter plot of the data with smaller markers
plt.scatter(engagements, engagements)

# Set the x and y-axis labels and title
plt.xlabel('Twitter Engagements')
plt.ylabel('Spotify Popularity')
plt.title('Correlation Between Twitter Engagements and Spotify Popularity')

# Add text labels for each point
for i, name in enumerate(names):
    plt.annotate(name, (engagements[i], engagements[i]), fontsize=8)


# Show the plot
plt.show()

# Close the database connection
conn.close()
