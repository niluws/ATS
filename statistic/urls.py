from django.urls import path

from . import views

app_name = 'statistic'

urlpatterns = [
    path('candidate_status/', views.CandidateStatusAPIView.as_view(), name='candidate_status'),
    path('candidate_job/', views.CandidateJobStatisticAPIView.as_view(), name='candidate_job'),
]