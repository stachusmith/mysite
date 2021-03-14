from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.humanize.templatetags.humanize import naturaltime
from .secret_settings import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from  import APIView

from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
# Create your views here.


#import urllib.request
import requests
import json
import base64
import datetime
import re
import sqlite3
import random

class AuthView(APIView):
    def get(self, request, format=None):
        scopes = 'playlist-read-private playlist-modify-private'




        form = UpadatePlaylistForm()
        ctx = {'form' = form}
        return(render(request, self.template_name, ctx))

#------------------------------------------------------------------------------
#old python script for spotify playlist download as reference and guide:
#------------------------------------------------------------------------------

    def post(self, request):

        spotify_URL = 'https://accounts.spotify.com/api/token'
        def get_creds (client_ID, client_secret): #secret settings
            #GETTING THE ACCESS TOKEN:
            

            client_creds=f'{client_ID}:{client_secret}' #secret settings
            client_creds_b64 = base64.b64encode(client_creds.encode())  
            
            token_data={
                'grant_type':'client_credentials'
            }

            token_headers={
                'Authorization': f'Basic {client_creds_b64.decode()}'
            }
            
            return {'token_data':token_data, 'token_headers':token_headers }
        
        form = UpadatePlaylistForm(request.POST)
        
        if not form.is_valid():
            ctx = {'form': form }
            return render(request, self.template_name, ctx)
        
        token = get_creds(client_ID, client_secret)


        return redirect(spotify_URL, data=token_data, headers=token_headers)
        #r=requests.post(spotify_URL, data=token_data, headers=token_headers)
        data=r.json()
        at = data['access_token']
        playlist_id = request.POST['playlist_number']

        specific_playlist_url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

        auth_header={
            'Authorization': f'Bearer {at}'
        }

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


        return redirect(reverse('spotify_download:playlist_print'))

class GetCredsView(View):
    


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