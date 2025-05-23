from django import forms
from .models import Project, Task
from organizations.models import Department
from accounts.models import NaturalPerson


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type', 'department']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Task description'
            }),
            'project_type': forms.Select(attrs={
                'id': 'project-type-select',
                'onchange': 'toggleDepartmentField()'
            }),
            'department': forms.Select(attrs={
                'id': 'department-select',
                'disabled': True
            }),
        }



    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not self.user.has_perm('help_desk.manage_department_projects'):
            self.fields['project_type'].choices = [('custom', 'Custom Project')]

        if self.instance and self.instance.project_type == 'custom':
            self.fields['department'].disabled = True


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assignee', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Task description'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-date'
            }),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project:
            if project.project_type == 'custom':
                participants = NaturalPerson.objects.filter(
                    tasks__project=project
                ).distinct()
                self.fields['assignee'].queryset = participants
            else:
                self.fields['assignee'].queryset = NaturalPerson.objects.filter(
                    department=project.department
                )
