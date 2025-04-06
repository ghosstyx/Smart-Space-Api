from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<int:pk>/', profile, name='profile'),
    path('dashboard/<int:pk>/', dashboard, name='dashboard'),
]