## IMPORTS
from urllib.request import urlopen
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import datetime
import sys
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime

## SPOTIFY AUTH
username = 'XYZ'
client_id = 'XYZ'
client_secret = 'XYZ'
redirect_uri = 'XYZ'
playlist_id='XYZ'

token = util.prompt_for_user_token(username, scope='playlist-modify-private,playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

## BEAUTIFUL SOUP STUFF
site = sys.argv[1]


page = urlopen(site)

soup = BeautifulSoup(page, 'html.parser')

date_block = soup.find('div', attrs={'class':'fill-blue-radio1 px2 py1 block overflow-hidden text-white mb1'})
date_par = date_block.find('p', attrs={'class':'mb0'})
date_string = date_par.find('span', attrs={'class':'bold'}).text

music_played_div = soup.find('div', attrs={'class':'m32-music-played-on-show my2'})
music_rows = music_played_div.findAll('div', attrs={'class':'small-12 columns border-bottom fill-white p2'})

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Speedtest-4d674b2c34b4.json', scope)

gc = gspread.authorize(credentials)


date = ''
if "john-creedon" in site:
    playlist_id = '0UDHYyisJpU8Zj3JTOgA4a'
    date = date_string.replace('John Creedon ', '')
    worksheet = gc.open('John Creedon Show Song List').sheet1
elif "simply-folk" in site:
    playlist_id = '23JPqer5rWR1lsfTpkWfm4'
    date = date_string.replace('Simply Folk ', '')
    worksheet = gc.open('Simply Folk Song List').sheet1


print(date)

tracks = []
for music_row in music_rows:
    songHTML = music_row.find('div', attrs={'class':'small-9 medium-10 columns mb2'})
    song = songHTML.find('p', attrs={'class':'mb1'}).text
    artist = songHTML.find('p', attrs={'class':'mb1 bold'}).text

    worksheet.append_row([date, artist, song])

    ## Spotify search, query "song artist", gets the top result. This is obviouly not 100% accurate all of the time
    query = song + " " + artist
    results = sp.search(q=query, type='track', limit=1)

    for i, t in enumerate(results['tracks']['items']):
        print("Title: " + song + " Artist: " + artist + " Spotify ID: " + t['id'])
        ## Add spotify id to list
        tracks.append(t['id'])

## Add tracks to playlist
sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=tracks)
