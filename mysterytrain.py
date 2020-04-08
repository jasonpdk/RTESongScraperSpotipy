# mysterytrain.py
# Scrapes RTE Lyric FM Mystery Train for songs played, then adds these songs to a spotify playlist
#
# Note: This should really be combined into jcscrape.py, rather than dupicating code.
#
# Jason Keane - jason@keane.id

## IMPORTS
import urllib
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import datetime
import sys

## SPOTIFY AUTH
username = 'XYZ'
client_id = 'XYZ'
client_secret = 'XYZ'
redirect_uri = 'XYZ'

token = util.prompt_for_user_token(username, scope='playlist-modify-private,playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

## BEAUTIFUL SOUP STUFF
site = sys.argv[1]

try:
    page = urllib.request.urlopen(site)
except urllib.error.URLError as e:
    exit(e)

playlist_id=''
if "mystery-train" in site:
    playlist_id = '63FeF82sd4AzWdk0tPP0Q3'
else:
    exit("Unsupported URL")

soup = BeautifulSoup(page, 'html.parser')

music_played_div = soup.find('div', attrs={'class':'m32-music-played-on-show my2'})
music_rows = music_played_div.findAll('div', attrs={'class':'small-12 columns border-bottom fill-white p2'})

tracks = []
for music_row in music_rows:
    songHTML = music_row.find('div', attrs={'class':'small-10 mb2 columns text-purple-lyricfm'})
    row = songHTML.findAll('p', attrs={'class':'mb1'})

    artist = ''
    song = ''
    for item in row:
        keyValue = item.findAll('span', attrs={'class':'mb1'})
        key = keyValue[0].text.rstrip()
        value = keyValue[1].text.rstrip()

        if key == 'Title:':
            song = value
        elif key == 'Performer(s):':
            artist = value

    query = song + " " + artist

    results = sp.search(q=query, type='track', limit=1)

    print(song + " - " + artist)
    print("Something found? " + len(results['tracks']['items']))

    for i, t in enumerate(results['tracks']['items']):
        ## Add spotify id to list
        tracks.append(t['id'])

# Add tracks to playlist
sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=tracks)
