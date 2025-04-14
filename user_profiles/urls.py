from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:id>/', profile, name='profile'),
    path('dashboard/<int:id>/', dashboard, name='dashboard'),
    path('employees/<int:id>/', employees, name='employees'),
]