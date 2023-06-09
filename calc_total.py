import csv
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('artist_twt.db')
c = conn.cursor()

# Connect to the database
conn = sqlite3.connect('artist_twt.db')
c = conn.cursor()

# Check if the total_engagements column exists, and if not, add it
c.execute("PRAGMA table_info(artist_twt)")
columns = [column[1] for column in c.fetchall()]
if 'total_engagements' not in columns:
    c.execute("ALTER TABLE artist_twt ADD COLUMN total_engagements INTEGER")

# Select all rows from the table
c.execute("SELECT * FROM artist_twt")

# Loop through the rows and calculate the total engagements for each artist
for row in c.fetchall():
    total_engagements = row[3] + row[4] + row[5] # tweets + retweets + mentions
    # Update the total_engagements column for the current row
    c.execute("UPDATE artist_twt SET total_engagements = ? WHERE id = ?", (total_engagements, row[0]))

# Commit the changes and close the connection
conn.commit()

# Retrieve all rows from the "artist_twt" table
c.execute("SELECT name, total_engagements FROM artist_twt")
rows = c.fetchall()

# Write the rows to a CSV file
with open('total_engagements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['name', 'total engagements'])
    # Write the data rows
    writer.writerows(rows)

conn.close()
