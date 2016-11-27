from django.contrib import admin

# Register your models here.

from .models import Project, Sprint, Task, GeneralIdea, InProjectIdea, Vote


class SprintInLine(admin.TabularInline):
    model = Sprint
    extra = 1




class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
    ]
    inlines = [SprintInLine]
    class Meta:
        model = Project


class GeneralIdeaAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'votes']
    fieldsets = [
        (None, {'fields': ['title', 'description', 'votes']})
    ]

    class Meta:
        model = GeneralIdea


admin.site.register(Project, ProjectAdmin)

admin.site.register(Sprint)

admin.site.register(Task)

admin.site.register(GeneralIdea, GeneralIdeaAdmin)

admin.site.register(Vote)

admin.site.register(InProjectIdea)
