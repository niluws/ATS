from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inbox'

router = DefaultRouter()
router.register('new_request', views.NewPositionViewSet,basename="new_postion")

urlpatterns = [
    path('', include(router.urls)),
    path("hr_approve/<int:pk>", views.HRApproval.as_view(), name="hr_approve"),
    path("td_approve/<int:pk>", views.TDApproval.as_view(), name="td_approve"),

]
