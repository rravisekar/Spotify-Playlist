from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

time_travel = input("Enter the date you want to create Spotify playlist? Format YYYY-MM-DD")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{time_travel}")

year_splice = time_travel.split("-")[0]
print(year_splice)

billboard_url = response.text

soup = BeautifulSoup(billboard_url, "html.parser")

song_list = soup.find_all(name="span", class_="chart-element__information__song")
song_artist_list = soup.find_all(name="span", class_="chart-element__information__artist")

song_final_list = [song.getText() for song in song_list]

print(song_final_list)

scope = "playlist-modify-private"

sp: Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

spotify_user_id = sp.current_user()["id"]
print(spotify_user_id)

spotify_playlist = f"Billboard Top 100 {time_travel}"
playlist = sp.user_playlist_create(user=spotify_user_id, name=spotify_playlist, public=False)

playlists_id = playlist["id"]
print(playlists_id)

spotify_tracks = []
for song in song_final_list:
    song_uri = f"track:{song} year:{year_splice}"
    result = sp.search(q=song_uri, type="track")
    items = result['tracks']['items']
    if len(items) > 0:
        track = items[0]
        print(track['name'], track['id'])
        spotify_tracks.append(track['id'])

print(spotify_tracks)

sp.playlist_add_items(playlist_id=playlists_id, items=spotify_tracks)