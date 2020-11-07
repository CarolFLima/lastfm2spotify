import keys
import requests
import json

class last2spot():

    def __init__(self):
        self.last_api_key = keys.last_api_key()
        self.spotify_token = keys.spotify_token()
        self.spotify_id = keys.spotify_user_id()
        self.spotify_headers = {'Content-Type': 'application/json',
                                'Authorization': f'Bearer {self.spotify_token}'}
        self.playlist_id = ''
        self.song_uris = []

    def fetch_loved_tracks(self, user):
        url = f'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={user}&api_key={self.last_api_key}&format=json'
        response = requests.get(url, params=None)
        if response.status_code != 200:
            print('ERROR')
        else:
            res = response.json()
            for item in res['lovedtracks']['track']:
                song = item['name']
                artist = item['artist']['name']
                self.get_uri_from_spotify(song, artist)
                
    def get_uri_from_spotify(self, song, artist):
        url = f'https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=1'
        response = requests.get(url, headers=self.spotify_headers)
        if response.status_code == 200:
            res = response.json()
            for item in res['tracks']['items']:
                self.song_uris.append(item['uri'])

    def create_playlist(self):
        info_request = {
            "name": "Lastfm loved songs",
            "description": "carolflima loved songs on lastfm",
            "public": True
        }
        url = f'https://api.spotify.com/v1/users/{self.spotify_id}/playlists'
        response = requests.post(url, data=json.dumps(info_request), headers=self.spotify_headers)
        if response.status_code != 201:
            print(f'ERROR: {response.content}')
        else:
            res = response.json()
            self.playlist_id = res['uri'].replace('spotify:playlist:', '')
        
    def add_songs_to_playlist(self):
        url = f'https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks'
        response = requests.post(url, data=json.dumps(self.song_uris), headers=self.spotify_headers)
        if response.status_code == 201:
            print('Playlist created with success')

inst = last2spot()
inst.fetch_loved_tracks('carolflima')
inst.create_playlist()
inst.add_songs_to_playlist()

