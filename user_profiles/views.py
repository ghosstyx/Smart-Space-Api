from django.views.generic import DetailView, ListView, TemplateView, View
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string

from accounts.models import NaturalPerson
from organizations.models import Department

app_name = 'user_profiles'

class ProfileView(DetailView):
    model = NaturalPerson
    template_name = 'profile.html'
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