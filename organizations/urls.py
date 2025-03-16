from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

app_name = "organizations"

urlpatterns = [
    path('org/', adm , name='organizations'),
]
