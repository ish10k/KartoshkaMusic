import requests
import json

auth= "Bearer BQCqY_WV8G4gTmGW9a_OO2BZ8Ths1KvAnIyjoWo3RLbJ1ZsvBlWcP-FLCbB4gsDj7cWxeKe9XTPHKGm-Pi5Zome6o5jY0qSjfNzdj8xmIExFUkB0myan-EuT1NaYNgzUaMsYJaRHFT1eZKS9RsCCeK6TwsdOVeNdqE46oh64089oDlZi2GuUDm9jrX0A6WTY7sBBNFY"
res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": auth})
print("res: ", res)

if res.status_code==200:
    response = json.loads(res.text)
    print("Band: ", response["item"]["artists"][0]["name"])
    print("Song: ", response["item"]["name"])
    print("large art: ", response["item"]["album"]["images"][0]["url"])
    print("small art: ", response["item"]["album"]["images"][2]["url"])
    print("progress: ", response["progress_ms"])
    print("duration: ", response["item"]["duration_ms"])
    print((response["progress_ms"]/response["item"]["duration_ms"])*100, "percent done")

    #18 past songs
    res = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=18", headers={"Authorization": auth})
    response = json.loads(res.text)
elif res.status_code==204:
    print("No song currently playing")
else:
    print("error")
    print("Status code info: https://developer.spotify.com/documentation/web-api/")