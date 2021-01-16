from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('callback', views.callback, name="callback"),
    path('skip_next', views.skip_next, name="skip_next"),
    path('skip_previous', views.skip_previous, name="skip_previous"),
    path('play_pause', views.play_pause, name="play_pause"),
]