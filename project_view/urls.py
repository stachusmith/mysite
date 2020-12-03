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

    path('part/<int:pk_part>/topic/<int:pk_topi>', views.TopicDetailView.as_view(), name='topic_detail'),
    path('part/<int:pk_part>/topic/create', views.TopicCreateView.as_view(), name='topic_create'),
    path('part/<int:pk_part>/topic/<int:pk_topi>/update', views.TopicUpdateView.as_view(), name='topic_update'),
    path('part/<int:pk_part>/topic/<int:pk_topi>/delete', views.TopicDeleteView.as_view(), name='topic_delete'),

    path('topic/<int:pk_topi>/add_pic', views.AddPictureView.as_view(), name='picture_add'),
    path('topic/<int:pk_topi>/picture/<int:pk_pict>', views.stream_file, name='picture_stream'),
    path('topic/<int:pk_topi>/picture/<int:pk_pict>/del_pic', views.DeletePictureView.as_view(), name='picture_delete'),

    path('fixing_list', views.FixingListView.as_view(), name='fixing_list'),
    path('fixing/create', views.FixingCreateView.as_view(), name='fixing_create'),
    path('fixing/<int:pk>/update', views.FixingUpdateView.as_view(), name='fixing_update'),
    path('fixing/<int:pk>/delete', views.FixingDeleteView.as_view(), name='fixing_delete'),

    path('part/<int:pk_part>/fix/create', views.FixCreateView.as_view(), name='fix_create'),
    path('part/<int:pk_part>/fix/<int:pk>/update', views.FixUpdateView.as_view(), name='fixing_update'),
    path('part/<int:pk_part>/fix/<int:pk>/delete', views.FixDeleteView.as_view(), name='fixing_delete'),
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