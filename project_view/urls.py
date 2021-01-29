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
    path('topic/<int:pk_topi>/cancel', views.TopicCancelView.as_view(), name='topic_cancel'),
    path('part/<int:pk_part>/topic/<int:pk_topi>/entry/<int:pk>/update', views.TopicEntryUpdateView.as_view(), name='topic_entry_update'),


    path('topic/<int:pk_topi>/add_pic', views.AddPictureView.as_view(), name='picture_add'),
    path('topic/<int:pk_topi>/picture/<int:pk_pict>', views.stream_file, name='picture_stream'),
    path('topic/<int:pk_topi>/picture/<int:pk_pict>/del_pic', views.DeletePictureView.as_view(), name='picture_delete'),

    path('fixing_list', views.FixingListView.as_view(), name='fixing_list'),
    path('fixing/<int:pk>', views.FixingDetailView.as_view(), name='fixing_detail'),
    path('fixing/create', views.FixingCreateView.as_view(), name='fixing_create'),
    path('fixing/<int:pk>/update', views.FixingUpdateView.as_view(), name='fixing_update'),
    path('fixing/<int:pk>/delete', views.FixingDeleteView.as_view(), name='fixing_delete'),

    path('participant/create', views.ParticipantCreateView.as_view(), name='participant_create'),
    path('participant/<int:pk>/update', views.ParticipantUpdateView.as_view(), name='participant_update'),
    path('participant/<int:pk>/delete', views.ParticipantDeleteView.as_view(), name='participant_delete'),

    path('participation', views.ParticipationListView.as_view(), name='participation_list'),
    path('participant/<int:pk>/participation/create', views.ParticipationCreateView.as_view(), name='participation_create'),
    path('project/<int:pk_proj>/participation/create', views.ParticipationPrjCreateView.as_view(), name='participation_proj_create'),
    path('participation/<int:pk>/update', views.ParticipationUpdateView.as_view(), name='participation_update'),
    path('participation/<int:pk>/delete', views.ParticipationDeleteView.as_view(), name='participation_delete'),

    path('entries', views.EntryListView.as_view(), name='entries_list'),
    path('topic/<int:pk_topi>/create', views.EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/update', views.EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete', views.EntryDeleteView.as_view(), name='entry_delete'),

    
    path('part/<int:pk_part>/fix/create', views.FixCreateView.as_view(), name='fix_create'),
    path('part/<int:pk_part>/fix/<int:pk>/update', views.FixUpdateView.as_view(), name='fix_update'),
    path('part/<int:pk_part>/fix/<int:pk>/delete', views.FixDeleteView.as_view(), name='fix_delete'),

    path('part/<int:pk>/mypart', views.MypartView.as_view(), name='mypart'),
    path('part/<int:pk>/unmypart', views.UnmypartView.as_view(), name='unmypart'),


]