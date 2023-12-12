from django.urls import path

from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.UserListView.as_view(), name='employee'),
    path('profile/<int:pk>/', views.ProfileAPIView.as_view(), name='profile'),
]
