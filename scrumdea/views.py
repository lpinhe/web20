from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, FormView, View, ListView, DeleteView, \
    RedirectView
from django.shortcuts import render, get_object_or_404, render_to_response, resolve_url, redirect
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib import parse as urlparse
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.contrib import auth
from scrumdea.utils import default_redirect

from scrumdea import models as src_models
from scrumdea import forms as src_forms


# General Idea Views
class GeneralIdeaListView(LoginRequiredMixin, ListView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/final/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GeneralIdeaListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['projects'] = src_models.Project.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        update_vote_count_general_idea()
        return super(GeneralIdeaListView, self).dispatch(request, *args, **kwargs)


class GeneralIdeaListListView(LoginRequiredMixin, ListView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/final/project_ideas.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GeneralIdeaListListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['projects'] = src_models.Project.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        update_vote_count_general_idea()
        return super(GeneralIdeaListListView, self).dispatch(request, *args, **kwargs)


class GeneralIdeaDetailView(LoginRequiredMixin, DetailView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/final/project_idea.html"

    def dispatch(self, request, *args, **kwargs):
        # called during init of class
        update_vote_count_general_idea()

        # call the view
        return super(GeneralIdeaDetailView, self).dispatch(request, *args, **kwargs)


class GeneralIdeaCreateView(LoginRequiredMixin, CreateView):
    model = src_models.GeneralIdea
    fields = ['title', 'description']
    template_name = "scrumdea/final/add_generalIdea.html"

    def get_success_url(self):
        return reverse('general_idea_detail_view', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> New Idea created :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class GeneralIdeaUpdateView(LoginRequiredMixin, UpdateView):
    model = src_models.GeneralIdea
    fields = ['title', 'description']
    template_name = "scrumdea/final/edit_generlIdea.html"

    def get_success_url(self):
        return reverse('general_idea_detail_view', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Idea updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class GeneralIdeaDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/final/delete_generalidea.html"

    def get_success_url(self):
        return reverse('general_idea_listlist_view')


# InProjectIdea
class InProjectIdeaCreateView(LoginRequiredMixin, CreateView):
    model = src_models.InProjectIdea
    fields = ['title', 'description']
    template_name = "scrumdea/final/add_inProjectIdea.html"

    def get_success_url(self):
        return reverse('project_detail_view', kwargs={"pk": self.object.project.id})

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> New Idea created :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.project = src_models.Project.objects.get(id=self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class InProjectIdeaDetailView(LoginRequiredMixin, DetailView):
    model = src_models.InProjectIdea
    template_name = "scrumdea/final/inProjectIdea_details.html"

    def get_object(self, queryset=None):
        return src_models.InProjectIdea.objects.get(id=self.kwargs['ipk'])

    def dispatch(self, request, *args, **kwargs):
        update_vote_count_in_project_idea()
        return super(InProjectIdeaDetailView, self).dispatch(request, *args, **kwargs)


class InProjectIdeaDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Sprint
    template_name = "scrumdea/final/delete_task_idea.html"

    def get_object(self, queryset=None):
        return src_models.InProjectIdea.objects.get(id=self.kwargs['ipk'])

    def get_success_url(self):
        return reverse('project_detail_view',
                       kwargs={'pk': self.kwargs['pk']})


class InProjectIdeaEditView(LoginRequiredMixin, UpdateView):
    model = src_models.InProjectIdea
    fields = ['title', 'description']
    template_name = "scrumdea/final/edit_task.html"

    def get_object(self, queryset=None):
        return src_models.InProjectIdea.objects.get(id=self.kwargs['ipk'])

    def get_success_url(self):
        return reverse('project_detail_view',
                       kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Sprint updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class InProjectIdeaCreateTaskView(LoginRequiredMixin, RedirectView):
    model = src_models.Task

    def get_redirect_url(self, *args, **kwargs):
        task_idea = src_models.InProjectIdea.objects.get(id=kwargs['ipk'])
        sprint_count = src_models.Sprint.objects.filter(project=kwargs['pk']).count()
        sprint_name = "Sprint " + str(sprint_count)
        current_sprint = src_models.Sprint.objects.get(name=sprint_name, project=kwargs['pk'])

        new_task = src_models.Task()
        new_task.sprint = current_sprint
        new_task.name = task_idea.title
        new_task.description = task_idea.description
        new_task.assignedUser = self.request.user
        new_task.save()

        task_idea.delete()

        messages.success(self.request, "<b>Successfully</b> added idea to tasks! :)",
                         extra_tags='alert alert-success safe')
        return reverse('project_detail_view', kwargs={'pk': self.kwargs['pk']})


# Project Views
class ProjectNewListView(LoginRequiredMixin, ListView):
    model = src_models.Project
    template_name = "scrumdea/final/my_projects.html"


class ProjectRunningListView(LoginRequiredMixin, ListView):
    model = src_models.Project
    template_name = "scrumdea/final/running_projects.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = src_models.Project
    template_name = 'scrumdea/final/project_page.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        sprint_list = src_models.Sprint.objects.filter(project=self.kwargs['pk'])
        sprints = []
        for sprint in sprint_list:
            sprint_dict = {'object': sprint,
                           'tasks_todo': src_models.Task.objects.filter(sprint=sprint.id, phase='ToDo'),
                           'tasks_in_progress': src_models.Task.objects.filter(sprint=sprint.id, phase='iP'),
                           'tasks_in_review': src_models.Task.objects.filter(sprint=sprint.id, phase='iR'),
                           'tasks_finished': src_models.Task.objects.filter(sprint=sprint.id, phase='F')}
            sprints.append(sprint_dict)

        context['sprints'] = sprints
        context['idea_list'] = src_models.InProjectIdea.objects.filter(project=self.kwargs['pk']).order_by('-votes')
        context['newest_sprint_id'] = (src_models.Sprint.objects.filter(project=self.kwargs['pk']))[0].id
        return context

    def dispatch(self, request, *args, **kwargs):
        update_vote_count_in_project_idea()
        return super(ProjectDetailView, self).dispatch(request, *args, **kwargs)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = src_models.Project
    form_class = src_forms.ProjectForm
    template_name = "scrumdea/final/add_project.html"

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> New Idea created :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        sprint1 = src_models.Sprint()
        sprint1.name = "Sprint 1"
        sprint1.project = self.object
        sprint1.save()
        return HttpResponseRedirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())

    context_object_name = 'project'


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Project
    template_name = "scrumdea/final/delete_project.html"

    def get_success_url(self):
        return reverse('project_list_view')


class ProjectEditView(LoginRequiredMixin, UpdateView):
    model = src_models.Project
    fields = ['name', 'description']
    template_name = "scrumdea/final/edit_project.html"

    def get_success_url(self):
        return reverse('project_detail_view', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Project updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


# sprint views
class SprintListView(LoginRequiredMixin, ListView):
    model = src_models.Sprint
    template_name = "scrumdea/sprint/sprint-list.html"

    def get_queryset(self):
        return src_models.Sprint.objects.filter(project=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SprintListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        return context


class SprintCreateView(LoginRequiredMixin, CreateView):
    model = src_models.Sprint
    template_name = 'scrumdea/sprint/sprint-create.html'
    context_object_name = 'sprint'
    form_class = src_forms.SprintForm

    def get_success_url(self):
        return reverse('sprint_list_view', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Sprint created! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.project = src_models.Project.objects.get(id=self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class SprintAutoCreateView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        sprint = src_models.Sprint()
        sprint_count = src_models.Sprint.objects.filter(project=kwargs['pk']).count()
        sprint.name = "Sprint " + str(sprint_count + 1)
        sprint.project = src_models.Project.objects.get(id=kwargs['pk'])
        sprint.save()
        messages.success(self.request, "<b>Success!</b> New Sprint created! :)", extra_tags='alert alert-success safe')
        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': sprint.id})


class SprintDetailView(LoginRequiredMixin, DetailView):
    model = src_models.Sprint
    template_name = 'scrumdea/final/sprint_details.html'

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_context_data(self, **kwargs):
        context = super(SprintDetailView, self).get_context_data(**kwargs)

        sprint_list = []
        sprint_list.append(src_models.Sprint.objects.get(id=self.kwargs['spk']))
        sprints = []
        for sprint in sprint_list:
            sprint_dict = {'object': sprint,
                           'tasks_todo': src_models.Task.objects.filter(sprint=sprint.id, phase='ToDo'),
                           'tasks_in_progress': src_models.Task.objects.filter(sprint=sprint.id, phase='iP'),
                           'tasks_in_review': src_models.Task.objects.filter(sprint=sprint.id, phase='iR'),
                           'tasks_finished': src_models.Task.objects.filter(sprint=sprint.id, phase='F')}
            sprints.append(sprint_dict)

        context['sprints'] = sprints
        context['allsprints'] = src_models.Sprint.objects.filter(project=self.kwargs['pk'])

        percent_complete = 0
        tasks_count = src_models.Task.objects.filter(sprint=self.kwargs['spk']).count()
        tasks_finished = src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='F').count()
        if tasks_count != 0:
            percent_complete = (tasks_finished / tasks_count) * 100
        context['sprint_complete_in_percent'] = round(percent_complete, 1)
        return context


class SprintDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Sprint
    template_name = "scrumdea/final/delete_sprint.html"

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_success_url(self):
        return reverse('project_detail_view',
                       kwargs={'pk': self.kwargs['pk']})


class SprintEditView(LoginRequiredMixin, UpdateView):
    model = src_models.Sprint
    fields = ['name', ]
    template_name = "scrumdea/sprint/sprint-update.html"

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_success_url(self):
        return reverse('sprint_detail_view',
                       kwargs={'pk': self.kwargs['pk'],
                               'spk': self.kwargs['spk']
                               })

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Sprint updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


# task view
class TaskListView(LoginRequiredMixin, ListView):
    model = src_models.Task
    template_name = "scrumdea/task/task-list.html"

    def get_queryset(self):
        return src_models.Task.objects.filter(sprint=self.kwargs['spk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TaskListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        context['sprint'] = src_models.Sprint.objects.get(id=self.kwargs['spk'])
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = src_models.Task
    template_name = 'scrumdea/final/add_task.html'
    context_object_name = 'task'
    form_class = src_forms.TaskForm

    def get_success_url(self):
        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Task created! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.sprint = src_models.Sprint.objects.get(id=self.kwargs['spk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = src_models.Task
    template_name = 'scrumdea/final/task_details.html'

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        return context


class TaskEditView(LoginRequiredMixin, UpdateView):
    model = src_models.Task
    form_class = src_forms.TaskForm
    template_name = "scrumdea/final/edit_task.html"

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_success_url(self):
        return reverse('sprint_detail_view',
                       kwargs={'pk': self.kwargs['pk'],
                               'spk': self.kwargs['spk']
                               })

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Task updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Task
    template_name = "scrumdea/final/delete-task.html"

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_success_url(self):
        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})


class TaskMoveRight(LoginRequiredMixin, RedirectView):
    model = src_models.Task

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def new_phase(self, argument):
        switcher = {
            'ToDo': 'iP',
            'iP': 'iR',
            'iR': 'F',
        }
        return switcher.get(argument, "F")

    def get_redirect_url(self, *args, **kwargs):
        task = src_models.Task.objects.get(id=self.kwargs['tpk'])
        task.phase = self.new_phase(task.phase)
        task.save()

        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})


# authentication

class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'scrumdea/final/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, ''))

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(TemplateResponseMixin, View):
    template_name = "scrumdea/final/logout.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        redirect_field_value = self.request.POST.get(
            redirect_field_name, self.request.GET.get(redirect_field_name, ''))
        context.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
        })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


# vote views
class VoteViewGeneralIdea(View):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('general_idea_detail_view', kwargs={'pk': self.kwargs['pk']})

    def get(self, request, *args, **kwargs):

        user = self.request.user
        general_idea = src_models.GeneralIdea.objects.get(id=kwargs["pk"])
        in_project_idea = None

        vote, created = src_models.Vote.objects.get_or_create(
            user=user,
            generalIdea=general_idea,
            inProjectIdea=in_project_idea
        )

        if not created:
            messages.error(self.request, "You have already voted for this Idea. Sorry.",
                           extra_tags='alert alert-danger safe')
            return HttpResponseRedirect(self.get_redirect_url())
        else:
            messages.success(self.request, "Awesome, thanks for voting!",
                             extra_tags='alert alert-success safe')
            update_vote_count_general_idea()
            return HttpResponseRedirect(self.get_redirect_url())


class VoteViewInProjectIdea(View):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('in_project_idea_detail_view', kwargs={'pk': self.kwargs['pk'], 'ipk': self.kwargs['ipk']})

    def get(self, request, *args, **kwargs):

        user = self.request.user
        general_idea = None
        in_project_idea = src_models.InProjectIdea.objects.get(id=kwargs["ipk"])

        vote, created = src_models.Vote.objects.get_or_create(
            user=user,
            generalIdea=general_idea,
            inProjectIdea=in_project_idea
        )

        if not created:
            messages.error(self.request, "You have already voted for this Idea. Sorry.",
                           extra_tags='alert alert-danger safe')
            return HttpResponseRedirect(self.get_redirect_url())
        else:
            messages.success(self.request, "Awesome, thanks for voting!",
                             extra_tags='alert alert-success safe')
            update_vote_count_in_project_idea()
            return HttpResponseRedirect(self.get_redirect_url())


# Updates all votes of general ideas
def update_vote_count_general_idea():
    all_ideas = src_models.GeneralIdea.objects.all()
    for idea in all_ideas:
        vote_count = (src_models.Vote.objects.filter(generalIdea=idea.id, inProjectIdea__isnull=True)).count();
        idea.votes = vote_count
        idea.save()


def update_vote_count_in_project_idea():
    all_ideas = src_models.InProjectIdea.objects.all()
    for idea in all_ideas:
        vote_count = (src_models.Vote.objects.filter(inProjectIdea=idea.id, generalIdea__isnull=True)).count();
        idea.votes = vote_count
        idea.save()


# trash
def page_not_found(request):
    response = render_to_response('scrumdea/404.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response
