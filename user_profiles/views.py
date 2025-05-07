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
    context_object_name = 'natural_person'
    pk_url_kwarg = 'np_id'

    def dispatch(self, request, *args, **kwargs):
        self.profile_natural = get_object_or_404(NaturalPerson, id=kwargs['np_id'])

        if not hasattr(request.user, 'naturalperson'):
            NaturalPerson.objects.create(
                user=request.user,
                full_name=request.user.get_full_name() or f"User-{request.user.id}"
            )
            messages.info(request, "Профиль автоматически создан")

        if hasattr(request.user, 'naturalperson'):
            if request.user.naturalperson.id != self.profile_natural.id:
                self.template_name = 'user_profiles/profile-visitor.html'

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'naturalperson'):
            if self.request.user.naturalperson.id == self.object.id:
                context['form'] = ProfileForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not hasattr(request.user, 'naturalperson') or request.user.naturalperson.id != self.object.id:
            raise PermissionDenied

        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('user_profiles:profile', np_id=self.object.id)
        return self.render_to_response(self.get_context_data(form=form))


class DashboardView(DetailView):
    model = NaturalPerson
    template_name = 'index.html'
    context_object_name = 'user'
    pk_url_kwarg = 'np_id'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'naturalperson'):
            NaturalPerson.objects.create(
                user=request.user,
                full_name=request.user.get_full_name() or f"User-{request.user.id}"
            )
            messages.info(request, "Профиль автоматически создан")
        return super().dispatch(request, *args, **kwargs)

class EmployeesView(View):
    def get(self, request):
        departments = Department.objects.all()
        self.profile_user = get_object_or_404(NaturalPerson, user=request.user)
        search_term = request.GET.get('search', '')
        selected_dept = request.GET.get('department')
        employees = NaturalPerson.objects.select_related('department').only(
            'id', 'full_name', 'department__deptName', 'jobTitle__jobTitle'
        )
        if selected_dept and selected_dept != 'all':
            try:
                employees = employees.filter(department__id=int(selected_dept))
            except ValueError:
                pass
        employees = employees[:20]

        if search_term:
            employees = employees.filter(
                Q(full_name__icontains=search_term) |
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

    def get_queryset(self):
        return NaturalPerson.objects.exclude(id=self.request.user.id)

def permission_denied_view(request):
    return render(request, '403.html', status=403)