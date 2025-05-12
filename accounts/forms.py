from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import NaturalPerson


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NaturalPerson
        fields = ('phone',)  # Используем phone вместо email как основное поле

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'