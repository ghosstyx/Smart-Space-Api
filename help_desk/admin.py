from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'department')
    list_filter = ('project_type', 'department')
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee')