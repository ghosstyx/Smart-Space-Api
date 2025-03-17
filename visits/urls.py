from django.urls import path
from .views import *

app_name = "visits"

urlpatterns = [
    path('visit/', adm , name='visits'),
]
