from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='account_register'),

    path('send-otp/', views.SendOTPAPIView.as_view(), name="send_otp"),
    path('login/', views.LoginAPIView.as_view(), name='account_login'),

    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', views.LogoutView.as_view(), name='rest_logout'),

]
