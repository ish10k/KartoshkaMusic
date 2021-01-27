from django.shortcuts import render, reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

import requests
import json
import time
from decouple import config

from .SpotifyAuth import SpotifyAuth
from .SongQueue import SongQueue
# Create your views here.

def index(request):
    if getAuth(request)==None:
        context={
            "loggedOut" : True,
            "login_link":"https://accounts.spotify.com/en/authorize?client_id=325f8457b0444db0919e8bc14e63ed9f&response_type=code&redirect_uri="+config('REDIRECT_URI')+"&scope=user-modify-playback-state user-read-playback-state user-read-recently-played user-read-currently-playing&show_dialog=true"
        }
        return render(request, "player/index.html", context)
    res_current = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": getAuth(request)})
    if res_current.status_code==204:
        return render(request, "player/index.html", context={"song_title": "No song playing"})
    elif res_current.status_code==200:
        context = getCurrentSongInfo(request)
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
    return HttpResponse(json.dumps(res.status_code))

def skip_previous(request):
    res = requests.post("https://api.spotify.com/v1/me/player/previous", headers={"Authorization": getAuth(request)})
    return HttpResponse(json.dumps(res.status_code))

def play(request):
    res = requests.put("https://api.spotify.com/v1/me/player/play", headers={"Authorization": getAuth(request)})
    return HttpResponse(json.dumps(res.status_code))

def pause(request):
    res = requests.put("https://api.spotify.com/v1/me/player/pause", headers={"Authorization": getAuth(request)})
    return HttpResponse(json.dumps(res.status_code))

def getAlbumCoverLink(request, song_id):
    res = requests.get("https://api.spotify.com/v1/tracks/"+song_id, headers={"Authorization": getAuth(request)})
    response = json.loads(res.text)
    return response["album"]["images"][0]["url"]

def getSongQueue(request):
    sq_cookie = request.session.get("songqueue", None)
    if sq_cookie==None:
        sq = SongQueue(length=19)
    else:
        sq_json = json.loads(sq_cookie)
        sq = SongQueue(length=sq_json["length"],head=sq_json["head"],queue=sq_json["queue"])
    return sq

def isSongPaused(request):
    time.sleep(0.5)
    res1 = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": getAuth(request)})
    if res1.status_code==204:
        #no song playing / spotify closed
        return True
    response = json.loads(res1.text)
    before = response["progress_ms"]
    #wait so song can progress and spotify update
    time.sleep(0.5)
    res2 = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": getAuth(request)})
    response2 = json.loads(res2.text)
    after = response2["progress_ms"]
    if after-before > 0:
        return False
    else:
        return True

def getCurrentSongInfo_HTTP_RES(request):
    return HttpResponse(json.dumps(getCurrentSongInfo(request)))

def getCurrentSongID(request):
    res_current = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": getAuth(request)})
    response = json.loads(res_current.text)
    data = {
        "song_id" : response["item"]["id"],
        "song_progress" : response["progress_ms"],
    }
    return HttpResponse(json.dumps(data))

def getCurrentSongInfo(request):
    isPaused = isSongPaused(request)
    res_current = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": getAuth(request)})
    response = json.loads(res_current.text)

    sq = getSongQueue(request)
    sq.addItem(response["item"]["album"]["images"][0]["url"])
    request.session["songqueue"] = sq.toJSON()
    artist_id = response["item"]["artists"][0]["id"]
    res2 = requests.get("https://api.spotify.com/v1/artists/"+artist_id, headers={"Authorization":  getAuth(request)})
    response2 = json.loads(res2.text)
    data = {
        "song_id" : response["item"]["id"],
        "song_title" : response["item"]["name"],
        "song_artist" : response["item"]["artists"][0]["name"],
        "song_art" : sq.peak(),
        "artist_image" : response2["images"][0]["url"],
        "song_progress" : response["progress_ms"],
        "song_duration" : response["item"]["duration_ms"],
        "song_time_left" : response["item"]["duration_ms"] - response["progress_ms"] + 1000,
        "recents" : sq.getTail(),
        "isPaused": isPaused,
    }
    return data 