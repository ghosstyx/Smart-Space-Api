from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserCreationForm
from accounts.models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User

    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Информация', {'fields': ('first_name', 'last_name', 'middle_name', 'birthday')}),
        ('Права', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'is_staff', 'is_active')}
        ),
    )
    search_fields = ('first_name', 'last_name', 'middle_name', 'email',)
    ordering = ('email',)
    date_hierarchy = 'date_joined'


@admin.register(NaturalPerson)
class NaturalPersonAdmin(admin.ModelAdmin):
    list_display = ('pnf', 'full_name', 'birthday', 'branch', 'organization', 'department', 'jobTitle', "work_hours")
    ordering = ('birthday',)
    search_fields = ('full_name', 'pnf')

