from django.conf import settings as django_settings
from django.contrib.auth.models import User

def user(request):
    return {'user': User.objects.all()}

def settings(request):
    return {
        'settings': django_settings,
    }
