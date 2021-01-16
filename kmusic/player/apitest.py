import requests
import json

auth= "Bearer BQBToLRR6omuWYmAnSYXUR8c4skC9k3oKkdhKdJVQ6dBOyOe-RlSdu0TJKziKlYjxYTdjA4dtOWKrVFZX-vtkVVDwnzjsB6A1fL2bgMSUz7wx0xdO9Dr3HhG6fTYkNcYzAjZK4EIw8KtS0pTW99E_FD_dQAh7pr-7jth"
res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": auth})
print("res: ", res)

if res.status_code==200:
    response = json.loads(res.text)
    print("Band: ", response["item"]["artists"][0]["name"])
    print("Song: ", response["item"]["name"])
    print("large art: ", response["item"]["album"]["images"][0]["url"])
    print("small art: ", response["item"]["album"]["images"][2]["url"])

    #18 past songs
    res = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=18", headers={"Authorization": auth})
    response = json.loads(res.text)
elif res.status_code==204:
    print("No song currently playing")
else:
    print("error")
    print("Status code info: https://developer.spotify.com/documentation/web-api/")