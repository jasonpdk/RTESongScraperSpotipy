## IMPORTS
from urllib.request import urlopen
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util

## SPOTIFY AUTH
username = 'XYZ'
client_id = 'XYZ'
client_secret = 'XYZ'
redirect_uri = 'XYZ'
playlist_id='XYZ'

token = util.prompt_for_user_token(username, scope='playlist-modify-private,playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

## BEAUTIFUL SOUP STUFF
site = 'https://www.rte.ie/radio1/john-creedon/programmes/2019/0411/1042176-john-creedon-thursday-11-april-2019/'

page = urlopen(site)
soup = BeautifulSoup(page, 'html.parser')
music_played_div = soup.find('div', attrs={'class':'m32-music-played-on-show my2'})
music_rows = music_played_div.findAll('div', attrs={'class':'small-12 columns border-bottom fill-white p2'})

tracks = []
for music_row in music_rows:
    songHTML = music_row.find('div', attrs={'class':'small-9 medium-10 columns mb2'})
    song = songHTML.find('p', attrs={'class':'mb1'}).text
    artist = songHTML.find('p', attrs={'class':'mb1 bold'}).text

    ## Spotify search, query "song artist", gets the top result. This is obviouly not 100% accurate all of the time
    query = song + " " + artist
    results = sp.search(q=query, type='track', limit=1)
    
    for i, t in enumerate(results['tracks']['items']):
        print("Title: " + song + " Artist: " + artist + " Spotify ID: " + t['id'])
        ## Add spotify id to list
        tracks.append(t['id']) 

## Add tracks to playlist
sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=tracks)
