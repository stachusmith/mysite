from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime


from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
#from project_view.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, My_part
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm

#from project_view.utils import dump_queries

#from django.db.models import Q

#MyParts--------------------------------------------------------------------------------------

 

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator
#from django.db.utils import IntegrityError

#@method_decorator(csrf_exempt, name='dispatch')
#2021-03-05 CSRF Present
class MypartView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("mypart",pk)
        part = get_object_or_404(Part, id=pk)
        my_part = My_part(user_id=request.user.id, part_id=part.id)
        try:
            my_part.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

#@method_decorator(csrf_exempt, name='dispatch')
#2021-03-05 CSRF Present
class UnmypartView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("unmypart",pk)
        part = get_object_or_404(Part, id=pk)
        try:
            my_part = My_part.objects.get(user_id=request.user.id, part_id=part.id).delete()
        except My_part.DoesNotExist as e:
            pass

        return HttpResponse()