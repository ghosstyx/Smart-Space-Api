from django import forms
from accounts.models import  NaturalPerson


class ProfileForm(forms.ModelForm):
    class Meta:
        model = NaturalPerson
        fields = ['about']
        widgets = {
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Расскажите о себе...'
            })
        }