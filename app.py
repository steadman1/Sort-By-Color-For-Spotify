from flask import Flask, request, redirect
import requests
import urllib.parse
from lib.create_playlist import create_playlist

app = Flask(__name__)

# Replace these with the values from your Spotify Developer Dashboard
CLIENT_ID = 'ba7faadbc5b940079f132523d028a1b3'
CLIENT_SECRET = '2eea4361222b4658a1643fe1e3fced27'
REDIRECT_URI = 'http://localhost:5000/callback'

# This scope will allow you to access a user's playlists
SCOPE = 'playlist-read-private playlist-modify-private playlist-modify-public'

# Generate a random state value for added security
import os
STATE = os.urandom(16).hex()

user_info = {}
access_token = None

@app.route('/')
def login():
    # Redirect the user to the Spotify authorization page
    auth_url = ('https://accounts.spotify.com/authorize?' +
                'response_type=code' +
                '&client_id=' + CLIENT_ID +
                '&scope=' + urllib.parse.quote(SCOPE) +
                '&redirect_uri=' + urllib.parse.quote(REDIRECT_URI) +
                '&state=' + STATE)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global user_info, access_token
    code = request.args.get('code')
    state = request.args.get('state')

    if state != STATE:
        return 'State mismatch', 400

    # Exchange the code for an access token
    auth_token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(auth_token_url, data=payload)
    response_data = response.json()

    access_token = response_data.get('access_token')

    if access_token:
        # Use the access token to access Spotify API
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_info = requests.get('https://api.spotify.com/v1/me', headers=headers).json()
        return f'Hello, {user_info["display_name"]}!'
    else:
        return 'Failed to retrieve access token', 400
    
@app.route('/create_playlist')
def create_playlist_route():

    print(user_info)

    if not user_info:
        return 'User not logged in', 400
    
    create_playlist(access_token, user_info)

    return 'Playlist created!'

if __name__ == '__main__':
    app.run(debug=True)