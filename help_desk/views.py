from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import NaturalPerson
from .models import *
from .forms import *

app_name = 'help_desk'
class KanbanBoardView(LoginRequiredMixin, FormMixin, DetailView):
    model = Project
    template_name = 'kanban/board.html'
    form_class = TaskForm
    context_object_name = 'project'
    pk_url_kwarg = 'pk'

    def get_object(self):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        if project.owner.id != self.kwargs['np_id']:
            raise Http404("Проект не принадлежит пользователю")
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context.update({
            'todo_tasks': Task.objects.filter(project=project, status='todo'),
            'progress_tasks': Task.objects.filter(project=project, status='progress'),
            'done_tasks': Task.objects.filter(project=project, status='done'),
            'users': NaturalPerson.objects.all(),
        })

        return context


    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax(request)
        return super().post(request, *args, **kwargs)

    def handle_ajax(self, request):
        action = request.POST.get('action')

        if action == 'delete_task':
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                return JsonResponse({'success': True})
            except Task.DoesNotExist:
                return JsonResponse({'success': False}, status=404)

        if action == 'update_status':
            task_id = request.POST.get('task_id')
            new_status = request.POST.get('new_status')
            try:
                task = Task.objects.get(id=task_id)
                task.status = new_status
                task.save()
                return JsonResponse({
                    'success': True,
                    'status_display': task.get_status_display(),
                    'task_id': task.id
                })
            except Task.DoesNotExist:
                return JsonResponse({'success': False}, status=404)
        elif action == 'create_task':
            form = self.get_form()
            if form.is_valid():
                task = form.save(commit=False)
                task.project = self.get_object()
                task.save()
                return JsonResponse({
                    'success': True,
                    'task_html': render_to_string(
                        'kanban/partials/task_card.html',
                        {'task': task}
                    )
                })
            return  JsonResponse({'success': False, 'errors': form.errors}, status=400)

        return JsonResponse({'success': False}, status=400)




















