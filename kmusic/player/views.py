from django.shortcuts import render
from django.http import HttpResponse

import requests
import json

from .SpotifyAuth import SpotifyAuth
# Create your views here.

def index(request):
    return render(request, "player/index.html")


def callback(request):
    code = request.GET.get("code", None)
    spotify_auth=SpotifyAuth(code)
    auth = spotify_auth.getAuth()

    res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": auth})
    response = json.loads(res.text)
    print("response: ", response)
    artist_id = response["item"]["artists"][0]["id"]
    res2 = requests.get("https://api.spotify.com/v1/artists/"+artist_id, headers={"Authorization": auth})
    response2 = json.loads(res2.text)
    print("response2: ", response2)
    context = {
        "song_title" : response["item"]["name"],
        "song_artist" : response["item"]["artists"][0]["name"],
        "song_art" : response["item"]["album"]["images"][0]["url"],
        "artist_image" : response2["images"][0]["url"],

    }
    return render(request, "player/index.html", context)