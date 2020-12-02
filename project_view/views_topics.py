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
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm, CreateTopicForm, UpdateTopicForm

#from project_view.utils import dump_queries

#from django.db.models import Q

# Fixing elements
#-------------------------------------------------------------------------------



class TopicDetailView(View, LoginRequiredMixin):
    model = Topic
    template_name = 'project_view/topic_detail.html'
    def get(self, request, pk_part, pk_topi) :
        topic = self.model.objects.get(id=pk_topi)
        part = topic.part.id
        module = topic.part.module_id
        context = { 'part' : part, 'module': module}
        return render(request, self.template_name, context)

class TopicCreateView(View, LoginRequiredMixin):

    template_name='project_view/topic_form.html'
    
    def get(self, request, pk_part):
        part = Part.objects.get(id=pk_part)
        
        form_data = { 'part':part }
        form = CreateTopicForm(initial=form_data)
        
        #limit options in dropdown:
        form.fields['part'].queryset = Part.objects.filter(id=pk_part)
        ctx= { 'form':form }
        return render(request, self.template_name, ctx)
        
    def post(self, request, pk_part):
        form = CreateTopicForm(request.POST, request.FILES or None)
        pk_topic=request.POST['title']
        print(pk_topic)
        #part = Part.objects.get(id=pk_part)
        if not form.is_valid():
            ctx = {'form': form }
            return render(request, self.template_name, ctx)
        topic = form.save(commit=False)
        topic.owner = self.request.user
        topic.save()
        pk_topi=topic.id
        return redirect(reverse('project_view:topic_update', args=[pk_part, pk_topi]))

class TopicUpdateView(UpdateView, LoginRequiredMixin):
    template_name='project_view/update_topic_form.html'
        
    def post(self, request, pk_part):
        form = UpdateTopicForm(request.POST, request.FILES or None)
        print(request.POST)
        #part = Part.objects.get(id=pk_part)
        if not form.is_valid():
            ctx = {'form': form }
            return render(request, self.template_name, ctx)

        return redirect('project_view:main')


class TopicDeleteView(DeleteView, LoginRequiredMixin):
    model = Fixing
    success_url=reverse_lazy('project_view:fixing_list')
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(FixingDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddPictureView(LoginRequiredMixin, View):
    def get(self, request, pk_topi):
        topic = Topic.objects.filter(id=pk_topi)
        print(topic)
        ctx= { 'topic':topic }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk_topi) :
        print("Add PK",pk_topi)
        t = get_object_or_404(Topic, id=pk_topi)
        picture = topic(user=request.user, picture=t)
        
        pic = form.save(commit=False)
        pic.owner = self.request.user
        try:
            pic.save()  # In case of duplicate key
        except IntegrityError as e:
            pass # pass is like continue
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeletePictureView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Thing, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, thing=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


