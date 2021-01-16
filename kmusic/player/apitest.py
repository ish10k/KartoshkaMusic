import requests
import json

auth= "Bearer BQDbQtiPq9GU74qfYR7nSP-TJ_DjXx5IOMlUlWy-OyUoPji1TINer4EKO3G-jAKHnZ4s1Im24eMJkSBD0eJT55KTVXZ05eJjP1J9IGSbIaeUhx7lSRhTAVAkxO2l-srWV4WubVLHSNN5Hk_jEhNmY-t9SeSdenqgxz8CiUGWi8xNwUPUo31mMwVd5QSg395DQt9Ahd8"
res = requests.get("https://api.spotify.com/v1/me/player", headers={"Authorization": auth})
response = json.loads(res.text)

print("Band: ", response["item"]["artists"][0]["name"])
print("Song: ", response["item"]["name"])
print("large art: ", response["item"]["album"]["images"][0]["url"])
print("small art: ", response["item"]["album"]["images"][2]["url"])

#18 past songs
res = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=18", headers={"Authorization": auth})
response = json.loads(res.text)