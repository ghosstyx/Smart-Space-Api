from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NaturalPerson
from .forms import CustomUserCreationForm


@admin.register(NaturalPerson)
class NaturalPersonAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = NaturalPerson

    list_display = ('email', 'phone', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('phone',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Организация', {'fields': ('branch', 'organization', 'department', 'jobTitle', 'work_hours')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'phone', 'password1', 'password2'),
        }),
    )