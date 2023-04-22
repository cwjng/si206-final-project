import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('artist_twt.db')
c = conn.cursor()

# Select the top 25 artists by total engagements
c.execute("SELECT name, tweets, retweets, mentions, total_engagements FROM artist_twt ORDER BY total_engagements DESC LIMIT 25")

# Create empty lists for the data
names = []
tweets = []
retweets = []
mentions = []

# Loop through the data and append it to the appropriate list
for row in c.fetchall():
    names.append(row[0])
    tweets.append(row[1])
    retweets.append(row[2])
    mentions.append(row[3])

# Set the x-axis tick locations and labels
x_ticks = range(len(names))
plt.xticks(x_ticks, names, rotation=90)

# Create the bar chart
bar_width = 0.2
plt.bar([x - bar_width for x in x_ticks], tweets, width=bar_width, label='Tweets')
plt.bar(x_ticks, retweets, width=bar_width, label='Retweets')
plt.bar([x + bar_width for x in x_ticks], mentions, width=bar_width, label='Mentions')

# Add chart title and axis labels
plt.title('Engagements by Artist (Top 25)')
plt.xlabel('Artist')
plt.ylabel('Number of Engagements')

# Add a legend
plt.legend()

# Adjust figure size and spacing
plt.gcf().set_size_inches(16, 8)
plt.subplots_adjust(bottom=0.2)

# Display the chart
plt.show()
