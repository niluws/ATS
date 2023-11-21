from django.db import models
from django.contrib.postgres.fields import ArrayField
from jdatetime import datetime as jdatetime

class CandidateModel(models.Model):
    name = models.CharField(max_length=150)
    job = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    score = models.IntegerField(null=True,blank=True)
    request_date= models.CharField(max_length=15)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    last_company=models.CharField(max_length=150,null=True,blank=True)
    education_level=models.CharField(max_length=150,null=True,blank=True)
    province=models.CharField(max_length=150,null=True,blank=True)
    location=models.CharField(max_length=150,null=True,blank=True)
    marital=models.CharField(max_length=150,null=True,blank=True)
    birthdate=models.CharField(max_length=150,null=True,blank=True)
    gender=models.CharField(max_length=150,null=True,blank=True)
    military_service_status=models.CharField(max_length=150,null=True,blank=True)
    job_status=models.CharField(max_length=150,null=True,blank=True)
    skills= ArrayField(models.CharField(max_length=150), null=True, blank=True)
    languages=ArrayField(models.CharField(max_length=150), null=True, blank=True)
    about=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class ExperiencesModel(models.Model):
    candidate=models.ForeignKey(CandidateModel,on_delete=models.CASCADE)
    title=models.CharField(max_length=150,null=True,blank=True)
    company=models.CharField(max_length=150,null=True,blank=True)
    start_at=models.CharField(max_length=150,null=True,blank=True)
    end_at=models.CharField(max_length=150,null=True,blank=True)
    duration=models.CharField(max_length=150,null=True,blank=True)

class PreferencesModel(models.Model):
    candidate=models.OneToOneField(CandidateModel,on_delete=models.CASCADE)
    proviences=ArrayField(models.CharField(max_length=150), null=True, blank=True)
    job_category=ArrayField(models.CharField(max_length=150), null=True, blank=True)
    job_level=models.CharField(max_length=150, null=True, blank=True)
    contracts_type=ArrayField(models.CharField(max_length=150), null=True, blank=True)
    salary=models.CharField(max_length=150, null=True, blank=True)
    benefits=ArrayField(models.CharField(max_length=150), null=True, blank=True)


class EducationModel(models.Model):
    candidate=models.ForeignKey(CandidateModel,on_delete=models.CASCADE)
    level=models.CharField(max_length=150, null=True, blank=True)
    major=models.CharField(max_length=150, null=True, blank=True)
    university=models.CharField(max_length=150, null=True, blank=True)
    duration=models.CharField(max_length=150, null=True, blank=True)

class QuestionModel(models.Model):
    text = models.CharField(max_length=150)

class InterviewerScoreModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    score = models.IntegerField()


class AppointmentModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    interview_start_time = models.DateTimeField( null=True, blank=True)
    interview_end_time = models.DateTimeField( null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.candidate.name} - {self.interview_start_time}"
    