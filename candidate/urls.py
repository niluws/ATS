from django.urls import path
from . import views

app_name='candidate'


urlpatterns = [
   path('upload_resume/',views.Upload_Resume.as_view(), name='upload_resume'),
   path('candidate_list/',views.CandidateList.as_view(), name='candidate_list'),

]