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

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, Picture, Entry, Participant, Participation, Development_provider, Job_title
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm, CreateTopicForm, CreateParticipantForm, CreateParticipationForm, CreateParticipantForm2, CreateParticipantForm2POST

#from project_view.utils import dump_queries

#from django.db.models import Q

class ParticipantCreateView(LoginRequiredMixin, CreateView):
    
    template_name='project_view/participant_form.html'
    
    def get(self, request):
        
        
        form = CreateParticipantForm()
        
        #limit options in dropdown:
        #works_for_choices = ['OEM', 'Supplier', 'Development service']
        #form.fields['works_for'].choices = works_for_choices
        #print(form)
        #form.fields['project'].queryset = Project.objects.filter(id=pk_proj)

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreateParticipantForm(request.POST)

        
        #if not valid render the form again:
        print(request.POST['works_for'])
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        participant = form.save(commit=False)
        participant.owner = self.request.user
        participant.save()
        pk = participant.id
        arg = [pk, request.POST['works_for']]
        return redirect(reverse('project_view:participant_create2', args=arg))

class ParticipantCreate2View(LoginRequiredMixin, UpdateView):
    model= Participant
    template_name='project_view/participant_form2.html'
    
    def get(self, request, pk, pk_for):
        
        participant=get_object_or_404(self.model, owner=self.request.user, id=pk)
        form = CreateParticipantForm2(pk_for, instance=participant)
        #form takes only pk_for and args, kwargs - so if it's an update, it'll also take instance
        
        

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk, pk_for):
        

        participant=get_object_or_404(self.model, owner=self.request.user, id=pk)
        form = CreateParticipantForm2POST(request.POST, instance=participant)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        projects = request.POST.getlist('project')
        for project in projects:
            try:
                participation = Participation.objects.get(project_id=project, owner=self.request.user, participant_id=pk)
            except:
                participation = Participation.objects.create(project_id=project, owner=self.request.user, participant_id=pk)
        
        form.save()

        return redirect(reverse('project_view:participation_list'))

class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    
    template_name='project_view/participant_form_update.html'
    
    def get(self, request, pk):
        
        participant=get_object_or_404(Participant, owner=self.request.user, id=pk)
        
        if participant.client:
            initial_choice = {'works_for': '1' }
        elif participant.supplier:
            initial_choice = {'works_for': '2' }
        elif participant.development_provider:
            initial_choice = {'works_for': '3' }#f'{participant.development_provider}'}
        else:
            initial_choice = {'works_for': '1' }

        form = CreateParticipantForm(initial=initial_choice, instance=participant)
        print(participant.development_provider)

        ctx= { 'form':form, 'participant':participant }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        
        participant=get_object_or_404(Participant, owner=self.request.user, id=pk)
        form = CreateParticipantForm(request.POST, instance=participant)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form, 'participant':participant}
            return render(request, self.template_name, ctx)
        
        form.save()
        arg = [pk, request.POST['works_for']]
        return redirect(reverse('project_view:participant_create2', args=arg))

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

        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        participation=get_object_or_404(Participation, owner=self.request.user, id=pk)
        form = CreateParticipationForm(request.POST, instance=participation)
        print(form)
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        form.save()
        

        return redirect(reverse('project_view:participant_list'))

class ParticipationDeleteView(LoginRequiredMixin, DeleteView):
    model = Participation
    success_url=reverse_lazy('project_view:participation_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(ParticipationDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class ParticipationPrjCreateView(LoginRequiredMixin, CreateView):
    
    template_name='project_view/participation_form.html'
    
    def get(self, request, pk_proj):
        project = Project.objects.get(id = pk_proj)
        #for link from projects
        form_data = {'project':pk_proj}
        
        form = CreateParticipationForm(initial=form_data)

        #limit options in dropdown:
        form.fields['project'].queryset = Project.objects.filter(id=pk_proj)
        
        ctx= { 'form':form, 'project':project }
        return render(request, self.template_name, ctx)

    def post(self, request, pk_proj):
              
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