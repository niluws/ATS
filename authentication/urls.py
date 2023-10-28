from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path('login/', views.Login.as_view(), name='token_obtain_pair'),
    path('me/', views.Me.as_view(), name='me'),
    path('activate/<str:otp_code>/', views.VerifyAccount.as_view(), name='otp_code'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('refresh/', views.RefreshToken.as_view(), name='refresh'),
]
