from django.shortcuts import render, reverse

from django.http import HttpResponse, HttpResponseRedirect

import requests
import json
import time

from .SpotifyAuth import SpotifyAuth
# Create your views here.

def index(request):
    auth = getAuth(request)
    if auth==None:
        return render(request, "player/index.html")
    
    res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": auth})
    if res.status_code==204:
        return render(request, "player/index.html", context={"song_title": "No song playing"})
    elif res.status_code==200:
        response = json.loads(res.text)
        artist_id = response["item"]["artists"][0]["id"]
        res2 = requests.get("https://api.spotify.com/v1/artists/"+artist_id, headers={"Authorization":  auth})
        response2 = json.loads(res2.text)
        print("response2: ", response2)
        context = {
            "song_title" : response["item"]["name"],
            "song_artist" : response["item"]["artists"][0]["name"],
            "song_art" : response["item"]["album"]["images"][0]["url"],
            "artist_image" : response2["images"][0]["url"],
            "song_progress" : response["progress_ms"],
            "song_duration" : response["item"]["duration_ms"],
            "song_time_left" : response["item"]["duration_ms"] - response["progress_ms"],
        }
        return render(request, "player/index.html", context)
    else:
        return HttpResponse("Spotify API returned status"+res.status_code)


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
    print("\n\nTOKEN: ", token)
    if token==None:
        return None
    t = json.loads(token)
    print("\n\nTOKEN: ", t)
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