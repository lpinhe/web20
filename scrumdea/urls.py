from django.conf.urls import url, handler404
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # General idea
    url(r'^$', views.GeneralIdeaListView.as_view(), name='general_idea_list_view'),
    url(r'^accounts/profile/$', views.GeneralIdeaListView.as_view(), name='general_idea_list_view'),
    url(r'^ideas/$', views.GeneralIdeaListListView.as_view(), name='general_idea_listlist_view'),
    url(r'^general-ideas/(?P<pk>\d+)/$', login_required(views.GeneralIdeaDetailView.as_view()),
        name='general_idea_detail_view'),
    url(r'^general-ideas/create/$', views.GeneralIdeaCreateView.as_view(), name='general_idea_create_view'),
    url(r'^general-ideas/(?P<pk>\d+)/edit$', views.GeneralIdeaUpdateView.as_view(), name='general_idea_edit_view'),
    url(r'^general-ideas/(?P<pk>\d+)/delete$', views.GeneralIdeaDeleteView.as_view(), name='general_idea_delete_view'),
    url(r'^general-ideas/(?P<pk>\d+)/vote$', views.VoteViewGeneralIdea.as_view(), name='general_idea_vote_view'),

    # Projects
    url(r'^projects/$', views.ProjectNewListView.as_view(), name='project_list_view'),
    url(r'^projects/running$', views.ProjectRunningListView.as_view(), name='project_running_list_view'),
    url(r'^projects/create$', views.ProjectCreateView.as_view(), name='project_create_view'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project_detail_view'),
    url(r'^projects/(?P<pk>\d+)/edit$', views.ProjectEditView.as_view(), name='project_edit_view'),
    url(r'^projects/(?P<pk>\d+)/delete$', views.ProjectDeleteView.as_view(), name='project_delete_view'),

    url(r'^projects/(?P<pk>\d+)/task-idea/create$', views.InProjectIdeaCreateView.as_view(),
        name='in_project_create_view'),
    url(r'^projects/(?P<pk>\d+)/task-idea/(?P<ipk>\d+)/transfer$', views.InProjectIdeaCreateTaskView.as_view(),
        name='in_project_create_task_view'),
    url(r'^projects/(?P<pk>\d+)/task-idea/(?P<ipk>\d+)/$', views.InProjectIdeaDetailView.as_view(),
        name='in_project_idea_detail_view'),
    url(r'^projects/(?P<pk>\d+)/task-idea/(?P<ipk>\d+)/vote$', views.VoteViewInProjectIdea.as_view(),
        name='in_project_idea_vote_view'),
    url(r'^projects/(?P<pk>\d+)/task-idea/(?P<ipk>\d+)/delete$', views.InProjectIdeaDeleteView.as_view(),
        name='in_project_idea_delete_view'),
    url(r'^projects/(?P<pk>\d+)/task-idea/(?P<ipk>\d+)/edit$', views.InProjectIdeaEditView.as_view(),
        name='in_project_idea_edit_view'),


    # Sprints
    url(r'^projects/(?P<pk>\d+)/sprints/$', views.SprintListView.as_view(), name='sprint_list_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/create$', views.SprintAutoCreateView.as_view(), name='sprint_create_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/$', views.SprintDetailView.as_view(), name='sprint_detail_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/delete$', views.SprintDeleteView.as_view(),
        name='sprint_delete_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/edit$', views.SprintEditView.as_view(),
        name='sprint_edit_view'),

    # Tasks
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/tasks/$', views.TaskListView.as_view(), name='task_list_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/tasks/create$', views.TaskCreateView.as_view(),
        name='task_create_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/tasks/(?P<tpk>\d+)/$', views.TaskDetailView.as_view(),
        name='task_detail_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/tasks/(?P<tpk>\d+)/edit$', views.TaskEditView.as_view(),
        name='task_edit_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/tasks/(?P<tpk>\d+)/delete$', views.TaskDeleteView.as_view(),
        name='task_delete_view'),
    url(r'^projects/(?P<pk>\d+)/sprints/(?P<spk>\d+)/tasks/(?P<tpk>\d+)/move-right$', views.TaskMoveRight.as_view(),
        name='task_move_right_view'),

    # Authenication
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login_view'),
    url(r'^accounts/logout/$', views.LogoutView.as_view(), name='logout_view'),

]
