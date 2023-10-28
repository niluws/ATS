from django.urls import path
from . import views

app_name = 'inbox'

urlpatterns = [
    path("new_request/", views.NewPositionAPIView.as_view(), name="register"),

]
