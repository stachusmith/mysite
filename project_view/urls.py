from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'project_view'

urlpatterns = [
    
    path('', views.ClientListView.as_view(), name='main'),
    path('client/create', views.ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update', views.ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', views.ClientDeleteView.as_view(), name='client_delete'),
    path('client/<int:pk>', views.ClientDetailView.as_view(), name='client_detail'), 
    
    path('client/<int:pk>/project/<int:pk_proj>', views.ProjectDetailView.as_view(), name='project_detail'), 
    path('client/<int:pk>/project/create', views.ProjectCreateView.as_view(), name='project_create'),
    path('client/<int:pk>/project/<int:pk_proj>/update', views.ProjectUpdateView.as_view(), name='project_update'),
    path('client/<int:pk>/project/<int:pk_proj>/delete', views.ProjectDeleteView.as_view(), name='project_delete'),

    path('project/<int:pk_proj>/module/<int:pk_modu>', views.ModuleDetailView.as_view(), name='module_detail'),
    path('project/<int:pk_proj>/module/create', views.ModuleCreateView.as_view(), name='module_create'),
    path('project/<int:pk_proj>/module/<int:pk_modu>/update', views.ModuleUpdateView.as_view(), name='module_update'),
    path('project/<int:pk_proj>/module/<int:pk_modu>/delete', views.ModuleDeleteView.as_view(), name='module_delete'),

    path('module/<int:pk_modu>/part/<int:pk_part>', views.PartDetailView.as_view(), name='part_detail'),
    path('module/<int:pk_modu>/part/create', views.PartCreateView.as_view(), name='part_create'),
    path('module/<int:pk_modu>/part/<int:pk_part>/update', views.PartUpdateView.as_view(), name='part_update'),
    path('module/<int:pk_modu>/part/<int:pk_part>/delete', views.PartDeleteView.as_view(), name='part_delete'),

    path('fixing_elements', views.FixingListView.as_view(), name='fixing_list'),
    path('fixing/create', views.FixingCreateView.as_view(), name='fixing_create'),
    path('fixing/<int:pk_fixi>', views.FixingDetailView.as_view(), name='fixing_detail'),
    path('fixing/<int:pk_fixi>/update', views.FixingUpdateView.as_view(), name='fixing_update'),
    path('fixing/<int:pk_fixi>/delete', views.FixingDeleteView.as_view(), name='fixing_delete'),
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