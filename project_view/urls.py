from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'project_view'

urlpatterns = [
    
    path('clients', views.ClientListView.as_view(), name='clients'),
    path('client/create', views.ClientCreateView.as_view(), name='client_create'),
    path('client/update', views.ClientUpdateView.as_view(), name='client_update'),
    path('client/delete', views.ClientDeleteView.as_view(), name='client_delete'),
    path('client/<int:pk>', views.ClientDetailView.as_view(), name='client_detail'), 
    
    
    #path('project/create', views.ProjectCreateView.as_view(), name='project_create'),
    #path('project/update', views.ProjectUpdateView.as_view(), name='project_update'),
    #path('project/delete', views.ProjectDeleteView.as_view(success_url=reverse_lazy('project_view:clients')), name='project_delete'),

    #path('modules', views.ModuleListView.as_view(), name='modules'),
    #path('module/create', views.ModuleCreateView.as_view(), name='module_create'),
    #path('module/update', views.ModuleUpdateView.as_view(), name='module_update'),
    #path('module/delete', views.ModuleDeleteView.as_view(success_url=reverse_lazy('module_view:clients')), name='module_delete'),

    path('', views.PartListView.as_view(), name='main'),
    path('part/<int:pk>', views.PartDetailView.as_view(), name='part_detail'),
    path('part/create', views.PartCreateView.as_view(), name='part_create'),
    path('part/<int:pk>/update', views.PartUpdateView.as_view(), name='part_update'),
    path('part/<int:pk>/delete', views.PartDeleteView.as_view(success_url=reverse_lazy('project_view:main')), name='part_delete'),
]
    
    
    
    
#References:
#    path('ad/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
#    path('ad/create', views.AdCreateView.as_view(), name='ad_create'),
#    path('ad/<int:pk>/update', views.AdUpdateView.as_view(), name='ad_update'),
#    path('ad/<int:pk>/delete', views.AdDeleteView.as_view(success_url=reverse_lazy('ads:main')), name='ad_delete'),
#    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
#    path('ad/<int:pk>/comment', views.CommentCreateView.as_view(), name='ad_comment_create'),
#    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='ad_comment_delete'),
#    path('ad/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='ad_favorite'),
#    path('ad/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='ad_unfavorite'),