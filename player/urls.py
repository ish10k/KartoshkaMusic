from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('callback', views.callback, name="callback"),
    path('skip_next', views.skip_next, name="skip_next"),
    path('skip_previous', views.skip_previous, name="skip_previous"),
    path('play', views.play, name="play"),
    path('pause', views.pause, name="pause"),
    path('getCurrentSongInfo_HTTP_RES', views.getCurrentSongInfo_HTTP_RES, name="getCurrentSongInfo_HTTP_RES"),
    path('getCurrentSongID', views.getCurrentSongID, name="getCurrentSongID"),
    path('like_song/<str:song_id>', views.like_song, name="like_song"),
]