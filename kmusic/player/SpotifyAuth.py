import datetime
import json

import requests
from decouple import config


class SpotifyAuth():
    access_token = None
    refresh_token = None
    expirey_time=None

    code = None
    auth = None

    def __init__(self, code=None, access_token=None, refresh_token=None, expirey_time=None):
        #if allows us to have two different constructors
        if code!=None:
            #print("code constructor")
            self.code = code
            self.getAccessToken()
        elif access_token!=None and refresh_token!=None and expirey_time!=None:
            #print("token constructor")
            self.access_token=access_token
            self.refresh_token=refresh_token
            self.expirey_time=self.stringToDateTime(expirey_time)

    def stringToDateTime(self, string):
        # time = "2020-06-05 16:30:34.392897"
        return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')
    
    def getAuth(self):
        accessToken=self.getAccessToken()
        return "Bearer " + accessToken

    def getAccessToken(self):
        # if expirey time not set, we assume the token has already expired
        now = datetime.datetime.now()
        #print("self.expirey_time", self.expirey_time)
        if self.expirey_time==None:
            #print("token not yet set")
            data = {
                "client_id": config('SPOTIFY_CID'),
                #should be hidden
                "client_secret": config('SPOTIFY_CS'),
                "grant_type":"authorization_code",
                "code":self.code,
                "redirect_uri":config('REDIRECT_URI'),
            }
            tokenRes = requests.post("https://accounts.spotify.com/api/token", data = data)
            response = json.loads(tokenRes.text)
            #print("response ",response)
            #print("exires in: ",response["expires_in"])
            self.expirey_time=self.calculateExpireyTime(response["expires_in"])
            self.refresh_token = response["refresh_token"]
            self.access_token = response["access_token"]
            return self.access_token
        elif self.expirey_time<=now:
            #print("token expired, time to get a new one")
            data = {
                "grant_type":"refresh_token",
                "refresh_token":self.refresh_token,
                "client_id": config('SPOTIFY_CID'),
                #should be hidden
                "client_secret": config('SPOTIFY_CS'),
                "redirect_uri": config('REDIRECT_URI'),
            }
            tokenRes = requests.post("https://accounts.spotify.com/api/token", data = data)
            response = json.loads(tokenRes.text)
            self.expirey_time=self.calculateExpireyTime(response["expires_in"])
            self.access_token = response["access_token"]
            return self.access_token
        else:
           #print("token still valid")
            #print(self.expirey_time)
            return self.access_token

    def getRefreshToken(self):
        return self.refresh_token
        
    def getExpireyTime(self):
        return self.expirey_time

    def toJSON(self):
        d = {
            "access_token" : self.access_token,
            "refresh_token" : self.refresh_token,
            "expirey_time": str(self.expirey_time),
        }
        return json.dumps(d)
        #expirey_time is a datetime object so must be serialized...

    def calculateExpireyTime(self, secondsUntilExpirey):
        now = datetime.datetime.now()
        expireyTime = now + datetime.timedelta(seconds=secondsUntilExpirey)
        return expireyTime