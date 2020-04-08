# jcscrape.py
# Scrapes RTE Radio 1's John Creedon Show and Simply Folk for songs played, then adds these songs to a spotify playlist
#
# Note: This is not entirely accurate. It totally depends on the way the song and artist are writen on the website. It searches Spotify for song + artist and accepts
# the top result, this can be innacurate. Improvements are very welcome!
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

playlist_id = ''
if "john-creedon" in site:
    playlist_id = '0UDHYyisJpU8Zj3JTOgA4a'
elif "simply-folk" in site:
    playlist_id = '23JPqer5rWR1lsfTpkWfm4'
else:
    exit("Unsupported URL")

soup = BeautifulSoup(page, 'html.parser')

date_block = soup.find('div', attrs={'class':'fill-blue-radio1 px2 py1 block overflow-hidden text-white mb1'})
date_par = date_block.find('p', attrs={'class':'mb0'})
date_string = date_par.find('span', attrs={'class':'bold'}).text

music_played_div = soup.find('div', attrs={'class':'m32-music-played-on-show my2'})
music_rows = music_played_div.findAll('div', attrs={'class':'small-12 columns border-bottom fill-white p2'})

tracks = []
for music_row in music_rows:
    songHTML = music_row.find('div', attrs={'class':'small-9 medium-10 columns mb2'})
    song = songHTML.find('p', attrs={'class':'mb1'}).text
    artist = songHTML.find('p', attrs={'class':'mb1 bold'}).text

    ## Sometimes RTE add (Vocal)/(Vocals) onto the end. This helps stop getting some karaoke versions, etc.
    if artist.endswith("(Vocal)"):
        artist = artist[:-len("(Vocal)")]
    elif artist.endswith("(Vocals)"):
        artist = artist[:-len("(Vocals)")]

    ## Spotify search, query "song artist", gets the top result. This is obviouly not 100% accurate all of the time
    query = song + " " + artist
    results = sp.search(q=query, type='track', limit=1)

    for i, t in enumerate(results['tracks']['items']):
        print("Title: " + song + " Artist: " + artist + " Spotify ID: " + t['id'])
        ## Add spotify id to list
        tracks.append(t['id'])

## Add tracks to playlist
sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=tracks)
