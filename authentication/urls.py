from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('activate/<str:otp_code>/', views.VerifyAccountAPIView.as_view(), name='otp_code'),
    path('login/', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('me/', views.MeAPIView.as_view(), name='me'),
    path('profile/<int:pk>/', views.ProfileAPIView.as_view(), name='profile'),
    path('refresh/', views.RefreshTokenAPIView.as_view(), name='refresh'),
    path('user/', views.UserListView.as_view(), name='user'),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
]
