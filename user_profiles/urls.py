from django.urls import path
from .views import *

urlpatterns = [
    path('profile/np-<int:np_id>/', ProfileView.as_view(), name='profile'),
    path('dashboard/np-<int:np_id>/', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('permission-denied/', permission_denied_view, name='permission_denied'),
]