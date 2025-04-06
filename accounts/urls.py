from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='account_register'),

    path('send-otp/', views.SendOTPAPIView.as_view(), name="send_otp"),
    path('loginapi/', views.LoginAPIView.as_view(), name='account_login'),

    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('logout/', views.LogoutView.as_view(), name='rest_logout'),
    # path('login/', login, name="Login"), ## http://127.0.0.1:8000/auth/login/

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]