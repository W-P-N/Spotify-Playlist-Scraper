from datetime import date as dt
from pprint import pprint

from bs4 import BeautifulSoup
import requests as rq
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk


URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "<client_id>"
CLIENT_SECRET = "<client_secret_key>"
REDIRECT_URI = "http://example.com"

user_date = input("which year do you want to travel to? Type the date in the format YYYY-MM-DD ("
                  "eg: 2022-01-01): ")

response = rq.get(url=f"{URL}{user_date}")

webpage_billboard = response.text

soup = BeautifulSoup(webpage_billboard, "html.parser")

title_list = [' '.join(item.getText().split()) for item in soup.find_all("h3",
                                                                         class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")]
print(title_list)

scope = "playlist-modify-private"
s_p = sp.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope,
                              show_dialog=True,
                              cache_path="token.txt"))

user_id = s_p.current_user()["id"]
year = user_date.split("-")[0]
song_uris = []
for song in title_list:
    result = s_p.search(q=f"track:{song} year:{year}", type="track")
    pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = s_p.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
# print(playlist)

s_p.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

ui = tk.Tk()

