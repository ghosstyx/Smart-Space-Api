from django.db import models
from accounts.models import NaturalPerson

# Create your models here.
class Project(models.Model):
     title = models.CharField(max_length=100)
     description = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     owner = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, blank=True, null=True)

     def __str__(self):
         return self.title
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE, blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
