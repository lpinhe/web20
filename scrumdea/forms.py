# -*- coding utf-8 -*-

from django import forms
from scrumdea import models as scr_models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = scr_models.Project
        fields = ('name', 'description')


class GeneralIdeaForm(forms.ModelForm):
    class Meta:
        model = scr_models.GeneralIdea
        fields = ('title', 'description')


class SprintForm(forms.ModelForm):
    class Meta:
        model = scr_models.Sprint
        fields = ('name',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = scr_models.Task
        fields = ('name', 'description','phase', 'assignedUser')
