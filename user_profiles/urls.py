from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('profile/visitor/<int:id>/', ProfileVisitorView.as_view(), name='profile_visitor'),
    path('dashboard/<int:id>/', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('permission-denied/', permission_denied_view, name='permission_denied'),
]