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

class ProjectDetailView(View, LoginRequiredMixin):
    model = Project
    
    # By convention:
    template_name = "project_view/project_detail.html"
    def get(self, request, pk, pk_proj) :
        x = Project.objects.get(id=pk_proj)
        module_list = Module.objects.filter(project_id=x)
        client = Client.objects.get(id=pk)
        print(client)
        ctx = {'project' : x, 'module_list' : module_list, 'client': client}
        return render(request, self.template_name, ctx)

class ProjectCreateView(LoginRequiredMixin, View):

    template_name='project_view/project_form.html'
    
    def get(self, request, pk):
        
        #pull defaults in form:
        client = Client.objects.get(id=pk)
        form_data = {'name':'project name', 'client':client}
        form = CreateProjectForm(form_data)
        
        #limit options in dropdown:
        form.fields['client'].queryset = Client.objects.filter(id=pk)

        ctx= { 'form':form }
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
        project = get_object_or_404(self.model, id=pk_proj, owner=self.request.user)
        form = CreateProjectForm(instance=project)
        
        #limit options in dropdown:
        form.fields['client'].queryset = Client.objects.filter(id=pk)
        
        ctx= {'form':form}
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
        ctx = {'project': project}
        return render(request, self.template_name, ctx)
    
#    def get_queryset(self):
#        print('delete get_queryset called')
#        qs = super(ProjectDeleteView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk, pk_proj):
        project = get_object_or_404(Project, id=pk_proj)
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
        
        ctx = {'client': client, 'project': project, 'module' : module, 'part_list' : part_list}
        print(ctx)
        return render(request, self.template_name, ctx)

class ModuleCreateView(LoginRequiredMixin, View):

    template_name='project_view/module_form.html'
    
    def get(self, request, pk_proj):
        
        #pull defaults in form:
        project = Project.objects.get(id=pk_proj)
        form_data = {'name':'module name', 'project':project}
        form = CreateModuleForm(form_data)
        
        #limit options in dropdown:
        form.fields['project'].queryset = Project.objects.filter(id=pk_proj)

        ctx= { 'form':form }
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
        
        return redirect(reverse('project_view:project_detail', args=[module.project_id, module.project.client.id]))


class ModuleUpdateView(LoginRequiredMixin, View):
    
    template_name='project_view/module_form.html'
    model = Module

     
    def get(self, request, pk_proj, pk_modu):
        module = get_object_or_404(self.model, id=pk_modu, owner=self.request.user)
        form = CreateModuleForm(instance=module)
        
        #limit options in dropdown:
        form.fields['project'].queryset = Project.objects.filter(id=pk_proj)
        
        ctx= {'form':form}
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
        return redirect(reverse('project_view:project_detail', args=[module.project_id, module.project.client.id]))


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
        arg = [module.project_id, module.project.client.id]
        
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

        fixing_types = Fix.objects.filter(part_id=pk_part)
        
        context = { 'part' : part, 'module': module, 'project': project, 'fix':fixing_types}
        return render(request, self.template_name, context)

class PartCreateView(LoginRequiredMixin, View):

    template_name='project_view/part_form.html'
    
    def get(self, request, pk_modu):
        
        #pull defaults in form:
        module = Module.objects.get(id=pk_modu)
        form_data = {'name':'part name', 'module':module}
        form = CreatePartForm(form_data)
        
        #limit options in dropdown:
        form.fields['module'].queryset = Module.objects.filter(id=pk_modu)

        ctx= { 'form':form }
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

        return redirect(reverse('project_view:module_detail', args=[part.module_id, part.module.project_id]))

class PartUpdateView(LoginRequiredMixin, View):
    
    template_name='project_view/part_form.html'
    model = Part

     
    def get(self, request, pk_modu, pk_part):
        part = get_object_or_404(self.model, id=pk_part, owner=self.request.user)
        form = CreatePartForm(instance=part)
        
        #limit options in dropdown:
        form.fields['module'].queryset = Module.objects.filter(id=pk_modu)
        
        ctx= {'form':form}
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
        return redirect(reverse('project_view:module_detail', args=[part.module_id, part.module.project_id]))


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
        arg = [part.module_id, part.module.project_id]
        
        part.delete()
        print(arg)
        return redirect(reverse('project_view:module_detail', args=arg))