import tweepy
import sqlite3
import time
from datetime import datetime, timedelta

# Twitter API credentials
API_KEY = 'ff6Jux1PcSViS0NtS8VTiD493'
API_SECRET_KEY = '8ib4jYOYC0wUHFdOkmplF81e8k7u7iKy9LrYDXvwdXXkMwz2yr'
ACCESS_TOKEN = '1013599543861145600-IMj9ZIWpf9oIxzISxSAhmnf6pH6Jtk'
ACCESS_TOKEN_SECRET = 'Mjc0p3ECxdGIvs25BVUQ4K6yv8vvjCdxAI3lvJXuaCdwM'

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

# Verify authentication
try:
    api.verify_credentials()
    print("Authentication successful!")
except Exception as e:
    print("Error during authentication:", e)

# Connect to SQLite database
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

# Create a new database called 'artist_twt'
conn2 = sqlite3.connect('artist_twt.db')
c2 = conn2.cursor()
c2.execute('''CREATE TABLE IF NOT EXISTS artist_twt
             (id INTEGER PRIMARY KEY,
              name TEXT,
              popularity INTEGER,
              tweet INTEGER,
              retweet INTEGER,
              mention INTEGER)''')

# Initialize the last searched artist name
last_artist_name = ''
# Initialize the counter
artist_count = 0

# Loop until all artists are searched
while True:
    # Get 25 distinct artists from the database, starting from the last searched artist
    artists = c.execute("SELECT name, popularity FROM top_artists").fetchall()

    # Stop the loop if no more artists are found
    if not artists:
        break

    # Loop through artists and count tweets, retweets and mentions
    for artist in artists:
        if artist_count >= 25:
            break
        else:
            artist_count += 1
            print(artist_count)
            # Construct query string for artist search
            query = f"{artist[0]} OR @{artist[0]} since:{(datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')}"

            # Get tweets containing the artist name
            while True:
                try:
                    tweets = tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended').items(66)
                    break
                except tweepy.TooManyRequests as e:
                    time.sleep(60*15) # wait 15 minutes before trying again

            # Count tweets, retweets and mentions
            tweet_count = 0
            retweet_count = 0
            mention_count = 0
            print('Searching for tweets for ' + artist[0])
            for tweet in tweets:
                # Check if the artist name is mentioned in the tweet text or full text
                if artist[0].lower() in tweet.full_text.lower():
                    tweet_count += 1
                # Check if the tweet is a retweet and increment retweet count
                if hasattr(tweet, 'retweeted_status'):
                    retweet_count += 1
                # Check if the tweet mentions another user and increment mention count
                if tweet.entities['user_mentions']:
                    mention_count += 1


            # Update artist record in new database
            c2.execute("INSERT INTO artist_twt (name, popularity, tweet, retweet, mention) VALUES (?, ?, ?, ?, ?)",
                    (artist[0], artist[1], tweet_count, retweet_count, mention_count))
            conn2.commit()
            print("Changes committed")

            # Set the last searched artist name to the current artist
            last_artist_name = artist[0]

            # Sleep for a short period to avoid hitting Twitter API rate limits
            time.sleep(1)
print('Last artist is ' + last_artist_name)
# Close database connection
conn.close()
