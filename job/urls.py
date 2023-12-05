from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'job'

router = DefaultRouter()
router.register('job_title', views.JobViewSet)
router.register('new_request', views.NewPositionViewSet, basename="new_postion")
router.register('job_requirement', views.JobRequirementViewSet, basename="job_requirement")

urlpatterns = [
    path('', include(router.urls)),
    path("hr_approve/<int:pk>", views.HRApproval.as_view(), name="hr_approve"),
    path("td_approve/<int:pk>", views.TDApproval.as_view(), name="td_approve"),
]
