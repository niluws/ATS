from django.db import models

class ExcelFileModel(models.Model):
    file = models.FileField(upload_to='excel/')
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

class Question(models.Model):
    text = models.CharField(max_length=150)

class InterviewerScore(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()

class JobinjaProfile(models.Model):
    basic_information=models.OneToOneField(CandidateModel,on_delete=models.CASCADE)
    job = models.CharField(max_length=150,null=True,blank=True)
    last_company=models.CharField(max_length=150,null=True,blank=True)
    education_level=models.CharField(max_length=150,null=True,blank=True)
    province=models.CharField(max_length=150,null=True,blank=True)
    location=models.CharField(max_length=150,null=True,blank=True)
    marital=models.CharField(max_length=150,null=True,blank=True)
    birthdate=models.IntegerField(null=True,blank=True)
    gender=models.CharField(max_length=150,null=True,blank=True)
    military_service_status=models.CharField(max_length=150,null=True,blank=True)
