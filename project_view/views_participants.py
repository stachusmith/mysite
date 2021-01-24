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

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, Picture, Entry, Participant, Participation
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm, CreateTopicForm, CreateParticipantForm, CreateParticipationForm

#from project_view.utils import dump_queries

#from django.db.models import Q

class ParticipantCreateView(LoginRequiredMixin, CreateView):
    
    template_name='project_view/participant_form.html'
    
    def get(self, request):
        
        form_data = {'name':''}
        form = CreateParticipantForm(initial=form_data)

        #limit options in dropdown:
        #form.fields['project'].queryset = Project.objects.filter(id=pk_proj)

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request):
        
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

        return redirect(reverse('project_view:participation_list'))

class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    
    template_name='project_view/participant_form_update.html'
    
    def get(self, request, pk):
        
        participant=get_object_or_404(Participant, owner=self.request.user, id=pk)
        form = CreateParticipantForm(instance=participant)

        #limit options in dropdown:
        #form.fields['project'].queryset = Project.objects.filter(id=pk_proj)

        ctx= { 'form':form, 'participant':participant }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        
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

        return redirect(reverse('project_view:participation_list'))

class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = Participant
    success_url=reverse_lazy('project_view:participation_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(ParticipantDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class ParticipationListView(LoginRequiredMixin, ListView):
    template_name='project_view/participation_list.html'
    def get(self, request):
        
        participant_list=Participant.objects.all()
        
        project_collection=dict()
        for participant in participant_list:
            participant_info=list()
            #pulling each participant's projects:
            project_query=Participation.objects.filter(participant_id=participant.id)
            project_list=list()
            for item in project_query:
                #extracting projects from query list:
                project_list.append(item)
            project_collection[participant]=project_list
        print(project_collection)

        ctx= { 'project_collection':project_collection }
        return render(request, self.template_name, ctx)

class ParticipationCreateView(LoginRequiredMixin, CreateView):
    
    template_name='project_view/participation_form.html'
    
    def get(self, request, pk):
        
        #for link from projects
        form_data = {'participant':pk}
        participant=Participant.objects.get(id=pk)
        form = CreateParticipationForm(initial=form_data)

        #limit options in dropdown:
        form.fields['participant'].queryset = Participant.objects.filter(id=pk)

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
              
        form = CreateParticipationForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        Participation = form.save(commit=False)
        Participation.owner = self.request.user
        Participation.save()

        return redirect(reverse('project_view:participation_list'))

class ParticipationUpdateView(LoginRequiredMixin, UpdateView):
    
    template_name='project_view/participation_form.html'
    
    def get(self, request, pk):
        
        
        participation=get_object_or_404(Participation, owner=self.request.user, id=pk)
        form = CreateParticipationForm(instance=participation)

        #limit options in dropdown:
        #form.fields['part'].queryset = Part.objects.filter(id=pk_part)

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request):
              
        form = CreateParticipationForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        Participation = form.save(commit=False)
        Participation.owner = self.request.user
        Participation.save()

        return redirect(reverse('project_view:participant_list'))

class ParticipationDeleteView(LoginRequiredMixin, DeleteView):
    model = Participation
    success_url=reverse_lazy('project_view:participation_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(ParticipationDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)