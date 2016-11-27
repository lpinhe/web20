from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    finishing_date = models.DateTimeField(null=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return u'/projects/%d' % self.id


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creation_date = timezone.now()
    finishing_date = models.DateTimeField(null=True)


class Task(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    creation_date = timezone.now()
    PHASE = (
        ('ToDo', 'To Do'),
        ('iP', 'in Progress'),
        ('iR', 'in Review'),
        ('F', 'Finished'),
    )
    phase = models.CharField(max_length=4,
                             choices=PHASE,
                             default='Todo')
    name = models.CharField(max_length=300, default='Task')
    description = models.TextField()
    assignedUser = models.ForeignKey(User, related_name='tasks', verbose_name='User')


class InProjectIdea(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    description = models.TextField()
    creation_date = timezone.now()
    transfered_to_sprint = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['votes']


class GeneralIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    creation_date = timezone.now()
    votes = models.IntegerField(default=0)
    transfered_to_project = models.BooleanField(default=False)

    class Meta:
        ordering = ['-votes']


class Vote(models.Model):
    class Meta:
        unique_together = (('user', 'generalIdea', 'inProjectIdea'),)

    user = models.ForeignKey(User)
    generalIdea = models.ForeignKey(GeneralIdea, null=True, default=None)
    inProjectIdea = models.ForeignKey(InProjectIdea, null=True, default=None)
