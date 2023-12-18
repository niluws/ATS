from django.urls import path

from . import views

app_name = 'statistic'

urlpatterns = [
    path('candidate_status/', views.CandidateStatusAPIView.as_view(), name='candidate_status'),
    path('candidate_statistic/', views.CandidateStatisticsAPIView.as_view(), name='candidate_statistic'),
]