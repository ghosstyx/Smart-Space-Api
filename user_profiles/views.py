from django.shortcuts import render, get_object_or_404
from accounts.models import NaturalPerson
from organizations.models import Department

# Create your views here.

app_name = 'user_profiles'
def profile(request, id):
    user = get_object_or_404(NaturalPerson, id=id)
    context = {'user': user}
    return render(request, 'profile.html', context=context)

def dashboard(request, id):
    user = get_object_or_404(NaturalPerson, id=id)
    context = {'user': user}
    return render(request, 'index.html', context=context)

def employees(request):
    user = NaturalPerson.objects.all()
    departments = Department.objects.all()
    context = {'user': user, 'departments' :departments}
    return render(request, 'employees.html', context=context)