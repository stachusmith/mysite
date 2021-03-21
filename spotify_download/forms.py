from django import forms
from project_view.models import Client, Project, Module, Part, Fixing, Fix, Topic, Picture, Entry, Participant, Participation, Todo

from django.core.validators import MinLengthValidator
from django.core.files.uploadedfile import InMemoryUploadedFile
from project_view.humanize import naturalsize
from django.core.exceptions import ValidationError
from django.core import validators



class UpadatePlaylistForm(forms.ModelForm):
    playlist_number = forms.CharField(required=True, max_length=200)