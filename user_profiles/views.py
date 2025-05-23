from django.views.generic import DetailView, ListView, TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import NaturalPerson
from organizations.models import Department
from .forms import ProfileForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


app_name = 'user_profiles'


class ProfileView(LoginRequiredMixin, DetailView):
    model = NaturalPerson
    form_class = ProfileForm
    context_object_name = 'profile_user'
    pk_url_kwarg = 'pk'

    def get_template_names(self):
        if self.request.user.pk == self.kwargs['pk']:
            return ['user_profiles/profile-owner.html']
        return ['user_profiles/profile-visitor.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.pk == self.object.pk:
            context['form'] = self.form_class(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('user_profiles:profile', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        if self.request.method == 'POST':
            return self.request.user.pk == self.kwargs['pk']
        return True


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class EmployeesView(LoginRequiredMixin, View):
    def get(self, request):
        departments = Department.objects.all().only('id', 'deptName')
        search_term = request.GET.get('search', '')
        selected_dept = request.GET.get('department')

        employees = self._get_filtered_employees(request, search_term, selected_dept)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('partials/_employees_list.html', {'employees': employees})
            return JsonResponse({'html': html})

        return render(request, 'employees.html', {
            'employees': employees,
            'departments': departments,
            'selected_dept': selected_dept,
        })

    def _get_filtered_employees(self, request, search_term, selected_dept):
        employees = NaturalPerson.objects.select_related(
            'department', 'jobTitle', 'organization'
        ).only(
            'pk', 'first_name', 'last_name',
            'department__deptName', 'jobTitle__jobTitle', 'organization__organizationTitle'
        ).exclude(pk=request.user.pk)

        if selected_dept and selected_dept != 'all':
            employees = employees.filter(department__id=selected_dept)

        if search_term:
            employees = employees.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(jobTitle__jobTitle__icontains=search_term) |
                Q(department__deptName__icontains=search_term)
            )
        return employees


def permission_denied_view(request):
    return render(request, '403.html', status=403)