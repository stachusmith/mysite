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