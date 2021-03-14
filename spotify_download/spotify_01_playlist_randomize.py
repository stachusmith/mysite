
#import urllib.request
import requests
import json
import base64
import datetime
import re
import sqlite3
import random

#GETTING THE ACCESS TOKEN:
spotify_URL = 'https://accounts.spotify.com/api/token'
client_ID='5b66ee41706b453a8138240f86387725'
client_secret='907184993c07408d8d54c6f54ae150ac'

method='POST'

client_creds=f'{client_ID}:{client_secret}'
client_creds_b64 = base64.b64encode(client_creds.encode())
#print(client_creds_b64)
#---------------------------------------------------------
token_data={
    'grant_type':'client_credentials'
}
#print(token_data)
#---------------------------------------------------------
token_headers={
    'Authorization': f'Basic {client_creds_b64.decode()}'
}
#print(token_headers)
#---------------------------------------------------------

r=requests.post(spotify_URL, data=token_data, headers=token_headers)
data=r.json()
#print(data)

at = data['access_token']
#print(at)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#GETTING THE PLAYLIST:

playlist_id=input('Please enter Playlist ID:')

if len(playlist_id)<1:
    playlist_id='6iPtsbYANrLDncDJQeTson'

specific_playlist_url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

#-------------------------------------------------------------------------------
auth_header={
    'Authorization': f'Bearer {at}'
}
#-------------------------------------------------------------------------------

conn = sqlite3.connect('randomize.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Track_ID;


CREATE TABLE Track_ID (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
track_id TEXT UNIQUE
);
''')

#-------------------------------------------------------------------------------


r1=requests.get(specific_playlist_url, headers=auth_header)
playlist=r1.json()
#print(json.dumps(playlist, indent=4))
items_ = playlist['items']
#items_=tracks['items']
count=0
track_ids=list()
random_nos=list()
for item in items_:
    for track_id in item:
        track_id=item['track']['id']
    count=count+1

    print(f'{count}    -   {track_id}')
    cur.execute('''INSERT OR REPLACE INTO Track_ID (track_id)
        VALUES (?)''', (track_id, ))
conn.commit()

user=input('Please enter user_id')
if len(user)<1:
    user='stanislawguy'
create_pl=f'https://api.spotify.com/v1/users/{user}/playlists'
r2=requests.post(create_pl, data={'name':f'Randomized {playlist_id}', 'description':f'this is the randomized {playlist_id}', 'public':True}, headers=auth_header)
randomized_pl=r2.json()
print(randomized_pl)


cur.execute('SELECT track_id FROM Track_ID ORDER BY RANDOM()')
#for row in cur :
    #print(row[0])
