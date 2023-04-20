import requests 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '35a59c0bdc734f3bbcd14555e527ebaf'
client_secret = '0888a300374e42d19c442b2f91bc72d1'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


results = sp.search(q='year:2023', type='track', limit=10, market='US')
for i, track in enumerate(results['tracks']['items']):
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    num_streams = track['popularity']
    print(f"{i+1}. {track_name} - {artist_name} ({num_streams} streams)")


# Get the top 10 artists across all genres
results1 = sp.search(q='year:2022', type='artist', limit=10)

# Loop through the artists and get their information
for i, artist in enumerate(results1['artists']['items']):
    artist_name = artist['name']
    artist_id = artist['id']
    artist_info = sp.artist(artist_id)
    num_followers = artist_info['followers']['total']
    num_monthly_listeners = num_streams * 1000
    print(f"{i+1}. {artist_name} - Followers: {num_followers} | Monthly Listeners: {num_monthly_listeners}")