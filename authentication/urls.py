from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.Me.as_view(), name='me'),
    path('activate/<uuid:active_code>/', views.activate_account, name='activate_account'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
