from django.db import models

class ExceFileModel(models.Model):
    file = models.FileField(upload_to='excel/')
class CandidateModel(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    request_date= models.CharField(max_length=100)
    link= models.CharField(max_length=300)
    resume = models.FileField(upload_to='resumes/',null=True,blank=True)
