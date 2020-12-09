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

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, Picture, Entry, Participant
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm, CreateTopicForm, UpdateTopicForm, CreateParticipantForm

#from project_view.utils import dump_queries

#from django.db.models import Q

class ParticipantListView(ListView):
    model = Participant

class ParticipantCreateView(CreateView, LoginRequiredMixin):
    
    template_name='project_view/participant_form.html'
    
    def get(self, request, pk_proj):
        
        project = Project.objects.get(id=pk_proj)
        print(project)
        
        form_data = {'name':'', 'project':project}
        form = CreateParticipantForm(initial=form_data)

        #limit options in dropdown:
        form.fields['project'].queryset = Project.objects.filter(id=pk_proj)

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk_proj):
        project = Project.objects.get(id=pk_proj)
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreateParticipantForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        Participant = form.save(commit=False)
        Participant.owner = self.request.user
        Participant.save()

        return redirect(reverse('project_view:project_detail', args=[project.client_id, project.id]))

class ParticipantUpdateView(UpdateView, LoginRequiredMixin):
    
    # not ready, needs to be changed similar to fixcreate
    
    model = Fix

    #fields = ['name']
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('update get_queryset called')
        #Limit a User to only modifying their own data
        qs = super(FixingUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class ParticipantDeleteView(DeleteView, LoginRequiredMixin):
    model = Fix
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(FixingDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)