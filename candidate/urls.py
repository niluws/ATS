from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'candidate'

router = DefaultRouter()
router.register(r'appointment', views.AppointmentViewSet)
router.register(r'settings', views.SettingsViewSet)
router.register(r'interview_settings', views.InterviewSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('candidate_list/', views.CandidateListAPIView.as_view(), name='candidate_list'),
    path('upload_excel/', views.UploadExcelAPIView.as_view(), name='upload_excel'),
    path('invite_old_candidate/', views.OldCandidateInvitationAPIView.as_view(), name='old_candidate'),
    path('candidate_update/<str:pk>/', views.CandidateUpdateAPIView.as_view(), name='candidate_update'),
    path('auto_scheduler/', views.SchedulerAPIView.as_view(), name='auto_scheduler'),
    path('score_new_candidate/', views.NewCandidateScoreAPIView.as_view(), name='score_new_candidate'),
    path('pdf_score/<uuid:candidate_id>/', views.PDFScoreAPIView.as_view(), name='pdf_score'),
    path('interviewer_scores/<uuid:candidate_id>/', views.InterviewerCandidateScoreAPI.as_view(), name='candidate_score_update'),
    path('interviewer_scores/', views.InterviewerAllScoresAPI.as_view(), name='all_candidates_scores'),
    path('interviewer_scores/<int:pk>', views.UpdateInterviewerCandidateScoreAPI.as_view(), name='update_interviewer_scores'),
]
