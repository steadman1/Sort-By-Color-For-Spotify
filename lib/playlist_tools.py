import requests
from .image_to_color import image_to_color
from .sort_colors import sort_by_SOM, sort_by_rainbow, init_color_display

def get_all_playlists(access_token, offset=0):
    playlist_items = []
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    while True:
        response = requests.get(f"https://api.spotify.com/v1/me/playlists?offset{offset}", headers=headers)
        if response.status_code != 200 or len(response["items"]) <= 0:
            break
        playlist_items.append(response.json()["items"])
    return playlist_items

def get_track_image(track):
    images = track["track"]["album"]["images"]
    if len(images) > 0:
        return images[0]["url"]
    return None

def read_playlist(access_token, playlist_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id, headers=headers)
    return response.json()

def create_playlist(access_token, playlist_id, user_info):
    playlist = read_playlist(access_token, playlist_id)

    # Create a new playlist
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": f"{playlist['name']} (Sorted)",
        "description": "My cool playlist description",
        "public": False,
    }

    response = requests.post(
        "https://api.spotify.com/v1/users/" + user_info["id"] + "/playlists",
        headers=headers,
        json=data
    )
    response_data = response.json()
    print(response_data)
    new_playlist_id = response_data["id"]

    # add all tracks from playlist_id to new playlist
    tracks = playlist["tracks"]["items"]

    colors_with_ids = [(image_to_color(get_track_image(track)), f"spotify:track:{track['track']['id']}") for track in tracks]

    sorted_colors_with_ids = sort_by_SOM(colors_with_ids)
    init_color_display(sorted_colors_with_ids)

    track_ids = [track_id for (_, track_id) in sorted_colors_with_ids]

    for index in range(0, len(track_ids), 20):
        data = {
            "uris": track_ids[index:index+20]
        }
        response = requests.post(
            "https://api.spotify.com/v1/playlists/" + new_playlist_id + "/tracks",
            headers=headers,
            json=data
        )

    return response.json()
