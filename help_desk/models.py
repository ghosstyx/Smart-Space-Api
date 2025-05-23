from django.db import models
from accounts.models import NaturalPerson
from organizations.models import Department
from django.utils import timezone


class Project(models.Model):
    PROJECT_TYPES = [
        ('custom', 'Custom Project'),
        ('department', 'Department Board'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, related_name='owned_projects')
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='custom')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')

    class Meta:
        permissions = [
            ('manage_department_projects', 'Can manage department projects'),
        ]

    def __str__(self):
        return self.title

    def has_access(self, user):
        """Проверка доступа пользователя к проекту"""
        if self.project_type == 'custom':
            # Для кастомного проекта - доступ есть у владельца и участников задач
            return (self.owner == user or
                    self.tasks.filter(assignee=user).exists())
        else:
            # Для доски департамента - доступ у всех сотрудников департамента
            # и администраторов департамента
            return (user.department == self.department or
                    user.has_perm('help_desk.manage_department_projects'))


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(NaturalPerson, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now().date()


class Column(models.Model):
    title = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='columns')
    order = models.PositiveIntegerField(default=0)