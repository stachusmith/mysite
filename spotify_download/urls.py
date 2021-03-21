from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'spotify_download'

urlpatterns = [
    
    path('auth', views.AuthView.as_view(), name='auth'),
#    path('', views.UpdatePlaylistView.as_view(), name='playlist_input'),
#    path('get_creds', views.GetCredsView.as_view(), name='get_creds'), 
#    path('playlist', views.PrintPlaylistView.as_view(), name='playlist_print'), 
]