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

from project_view.models import Part
#from project_view.forms import CreateForm, CommentForm

#from project_view.utils import dump_queries

#from django.db.models import Q

class PartListView(ListView):
    model = Part
    # By convention:
    template_name = "project_view/part_list.html"
    def get(self, request) :
        part_list = Part.objects.all() #pulling objects from db

        ctx = {'part_list' : part_list} # leaving out for now: 'favorites': favorites, 'search': strval}
        return render(request, self.template_name, ctx)

class PartDetailView(DetailView, LoginRequiredMixin):
    model = Part
    template_name = "project_view/part_detail.html"
    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x }
        return render(request, self.template_name, context)