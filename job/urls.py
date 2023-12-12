from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'job'

router = DefaultRouter()
router.register('job_title', views.JobViewSet)
router.register('new_request', views.NewRequestViewSet, basename="new_request")
router.register('job_requirement', views.JobRequirementViewSet, basename="job_requirement")
router.register(r'question', views.QuestionsViewSet, basename="question")
router.register(r'role', views.RoleViewSet, basename="role")

urlpatterns = [
    path('', include(router.urls)),
    path("hr_approve/<int:pk>", views.HRApproval.as_view(), name="hr_approve"),
    path("td_approve/<int:pk>", views.TDApproval.as_view(), name="td_approve"),
]
