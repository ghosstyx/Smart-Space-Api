from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('dashboard/<int:id>/', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
]