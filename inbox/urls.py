from django.urls import path
from . import views

urlpatterns = [
    path("new_request/", views.NewPositionAPIView.as_view(), name="register"),

]
