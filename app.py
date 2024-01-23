from flask import Flask, request, redirect, render_template
import requests
import urllib.parse
from lib.playlist_tools import create_playlist, get_all_playlists

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
def callback_route():
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
        return render_template('index.html', display_name=user_info['display_name'])
    else:
        return 'Failed to retrieve access token', 400
    
@app.route('/pick_playlist')
def pick_playlist_route():
    if not user_info:
        return 'User not logged in', 400
    
    playlists = get_all_playlists(access_token)["items"]

    return render_template('pick_playlist.html', display_name=user_info['display_name'], playlists=playlists)

@app.route('/sort_playlist')
def sort_playlist_route():
    if not user_info:
        return 'User not logged in', 400
    
    playlist_id = request.args.get('playlist_id')

    create_playlist(access_token, playlist_id, user_info)

    return render_template('sort_playlist.html', display_name=user_info['display_name'])

if __name__ == '__main__':
    app.run(debug=True)
