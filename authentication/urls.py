from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('activate/<str:otp_code>/', views.ActiveAccountAPIView.as_view(), name='otp_code'),
    path('login/', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('me/', views.MeAPIView.as_view(), name='me'),
    path('refresh/', views.RefreshTokenAPIView.as_view(), name='refresh'),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("verify_email/", views.VerifyEmailAPIView.as_view(), name="verify_email"),
    path("logs/", views.LogAPIView.as_view(), name="logs"),
]
