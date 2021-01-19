from django.shortcuts import render, reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

import requests
import json
import time

from .SpotifyAuth import SpotifyAuth
from .SongQueue import SongQueue
# Create your views here.

def index(request):
    auth = getAuth(request)
    if auth==None:
        return render(request, "player/index.html")
    
    res_current = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": auth})
    if res_current.status_code==204:
        return render(request, "player/index.html", context={"song_title": "No song playing"})
    elif res_current.status_code==200:
        response = json.loads(res_current.text)
        sq = getSongQueue(request)
        sq.addItem(response["item"]["album"]["images"][0]["url"])
        request.session["songqueue"] = sq.toJSON()
        artist_id = response["item"]["artists"][0]["id"]
        res2 = requests.get("https://api.spotify.com/v1/artists/"+artist_id, headers={"Authorization":  auth})
        response2 = json.loads(res2.text)
        res_recents = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=9", headers={"Authorization":  auth})
        response_recents = json.loads(res_recents.text)
        context = {
            "song_title" : response["item"]["name"],
            "song_artist" : response["item"]["artists"][0]["name"],
            "song_art" : sq.peak(),
            "artist_image" : response2["images"][0]["url"],
            "song_progress" : response["progress_ms"],
            "song_duration" : response["item"]["duration_ms"],
            "song_time_left" : response["item"]["duration_ms"] - response["progress_ms"],
            "recents" : sq.getQueue(),
        }
        return render(request, "player/index.html", context)
    else:
        return HttpResponse("Spotify API returned status"+res_current.status_code)


def callback(request):
    code = request.GET.get("code", None)
    if code!=None:
        spotify_auth=SpotifyAuth(code)
        #cookie
        request.session["token"] = spotify_auth.toJSON()
        #auth = spotify_auth.getAuth()
    
    return HttpResponseRedirect(reverse("index"))

def getAuth(request):
    token = request.session.get("token", None)
    if token==None:
        return None
    t = json.loads(token)
    spotify_auth = SpotifyAuth(access_token=t["access_token"], refresh_token=t["refresh_token"], expirey_time=t["expirey_time"])
    auth = spotify_auth.getAuth()
    request.session["token"] = spotify_auth.toJSON()
    return auth

def skip_next(request):
    res = requests.post("https://api.spotify.com/v1/me/player/next", headers={"Authorization": getAuth(request)})
    #wait so spotify can change song
    time.sleep(0.5)
    return HttpResponseRedirect(reverse("index"))

def skip_previous(request):
    res = requests.post("https://api.spotify.com/v1/me/player/previous", headers={"Authorization": getAuth(request)})
    #wait so spotify can change song
    time.sleep(0.5)
    return HttpResponseRedirect(reverse("index"))

def play_pause(request):
    res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": getAuth(request)})
    if res.status_code==204:
        requests.put("https://api.spotify.com/v1/me/player/play", headers={"Authorization": getAuth(request)})
    elif res.status_code==200:
        #TODO change because spotify does not update immdeiately when song paused
        requests.put("https://api.spotify.com/v1/me/player/pause", headers={"Authorization": getAuth(request)})
    return HttpResponseRedirect(reverse("index"))

def getAlbumCoverLink(request, song_id):
    res = requests.get("https://api.spotify.com/v1/tracks/"+song_id, headers={"Authorization": getAuth(request)})
    response = json.loads(res.text)
    return response["album"]["images"][0]["url"]

def getSongQueue(request):
    sq_json = json.loads(request.session.get("songqueue", None))
    if sq_json==None:
        sq = SongQueue(length=10)
    else:
        sq = SongQueue(length=sq_json["length"],head=sq_json["head"],queue=sq_json["queue"])
    return sq