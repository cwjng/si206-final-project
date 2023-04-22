import matplotlib.ticker as ticker
import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('artist_twt.db')
c = conn.cursor()

# Select all 100 artists and their data
c.execute("SELECT id, name, popularity, tweet, retweet, mention, total_engagements FROM artist_twt ORDER BY popularity DESC LIMIT 25")
data = c.fetchall()

# Extract the data for the scatter plot
names = [row[1] for row in data]
popularity = [row[2] for row in data]
engagements = [row[6] for row in data]


# Create a scatter plot of the data with smaller markers
plt.scatter(popularity, engagements, c='green')

# Set the x and y-axis labels and title
plt.xlabel('Spotify popularity')
plt.ylabel('Twitter Engagements')
plt.title('Correlation Between Spotify Popularity and Twitter Engagements')

# Add text labels for each point
for i, name in enumerate(names):
    plt.annotate(name, (popularity[i], engagements[i]), fontsize=8)

# Adjust the y-axis tick increment
y_locator = ticker.MultipleLocator(10)
plt.gca().yaxis.set_major_locator(y_locator)

# Show the plot
plt.show()

# Close the database connection
conn.close()