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
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm

#from project_view.utils import dump_queries

#from django.db.models import Q

# Fixing elements
#-------------------------------------------------------------------------------

class FixingListView(LoginRequiredMixin, ListView):
    model = Fixing

class FixingDetailView(LoginRequiredMixin, View):

    template_name='project_view/fixing_detail.html'

    def get(self, request, pk):

        fix_list = Fix.objects.filter(fixing_id=pk)
        print(fix_list)
        fixing= Fixing.objects.get(id=pk)
        ctx= { 'fixing':fixing, 'fix_list':fix_list }
        return render(request, self.template_name, ctx)
        

class FixingCreateView(LoginRequiredMixin, CreateView):
    
    template_name='project_view/fixing_form.html'
    
    def get(self, request):
                
        form_data = {'name':''}
        form = CreateFixingForm(initial=form_data)
        
        ctx= { 'form':form }
        return render(request, self.template_name, ctx)

    def post(self, request):
        
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreateFixingForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        fixing = form.save(commit=False)
        fixing.owner = self.request.user
        fixing.save()

        return redirect(reverse('project_view:fixing_list'))

class FixingUpdateView(LoginRequiredMixin, UpdateView):
    model = Fixing

    fields = ['name']
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('update get_queryset called')
        #Limit a User to only modifying their own data
        qs = super(FixingUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class FixingDeleteView(LoginRequiredMixin, DeleteView):
    model = Fixing
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(FixingDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

#Fix combination views:
#--------------------------------------------------------

class FixCreateView(LoginRequiredMixin, CreateView):
    
    template_name='project_view/fix_form.html'
    
    def get(self, request, pk_part):
        
        part = Part.objects.get(id=pk_part)
        print(part)
        
        form_data = {'number_of_elements':1, 'part':part}
        form = CreateFixForm(initial=form_data)

        #limit options in dropdown:
        form.fields['part'].queryset = Part.objects.filter(id=pk_part)

        ctx= { 'form':form, 'part':part }
        return render(request, self.template_name, ctx)

    def post(self, request, pk_part):
        part = Part.objects.get(id=pk_part)
        #unused:
        #pk=request.POST['client']
        #print(pk)
        
        form = CreateFixForm(request.POST)
        
        #if not valid render the form again:
        if not form.is_valid():
            form.fields['part'].queryset = Part.objects.filter(id=pk_part)
            ctx = {'form': form, 'part':part}
            return render(request, self.template_name, ctx)

        #add user as owner before saving:
        fix = form.save(commit=False)
        fix.owner = self.request.user
        fix.save()

        return redirect(reverse('project_view:part_detail', args=[part.module.id, pk_part]))

class FixUpdateView(LoginRequiredMixin, UpdateView):
    
    template_name='project_view/fix_form.html'
    
    def get(self, request, pk_part, pk):
        
        part = get_object_or_404(Part, id=pk_part, owner=self.request.user)
        print(part)
        fix = get_object_or_404(Fix, id=pk, owner=self.request.user)
        
        form = CreateFixForm(instance=fix)

        #limit options in dropdown:
        form.fields['part'].queryset = Part.objects.filter(id=pk_part)

        ctx= { 'form':form, 'part':part }
        return render(request, self.template_name, ctx)

    def post(self, request, pk_part, pk):
        part = get_object_or_404(Part, id=pk_part, owner=self.request.user)
        #unused:
        #pk=request.POST['client']
        #print(pk)
        fix = get_object_or_404(Fix, id=pk, owner=self.request.user)
        form = CreateFixForm(request.POST, instance=fix)
        
        #if not valid render the form again:
        if not form.is_valid():
            form.fields['part'].queryset = Part.objects.filter(id=pk_part)
            ctx = {'form': form, 'part':part}
            return render(request, self.template_name, ctx)
        
        fix.save()

        return redirect(reverse('project_view:part_detail', args=[part.module.id, pk_part]))

class FixDeleteView(LoginRequiredMixin, DeleteView):

    template_name='project_view/fix_confirm_delete.html'
    def get (self, request, pk_part, pk):
        fix = get_object_or_404(Fix, id=pk, owner=self.request.user)
        ctx = {'fix': fix}
        return render(request, self.template_name, ctx)

    def post(self, request, pk_part, pk):
        fix = get_object_or_404(Fix, id=pk)
        arg = [fix.part.module.id, fix.part.id]
        
        fix.delete()
        print(arg)
        return redirect(reverse('project_view:part_detail', args=arg))