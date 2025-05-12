from django.views.generic import DetailView, ListView, TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import NaturalPerson
from django.urls import reverse
from organizations.models import Department
from .forms import ProfileForm
from django.db.models import Q
from django.contrib import messages

app_name = 'user_profiles'


class ProfileView(LoginRequiredMixin, DetailView):
    model = NaturalPerson
    form_class = ProfileForm
    template_name = 'user_profiles/profile-owner.html'
    context_object_name = 'profile_user'  # Изменили для ясности
    pk_url_kwarg = 'pk'  # Изменили с np_id на pk для единообразия

    def dispatch(self, request, *args, **kwargs):
        # Теперь NaturalPerson - это сам пользователь, а не связанная модель
        self.profile_user = get_object_or_404(NaturalPerson, pk=kwargs['pk'])

        if request.user.pk != self.profile_user.pk:
            self.template_name = 'user_profiles/profile-visitor.html'

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.pk == self.object.pk:
            context['form'] = ProfileForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.pk != self.object.pk:
            raise PermissionDenied

        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('user_profiles:profile', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


class DashboardView(LoginRequiredMixin, DetailView):
    template_name = 'index.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class EmployeesView(LoginRequiredMixin, View):
    def get(self, request):
        departments = Department.objects.all()
        search_term = request.GET.get('search', '')
        selected_dept = request.GET.get('department')

        employees = NaturalPerson.objects.select_related('department').only(
            'pk', 'first_name', 'last_name', 'department__deptName', 'jobTitle__jobTitle'
        ).exclude(pk=request.user.pk)

        if selected_dept and selected_dept != 'all':
            try:
                employees = employees.filter(department__id=int(selected_dept))
            except ValueError:
                pass

        if search_term:
            employees = employees.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(jobTitle__jobTitle__icontains=search_term) |
                Q(department__deptName__icontains=search_term)
            )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('partials/_employees_list.html', {
                'employees': employees
            })
            return JsonResponse({'html': html})

        return render(request, 'employees.html', {
            'employees': employees,
            'departments': departments,
            'selected_dept': selected_dept,
        })


def permission_denied_view(request):
    return render(request, '403.html', status=403)