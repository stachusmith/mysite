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

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry

class EntryCreateView(LoginRequiredMixin, CreateView):
    
    #get request happens in topic view

    def post(self, request, pk_topi):
        
        print(request.POST)
        entry_form = CreateEntryForm(request.POST)
        topic = get_object_or_404(Topic, id=pk_topi)
        print(entry_form)
        if not entry_form.is_valid():
            ctx = {'entry_form': entry_form}
            return render(request, self.template_name, ctx)

        entry = entry_form.save(commit=False)
        entry.owner = self.request.user
        entry.topic_id = pk_topi
        entry.save()
        #saves many2many table
        entry_form.save_m2m()
        return redirect(reverse('project_view:topic_update', args=[topic.part.id, topic.id]))

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    
    #get request happens in topic view

    def post(self, request, pk):
        
        print(request.POST)
        entry = get_object_or_404(Entry, owner=self.request.user, id=pk)
        print(entry.deadline)
        entry_form = CreateEntryForm(request.POST, instance=entry)
        print(entry_form)
        if not entry_form.is_valid():
            ctx = {'entry_form': entry_form}
            return render(request, self.template_name, ctx)
        

        
        entry_form.save()
#        entry_form.save_m2m()

        return redirect(reverse('project_view:topic_update', args=[entry.topic.part.id, entry.topic.id]))

class EntryDeleteView(LoginRequiredMixin, DeleteView):

    template_name='project_view/entry_confirm_delete.html'
    def get (self, request, pk):
        entry = get_object_or_404(Entry, id=pk, owner=self.request.user)
        ctx = {'entry': entry }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        entry = get_object_or_404(Entry, id=pk)
        
        entry.delete()
        return redirect(reverse('project_view:topic_update', args=[entry.topic.part.id, entry.topic.id]))