from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='main'),   
]