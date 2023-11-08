from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user'),
    path('profile/<int:pk>/', views.ProfileAPIView.as_view(), name='profile'),
]
