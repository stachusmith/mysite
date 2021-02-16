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
from django.core.mail import send_mail

from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
#from project_view.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, Picture, Entry, Participation, Participant, Responsibility, Todo
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm, CreateTopicForm, UpdateTopicForm, CreateEntryForm, CreateTodoForm

#from project_view.utils import dump_queries

#from django.db.models import Q

class TodoCreateView(LoginRequiredMixin, View):

    template_name='project_view/todo_form.html'
    
    def get(self, request) :
        todo_list = Todo.objects.filter(owner = self.request.user)

        
        priority_list = Todo.objects.filter(owner = self.request.user, status_id=1).order_by('-deadline') #minus make reverse order
        in_process_list = Todo.objects.filter(owner = self.request.user, status_id=2).order_by('-deadline')
        settled_list = Todo.objects.filter(owner = self.request.user, status_id=3).order_by('-deadline')
        
        form = CreateTodoForm()
        update = 0
        context = { 'form':form, 'priority_list': priority_list, 'in_process_list':in_process_list,
                    'settled_list':settled_list }
        return render(request, self.template_name, context)
        
    def post(self, request):

        form = CreateTodoForm(request.POST)
        
        if not form.is_valid():
            ctx = {'form': form }
            return render(request, self.template_name, ctx)
        todo = form.save(commit=False)
        todo.owner = self.request.user
        todo.save()
        #send notification:
        message_name = 'you have a new task in your project'
        message = request.POST['description']
        from_email = 'projectviewapp@gmail.com'
        to_email = [todo.app_user.email]
        send_mail (
            message_name, #title
            message, #message
            from_email,
            to_email,
            fail_silently=False 
        )
        print(todo.id)
        return redirect(reverse('project_view:todo_create'))

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    template_name='project_view/todo_form.html'
    
    def get(self, request, pk):
        todo_list = Todo.objects.filter(owner = self.request.user)
        todo = get_object_or_404(Todo, owner = self.request.user, id = pk)
        
        priority_list = Todo.objects.filter(owner = request.user, status_id=1).order_by('-deadline') #minus makes reverse order
        in_process_list = Todo.objects.filter(owner = request.user, status_id=2).order_by('-deadline')
        settled_list = Todo.objects.filter(owner = request.user, status_id=3).order_by('-deadline')
        
        form = CreateTodoForm(instance=todo)
        update = 1
        context = { 'form':form, 'priority_list': priority_list, 'in_process_list':in_process_list,
                    'settled_list':settled_list, 'update': update }
        return render(request, self.template_name, context)
        
    def post(self, request):
        todo = get_object_or_404(Todo, owner = self.request.user, id = pk)

        form = CreateTodoForm(request.POST, instance=todo)
        
        if not form.is_valid():
            ctx = {'form': form }
            return render(request, self.template_name, ctx)
        todo = form.save(commit=False)
        todo.owner = self.request.user
        todo.save()
        
        return redirect(reverse('project_view:todo_create'))

class TodoDeleteView(LoginRequiredMixin, View):
    
    template_name='project_view/todo_confirm_delete.html'
    def get (self, request, pk):
        todo = get_object_or_404(Todo, id = pk, owner=self.request.user)

        ctx = {'todo': todo}
        return render(request, self.template_name, ctx)
    
#    def get_queryset(self):
#        print('delete get_queryset called')
#        qs = super(ModuleDeleteView, self).get_queryset()
#        return qs.filter(owner=self.request.user)

    def post(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        
        todo.delete()
        return redirect(reverse('project_view:todo_create'))