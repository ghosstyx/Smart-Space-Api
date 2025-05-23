from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from accounts.models import NaturalPerson
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.db.models import Q


app_name = 'help_desk'


class ProjectAccessMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, id=self.kwargs['pk'])

        if self.project.project_type == 'department':
            if not hasattr(request.user, 'department'):
                raise Http404("Department profile required")
            if self.project.department is None:
                raise Http404("Project has no department")

        if not self.project.has_access(request.user):
            raise Http404("Access denied")

        return super().dispatch(request, *args, **kwargs)


class KanbanBoardView(ProjectAccessMixin, FormMixin, DetailView):
    model = Project
    template_name = 'kanban/board.html'
    form_class = TaskForm
    context_object_name = 'project'
    pk_url_kwarg = 'pk'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.project
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['project_form'] = ProjectForm(instance=self.project, user=self.request.user)
        context.update({
            'todo_tasks': self.project.tasks.filter(status='todo'),
            'progress_tasks': self.project.tasks.filter(status='progress'),
            'done_tasks': self.project.tasks.filter(status='done'),
            'can_edit': self.can_edit_project(),
            'is_department_project': self.project.project_type == 'department'
        })
        context['can_edit_project'] = (
                self.project.owner == self.request.user or
                self.request.user.has_perm('help_desk.manage_department_projects')
        )
        return context

    def can_edit_project(self):
        user = self.request.user
        project = self.project

        if project.project_type == 'custom':
            return user == project.owner
        else:
            return (user == project.owner or
                    user.has_perm('help_desk.manage_department_projects') or
                    (hasattr(user, 'is_department_head') and
                     user.is_department_head and
                     user.department == project.department))

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax(request)
        return super().post(request, *args, **kwargs)

    def handle_ajax(self, request):
        action = request.POST.get('action')

        if not self.can_edit_project():
            return JsonResponse({'success': False, 'error': 'No edit permissions'}, status=403)

        handlers = {
            'delete_task': self.handle_delete_task,
            'update_status': self.handle_update_status,
            'create_task': self.handle_create_task
        }

        handler = handlers.get(action)
        if handler:
            return handler(request)
        return JsonResponse({'success': False}, status=400)

    def handle_delete_task(self, request):
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id, project=self.project)
            task.delete()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

    def handle_update_status(self, request):
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('new_status')
        try:
            task = Task.objects.get(id=task_id, project=self.project)
            task.status = new_status
            task.save()
            return JsonResponse({
                'success': True,
                'status_display': task.get_status_display(),
                'task_id': task.id
            })
        except Task.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

    def handle_create_task(self, request):
        form = self.get_form()
        if form.is_valid():
            task = form.save(commit=False)
            task.project = self.project
            task.save()
            return JsonResponse({
                'success': True,
                'task_html': render_to_string(
                    'kanban/partials/task_card.html',
                    {'task': task}
                )
            })
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'kanban/project_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.instance.project_type == 'custom':
            form.instance.department = None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('help_desk:kanban_board', kwargs={
            'np_id': self.request.user.id,
            'pk': self.object.id
        })


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'kanban/project_form.html'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if not (project.owner == request.user or
                request.user.has_perm('help_desk.manage_department_projects') or
                (hasattr(request.user, 'is_department_head') and
                 request.user.is_department_head and
                 request.user.department == project.department)):
            raise Http404("Edit not allowed")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax(request)
        return super().post(request, *args, **kwargs)

    def handle_ajax(self, request):
        handlers = {
            'update_project': self.handle_update_project,
        }
        if request.POST.get('action') == 'update_project':
            form = ProjectForm(request.POST, instance=self.get_object(), user=request.user)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return JsonResponse({'success': False}, status=400)
    def handle_update_project(self, request):
        form = ProjectForm(request.POST, instance=self.project, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('help_desk:kanban_board', kwargs={
            'np_id': self.request.user.id,
            'pk': self.object.id
        })