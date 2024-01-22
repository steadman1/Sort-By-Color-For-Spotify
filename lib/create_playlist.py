import requests

def create_playlist(access_token, user_info):
    # Create a new playlist
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': 'My Cool Playlist',
        'description': 'My cool playlist description',
        'public': False
    }
    response = requests.post(
        'https://api.spotify.com/v1/users/' + user_info['id'] + '/playlists',
        headers=headers,
        json=data
    )
    response_data = response.json()
    playlist_id = response_data['id']

    # Search for songs
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': 'genre:hip-hop',
        'type': 'track',
        'limit': 5
    }
    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    response_data = response.json()
    track_ids = [track['id'] for track in response_data['tracks']['items']]

    # Add songs to playlist
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'uris': [f'spotify:track:{track_id}' for track_id in track_ids]
    }
    response = requests.post(
        'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks',
        headers=headers,
        json=data
    )

    return response.json()
