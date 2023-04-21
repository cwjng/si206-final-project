import matplotlib.ticker as ticker
import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('top_artists.db')
c = conn.cursor()

# Select all 100 artists and their data
c.execute("SELECT id, name, streams, tweets, retweets, mentions, total_engagements FROM top_artists ORDER BY streams DESC LIMIT 25")
data = c.fetchall()

# Extract the data for the scatter plot
names = [row[1] for row in data]
streams = [row[2] for row in data]
engagements = [row[6] for row in data]


# Create a scatter plot of the data with smaller markers
plt.scatter(streams, engagements, c='green')

# Set the x and y-axis labels and title
plt.xlabel('Spotify Streams (per million)')
plt.ylabel('Twitter Engagements')
plt.title('Correlation Between Spotify Streams and Twitter Engagements')

# Add text labels for each point
for i, name in enumerate(names):
    plt.annotate(name, (streams[i], engagements[i]), fontsize=8)

# Adjust the y-axis tick increment
y_locator = ticker.MultipleLocator(10)
plt.gca().yaxis.set_major_locator(y_locator)

# Show the plot
plt.show()

# Close the database connection
conn.close()



# import sqlite3
# import matplotlib.pyplot as plt

# # Connect to the database
# conn = sqlite3.connect('top_artists.db')
# c = conn.cursor()

# # Select all 100 artists and their data
# c.execute("SELECT id, name, streams, tweets, retweets, mentions, total_engagements FROM top_artists ORDER BY streams DESC LIMIT 25")
# data = c.fetchall()

# # Extract the data for the scatter plot
# names = [row[1] for row in data]
# streams = [row[2] for row in data]
# engagements = [row[6] for row in data]

# # Create a scatter plot of the data with smaller markers
# plt.scatter(streams, engagements, s=50, alpha=0.5)


# # Add labels and a title to the plot
# plt.xlabel('Spotify Streams')
# plt.ylabel('Twitter Engagements')
# plt.title('Correlation Between Spotify Streams and Twitter Engagements')


# # Add text labels for each point
# for i, name in enumerate(names):
#     plt.annotate(name, (streams[i], engagements[i]), fontsize=8)

# # Show the plot
# plt.show()

# # Close the database connection
# conn.close()
