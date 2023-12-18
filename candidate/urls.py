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
    path('candidate_user_update/<str:pk>/',views.CandidateUserUpdateAPIView.as_view(),name='candidate_user_update'),
    path('candidate_update/<str:pk>/', views.CandidateUpdateAPIView.as_view(), name='candidate_update'),
    path('auto_scheduler/', views.SchedulerAPIView.as_view(), name='auto_scheduler'),
    path('score_new_candidate/', views.NewCandidateScoreAPIView.as_view(), name='score_new_candidate'),
    path('update_pdf_score/<uuid:candidate_id>/', views.PDFScoreAPIView.as_view(), name='update_pdf_score'),
    path('interviewer_scores/<uuid:candidate_id>/', views.InterviewerCandidateScoreAPI.as_view(),
         name='candidate_score_update'),
    path('interviewer_scores/', views.InterviewerAllScoresAPI.as_view(), name='interviewer_scores'),
    path('update_interviewer_scores/<int:pk>/', views.UpdateInterviewerCandidateScoreAPI.as_view(),
         name='update_interviewer_scores'),
    path('candidate_all_interviewer_score/<uuid:candidate_id>/', views.CandidateAllInterviewerScoreAPI.as_view(),
         name='candidate_all_interviewer_score'),
    path('interview_done/<uuid:candidate_id>/', views.InterviewDoneAPIView.as_view(), name='interview_done'),
    path('score_history/<uuid:candidate_id>/', views.HistoryScoreAPI.as_view(), name='score_history'),
]
