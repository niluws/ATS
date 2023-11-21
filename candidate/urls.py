from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

app_name='candidate'

router = DefaultRouter()
router.register('', views.AppointmentViewSet)

urlpatterns = [
   path('appointment', include(router.urls)),
   path('candidate_list/',views.CandidateListAPIView.as_view(), name='candidate_list'),
   path('upload_excel/',views.UploadExcelAPIView.as_view(), name='upload_excel'),
   path('score_online_resume/',views.ScoreOnlineResume.as_view(),name='score_online_resume'),
   path('old_candidate/',views.OldCandidateInvitationAPIView.as_view(),name='old_candidate'),
   path('candidate_update/<int:pk>/', views.CandidateUpdateAPIView.as_view(), name='candidate_update'),
   # path('appointment', views.AppointmentViewAPI.as_view(), name='appointment'),
   ]