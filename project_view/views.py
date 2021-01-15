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
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateEntryForm #, CommentForm
from project_view.views_fixing import *
from project_view.views_topics import *
from project_view.views_entries import *
from project_view.views_participants import *
from project_view.views_mypart import *
#from project_view.utils import dump_queries

#from django.db.models import Q

# Clients
#-------------------------------------------------------------------------------

class ClientListView(ListView):
    model = Client

class ClientDetailView(View, LoginRequiredMixin):
    model = Client
    
    # By convention:
    template_name = "project_view/client_detail.html"
    def get(self, request, pk) :
        x = Client.objects.get(id=pk) #pulling the client from db
        project_list = Project.objects.filter(client_id=x) #pulling projects belonging to client from db

        ctx = {'client' : x, 'project_list' : project_list}
        print(ctx)
        return render(request, self.template_name, ctx)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['name']
    success_url=reverse_lazy('project_view:main')

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Client
    fields = ['name']
    success_url=reverse_lazy('project_view:main')
    def get_queryset(self):
        print('update get_queryset called')
        #Limit a User to only modifying their own data
        qs = super(ClientUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url=reverse_lazy('project_view:main')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(DeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

# Projects
#-------------------------------------------------------------------------------

class ProjectDetailView(LoginRequiredMixin, View):
    model = Project
    
    # By convention:
    template_name = "project_view/project_detail.html"
    def get(self, request, pk, pk_proj) :
        x = Project.objects.get(id=pk_proj)
        module_list = Module.objects.filter(project_id=x)
        project_list = Participation.objects.filter(project_id=x)
        client = Client.objects.get(id=pk)
        print(client)
        ctx = {'project' : x, 'module_list' : module_list, 'client': client, 'project_list':project_list}
        return render(request, self.template_name, ctx)

class ProjectCreateView(LoginRequiredMixin, View):

    template_name='project_view/project_form.html'
    
    def get(self, request, pk):
        
        #pull defaults in form:
        client = Client.objects.get(id=pk)
        form_data = {'client':client}
        form = CreateProjectForm(initial=form_data)
        print(form)
        #limit options in dropdown:
        form.fields['client'].queryset = Client.objects.filter(id=pk)
        
        ctx= { 'form':form, 'client':client}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreateProjectForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()

        return redirect(reverse('project_view:client_detail', args=[pk]))

class ProjectUpdateView(LoginRequiredMixin, View):
    
    template_name='project_view/project_form.html'
    model = Project

     
    def get(self, request, pk, pk_proj):
        client = Client.objects.get(id=pk)
        project = get_object_or_404(self.model, id=pk_proj, owner=self.request.user)
        form = CreateProjectForm(instance=project)
        
        #limit options in dropdown:
        form.fields['client'].queryset = Client.objects.filter(id=pk)
        
        ctx= {'form':form, 'client':client }
        return render(request, self.template_name, ctx)

#    for TemplateView:
#    def get_queryset(self):
#        print('update get_queryset called')
#        #Limit a User to only modifying their own data
#        qs = super(ProjectUpdateView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk, pk_proj):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        project = get_object_or_404(self.model, id=pk_proj, owner=self.request.user)
        form = CreateProjectForm(request.POST, instance=project)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        form.save()
        return redirect(reverse('project_view:client_detail', args=[project.client_id]))


class ProjectDeleteView(LoginRequiredMixin, View):
    
    template_name='project_view/project_confirm_delete.html'
    def get (self, request, pk, pk_proj):
        project = get_object_or_404(Project, pk=pk_proj, owner=self.request.user)
        print(project)
        client = project.client_id
        ctx = {'project': project, 'client': client}
        return render(request, self.template_name, ctx)
    
#    def get_queryset(self):
#        print('delete get_queryset called')
#        qs = super(ProjectDeleteView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk, pk_proj):
        project = get_object_or_404(Project, id=pk_proj)
        print(project)
        arg = [project.client_id]
        
        project.delete()
        print(arg)
        return redirect(reverse('project_view:client_detail', args=arg))
# Modules
#-------------------------------------------------------------------------------

class ModuleDetailView(View, LoginRequiredMixin):
    model = Module
    
    # By convention:
    template_name = "project_view/module_detail.html"
    def get(self, request, pk_proj, pk_modu) :
        #print(pk_proj, pk_modu)
        module = Module.objects.get(id=pk_modu)
        print(module)
        
        part_list = Part.objects.filter(module_id=module)
        print(part_list)

        project = Project.objects.get(id=pk_proj)
        print(project)
        
        client_number = project.client_id
        client = Client.objects.get(id=client_number)
        print(client)
        
        all_my_parts = My_part.objects.all()
        my_parts_ids = list()
        for part in all_my_parts:
            my_parts_ids.append(part.part_id)
        print(my_parts_ids)
        ctx = {'client': client, 'project': project, 'module' : module, 'part_list' : part_list, 'my_parts_ids': my_parts_ids }
        print(ctx)
        return render(request, self.template_name, ctx)

class ModuleCreateView(LoginRequiredMixin, View):

    template_name='project_view/module_form.html'
    
    def get(self, request, pk_proj):
        
        #pull defaults in form:
        project = Project.objects.get(id=pk_proj)
        form_data = {'name':'', 'project':project}
        form = CreateModuleForm(initial=form_data)
        
        #limit options in dropdown:
        form.fields['project'].queryset = Project.objects.filter(id=pk_proj)
        
        ctx= { 'form':form, 'project':project }
        return render(request, self.template_name, ctx)

    def post(self, request, pk_proj):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreateModuleForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        module = form.save(commit=False)
        module.owner = self.request.user
        module.save()
        
        return redirect(reverse('project_view:project_detail', args=[module.project.client.id, module.project_id]))


class ModuleUpdateView(LoginRequiredMixin, View):
    
    template_name='project_view/module_form.html'
    model = Module

     
    def get(self, request, pk_proj, pk_modu):
        module = get_object_or_404(self.model, id=pk_modu, owner=self.request.user)
        project = Project.objects.get(id=pk_proj)
        form = CreateModuleForm(instance=module)
        
        #limit options in dropdown:
        form.fields['project'].queryset = Project.objects.filter(id=pk_proj)

        ctx= {'form':form, 'project':project }
        return render(request, self.template_name, ctx)

#    for TemplateView:
#    def get_queryset(self):
#        print('update get_queryset called')
#        #Limit a User to only modifying their own data
#        qs = super(ModuleUpdateView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk_proj, pk_modu):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        module = get_object_or_404(self.model, id=pk_modu, owner=self.request.user)
        form = CreateModuleForm(request.POST, instance=module)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        form.save()
        return redirect(reverse('project_view:project_detail', args=[module.project.client.id, module.project_id]))


class ModuleDeleteView(LoginRequiredMixin, View):
    
    template_name='project_view/module_confirm_delete.html'
    def get (self, request, pk_proj, pk_modu):
        module = get_object_or_404(Module, pk=pk_modu, owner=self.request.user)
        print(module)
        ctx = {'module': module}
        return render(request, self.template_name, ctx)
    
#    def get_queryset(self):
#        print('delete get_queryset called')
#        qs = super(ModuleDeleteView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk_proj, pk_modu):
        module = get_object_or_404(Module, id=pk_modu)
        arg = [module.project.client.id, module.project_id]
        
        module.delete()
        print(arg)
        return redirect(reverse('project_view:project_detail', args=arg))

# Parts
#-------------------------------------------------------------------------------

class PartDetailView(DetailView, LoginRequiredMixin):
    model = Part
    template_name = "project_view/part_detail.html"
    def get(self, request, pk_modu, pk_part) :
        part = Part.objects.get(id=pk_part)
        
        module = Module.objects.get(id=pk_modu)
        
        project_number = part.module.project_id
        project = Project.objects.get(id=project_number)

        fixes = Fix.objects.filter(part_id=part)
        
        new_topics_list = Topic.objects.filter(part_id=part, status_id=1).order_by('-last_modified') #minus make reverse order
        in_process_topics_list = Topic.objects.filter(part_id=part, status_id=2).order_by('-last_modified')
        settled_topics_list = Topic.objects.filter(part_id=part, status_id=3).order_by('-last_modified')
        #print(new_topics_list) 
        #print(in_process_topics_list)
        #print(settled_topics_list)
        
        for topic in new_topics_list:
            topic.pic_list=Picture.objects.filter(topic_id=topic.id).order_by('-id')#[:3]
            topic.entry_list=Entry.objects.filter(topic_id=topic.id).order_by('-date_of_entry')

        for topic in in_process_topics_list:
            topic.pic_list=Picture.objects.filter(topic_id=topic.id).order_by('-id')
            topic.entry_list=Entry.objects.filter(topic_id=topic.id).order_by('-date_of_entry')
            print(topic.entry_list)
        for topic in settled_topics_list:
            topic.pic_list=Picture.objects.filter(topic_id=topic.id).order_by('-id')
            topic.entry_list=Entry.objects.filter(topic_id=topic.id).order_by('-date_of_entry')
        
        context = { 'part' : part, 'module': module, 'project': project, 'fixes':fixes,
                    'new_topics_list': new_topics_list, 'in_process_topics_list':in_process_topics_list,
                    'settled_topics_list':settled_topics_list }
        return render(request, self.template_name, context)

class PartCreateView(LoginRequiredMixin, View):

    template_name='project_view/part_form.html'
    
    def get(self, request, pk_modu):
        
        #pull defaults in form:
        module = Module.objects.get(id=pk_modu)
        form_data = {'name':'', 'description':'', 'module':module, 'thickness':0, 'minimal_draft_angle':0}
        form = CreatePartForm(initial=form_data)
        
        #limit options in dropdown:
        form.fields['module'].queryset = Module.objects.filter(id=pk_modu)

        ctx= { 'form':form, 'module':module }
        return render(request, self.template_name, ctx)

    def post(self, request, pk_modu):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreatePartForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        part = form.save(commit=False)
        part.owner = self.request.user
        part.save()

        return redirect(reverse('project_view:module_detail', args=[part.module.project_id, part.module_id]))

class PartUpdateView(LoginRequiredMixin, View):
    
    template_name='project_view/part_form.html'
    model = Part

     
    def get(self, request, pk_modu, pk_part):
        module = Module.objects.get(id=pk_modu)
        part = get_object_or_404(self.model, id=pk_part, owner=self.request.user)
        form = CreatePartForm(instance=part)
        
        #limit options in dropdown:
        form.fields['module'].queryset = Module.objects.filter(id=pk_modu)
        
        ctx= {'form':form, 'module':module }
        return render(request, self.template_name, ctx)

#    for TemplateView:
#    def get_queryset(self):
#        print('update get_queryset called')
#        #Limit a User to only modifying their own data
#        qs = super(ModuleUpdateView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk_modu, pk_part):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        part = get_object_or_404(self.model, id=pk_part, owner=self.request.user)
        form = CreatePartForm(request.POST, instance=part)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        form.save()
        return redirect(reverse('project_view:module_detail', args=[part.module.project_id, part.module_id]))


class PartDeleteView(LoginRequiredMixin, View):
    
    template_name='project_view/part_confirm_delete.html'
    def get (self, request, pk_modu, pk_part):
        part = get_object_or_404(Part, pk=pk_part, owner=self.request.user)
        print(part)
        ctx = {'part': part}
        return render(request, self.template_name, ctx)
    
#    def get_queryset(self):
#        print('delete get_queryset called')
#        qs = super(ModuleDeleteView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk_modu, pk_part):
        part = get_object_or_404(Part, id=pk_part)
        arg = [part.module.project_id, part.module_id]
        
        part.delete()
        print(arg)
        return redirect(reverse('project_view:module_detail', args=arg))