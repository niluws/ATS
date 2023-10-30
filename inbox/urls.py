from django.urls import path
from . import views

app_name = 'inbox'

urlpatterns = [
    path("new_request/", views.NewPositionAPIView.as_view(), name="register"),
    path("hr_approve/<int:pk>", views.HRApproval.as_view(), name="hr_approve"),
    path("td_approve/<int:pk>", views.TDApproval.as_view(), name="td_approve"),

]
