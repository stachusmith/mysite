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

from project_view.models import Part, Client, Project, Module, Supplier, Topic, Fixing, Fix, My_part
from project_view.forms import CreateProjectForm, CreateModuleForm, CreatePartForm, CreateFixingForm, CreateFixForm

#from project_view.utils import dump_queries

#from django.db.models import Q

#MyParts--------------------------------------------------------------------------------------

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class MypartView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("mypart",pk)
        part = get_object_or_404(Part, id=pk)
        my_part = My_part(user_id=request.user.id, part_id=part.id)
        try:
            my_part.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class UnmypartView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("unmypart",pk)
        part = get_object_or_404(Part, id=pk)
        try:
            my_part = My_part.objects.get(user_id=request.user.id, part_id=part.id).delete()
        except My_part.DoesNotExist as e:
            pass

        return HttpResponse()



# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError



@method_decorator(csrf_exempt, name='dispatch')
class AddPictureView(LoginRequiredMixin, View):

    def post(self, request, pk_topi) :
        
        
        pic_file = request.FILES['inpFile']
        print('pic_file:',pic_file)
        
        pic_bytearr=pic_file.read()
        print('pic_bytearr:',pic_bytearr)
        
        Picture.objects.create(picture=pic_bytearr, owner = self.request.user, topic_id=pk_topi, content_type=pic_file.content_type, session=1)
        
        return HttpResponse()

#@method_decorator(csrf_exempt, name='dispatch')
class DeletePictureView(LoginRequiredMixin, View):
    
    template_name='project_view/picture_confirm_delete.html'
    def get (self, request, pk_topi, pk_pict):
        picture = get_object_or_404(Picture, pk=pk_pict, owner=self.request.user)
        topic = Topic.objects.get(id=pk_topi)
        print(topic)

        ctx = {'picture': picture, 'topic':topic }
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk_topi, pk_pict):
        picture = get_object_or_404(Picture, pk=pk_pict)
        arg = [picture.topic.part_id, picture.topic_id]
        
        picture.delete()
        print(arg)
        return redirect(reverse('project_view:topic_detail', args=arg))

#stream picture----------------------------------------------------------------------------
def stream_file(request, pk_topi, pk_pict):
    pic = get_object_or_404(Picture, id=pk_pict)

    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response