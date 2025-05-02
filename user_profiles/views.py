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
from django.contrib import messages
app_name = 'user_profiles'


class ProfileView(LoginRequiredMixin, DetailView):
    model = NaturalPerson
    form_class = ProfileForm
    template_name = 'user_profiles/profile-owner.html'
    context_object_name = 'user'
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        self.profile_user = get_object_or_404(NaturalPerson, id=kwargs['id'])

        # Автоматическое создание связи при отсутствии (для разработки)
        if not hasattr(request.user, 'naturalperson'):
            NaturalPerson.objects.create(
                user=request.user,
                full_name=request.user.get_full_name() or f"User-{request.user.id}"
            )
            messages.info(request, "Профиль автоматически создан")

        # Теперь проверка будет работать
        if request.user.naturalperson.id != self.profile_user.id:
            return redirect('user_profiles:profile_visitor', id=self.profile_user.id)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(
            request.POST,
            instance=self.object
        )

        if not form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form)
            )

        form.save()
        return redirect(
            reverse(
                'profile',
                kwargs={'id': self.object.id}
            )
        )


class ProfileVisitorView(DetailView):
    template_name = 'user_profiles/profile-visitor.html'
    model = NaturalPerson
    context_object_name = 'user'
    pk_url_kwarg = 'id'

class DashboardView(DetailView):
    model = NaturalPerson
    template_name = 'index.html'
    context_object_name = 'user'
    pk_url_kwarg = 'id'


class EmployeesView(View):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        self.profile_user = get_object_or_404(NaturalPerson, id=kwargs['id'])
        search_term = request.GET.get('search', '')
        selected_dept = request.GET.get('department')
        employees = NaturalPerson.objects.select_related('department').only(
            'id', 'full_name', 'department__deptName'
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
                Q(position__icontains=search_term) |
                Q(department__name__icontains=search_term)
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