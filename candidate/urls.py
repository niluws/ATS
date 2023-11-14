from django.urls import path
from . import views

app_name='candidate'


urlpatterns = [
   path('candidate_list/',views.CandidateListAPIView.as_view(), name='candidate_list'),
   path('upload_excel/',views.UploadExcelAPIView.as_view(), name='upload_excel'),
   path('score_online_resume/',views.ScoreOnlineResume.as_view(),name='score_online_resume')
]