from django.shortcuts import render, get_object_or_404
from accounts.models import NaturalPerson

# Create your views here.

app_name = 'user_profiles'
def profile(request, *args, **kwargs):
    user_pk = kwargs['pk']
    natural_person = NaturalPerson.objects.filter(id=user_pk).first()
    context = {'natural_person': natural_person}
    return render(request, 'profile.html', context=context)

def dashboard(request, *args, **kwargs):
    user_pk = kwargs['pk']
    natural_person = NaturalPerson.objects.filter(id=user_pk).first()
    context = {'natural_person': natural_person}
    return render(request, 'index.html', context=context)