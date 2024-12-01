import datetime
import json

import requests
from decouple import config
import base64


class SpotifyAuth():
    access_token = None
    refresh_token = None
    expiry_time=None

    code = None
    auth = None

    def __init__(self, code=None, access_token=None, refresh_token=None, expiry_time=None):
        #if allows us to have two different constructors
        if code!=None:
            #print("code constructor")
            self.code = code
            self.access_token=None
            self.refresh_token=None
            self.expiry_time=None
            self.auth=None
            self.getAccessToken()
        elif access_token!=None and refresh_token!=None and expiry_time!=None:
            #print("token constructor")
            self.access_token=access_token
            self.refresh_token=refresh_token
            self.expiry_time=self.stringToDateTime(expiry_time)

    def stringToDateTime(self, string):
        # time = "2020-06-05 16:30:34.392897"
        return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')
    
    def getAuth(self):
        accessToken=self.getAccessToken()
        return "Bearer " + accessToken

    def getAccessToken(self):
        now = datetime.datetime.now()

        # early circuit breaker
        if self.expiry_time is not None and self.expiry_time > now:
            print("token still valid, expires", self.expiry_time)
            return self.access_token

        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{config('SPOTIFY_CLIENT_ID')}:{config('SPOTIFY_CLIENT_SECRET')}".encode()).decode("utf-8"),
            "content-type": "application/x-www-form-urlencoded"
        }
        payload = {
            "code":self.code,
            "redirect_uri":config('SPOTIFY_REDIRECT_URI'),
        }

        # No expiry time means no token, so we need to fetch a new one.
        # If we have an expiry time and reached this point, it means the token must be expired
        # and we need to get a new one!
        if self.expiry_time is None:
            print("token not yet set")
            payload["grant_type"] = "authorization_code"
        else:
            print("token expired, time to get a new one")
            payload["grant_type"] = "refresh_token"

        response = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)

        if response.status_code >= 400:
            raise Exception("Could not obtain new token, response", response.text) 

        resJson = response.json()
        print("obtained new token, response", resJson)
        self.expiry_time=self.calculateExpiryTime(resJson["expires_in"])
        self.refresh_token = resJson["refresh_token"]
        self.access_token = resJson["access_token"]
            
        return self.access_token

    def getRefreshToken(self):
        return self.refresh_token
        
    def getexpiryTime(self):
        return self.expiry_time

    def toJSON(self):
        d = {
            "access_token" : self.access_token,
            "refresh_token" : self.refresh_token,
            "expiry_time": str(self.expiry_time),
        }
        return json.dumps(d)
        #expiry_time is a datetime object so must be serialized...

    def calculateExpiryTime(self, secondsUntilexpiry):
        now = datetime.datetime.now()
        expiryTime = now + datetime.timedelta(seconds=secondsUntilexpiry)
        return expiryTime