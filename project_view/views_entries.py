#----------------------------------------------------------
#in this file you will find the topic & picture views
#----------------------------------------------------------

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.files.uploadedfile import InMemoryUploadedFile


from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
#from project_view.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, Picture, Entry
from project_view.forms import *

#from project_view.utils import dump_queries

#from django.db.models import Q

class EntryListView(ListView, LoginRequiredMixin):
    model = Entry

class EntryCreateView(CreateView, LoginRequiredMixin):
    
    #get request happens in topic view

    def post(self, request, pk_topi):
        
        print(request.POST)
        entry_form = CreateEntryForm(request.POST)
        topic = get_object_or_404(Topic, id=pk_topi)
        entry= Entry(solution=request.POST['solution'],
                responsible_id=request.POST['responsible'],
                involved_id=request.POST['involved'],
                agreed_with_id=request.POST['agreed_with'],
                deadline=request.POST['deadline'],
                topic_id=pk_topi)
        #form validation happens in topic view
        

        #add user as owner before saving:
        entry.save()

        return redirect(reverse('project_view:topic_update', args=[topic.part.id, topic.id]))

class EntryUpdateView(UpdateView, LoginRequiredMixin):
    model = Fix

    fields = ['name']
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('update get_queryset called')
        #Limit a User to only modifying their own data
        qs = super(FixingUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class EntryDeleteView(DeleteView, LoginRequiredMixin):
    model = Fixing
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(FixingDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)