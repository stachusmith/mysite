# Register your models here.
from django.contrib import admin

# Register your models here.
from project_view.models import Part
admin.site.register(Part)

from project_view.models import Project
admin.site.register(Project)

from project_view.models import Module
admin.site.register(Module)

from project_view.models import Client
admin.site.register(Client)

from project_view.models import Supplier
admin.site.register(Supplier)

from project_view.models import Topic
admin.site.register(Topic)

from project_view.models import Fixing
admin.site.register(Fixing)

from project_view.models import Fix
admin.site.register(Fix)

from project_view.models import Status
admin.site.register(Status)

from project_view.models import Participant
admin.site.register(Participant)

from project_view.models import Development_provider
admin.site.register(Development_provider)

from project_view.models import Job_title
admin.site.register(Job_title)

from project_view.models import Entry
admin.site.register(Entry)