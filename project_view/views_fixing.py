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

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm #, CommentForm

#from project_view.utils import dump_queries

#from django.db.models import Q

# Fixing elements
#-------------------------------------------------------------------------------

class FixingListView(ListView):
    model = Fixing

class FixingDetailView(DetailView, LoginRequiredMixin):
    model = Fixing
    
class FixingCreateView(CreateView, LoginRequiredMixin):
    model = Fixing
    fields = ['name']
    success_url=reverse_lazy('project_view:fixing_list')

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(FixingCreateView, self).form_valid(form)

class FixingUpdateView(UpdateView, LoginRequiredMixin):
    model = Fixing
    fields = ['name']
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('update get_queryset called')
        #Limit a User to only modifying their own data
        qs = super(FixingUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class FixingDeleteView(DeleteView, LoginRequiredMixin):
    model = Fixing
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(FixingDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)