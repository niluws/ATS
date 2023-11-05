from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'job'

router = DefaultRouter()
router.register('', views.JobViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
