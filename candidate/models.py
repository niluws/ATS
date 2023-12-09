import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from authentication.models import User
from job.models import Job, QuestionsModel


class SettingsModel(models.Model):
    start_work_time = models.IntegerField(null=True, blank=True)
    end_work_time = models.IntegerField(null=True, blank=True)


class InterviewSettingsModel(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    settings = models.ForeignKey(SettingsModel, on_delete=models.CASCADE)
    interview_duration_minutes = models.IntegerField(null=True, blank=True)
    pass_score = models.IntegerField(null=True, blank=True)


class CandidateModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    job = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    request_date = models.CharField(max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    last_company = models.CharField(max_length=150, null=True, blank=True)
    education_level = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    marital = models.CharField(max_length=150, null=True, blank=True)
    birthdate = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=150, null=True, blank=True)
    military_service_status = models.CharField(max_length=150, null=True, blank=True)
    job_status = models.CharField(max_length=150, null=True, blank=True)
    skills = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    languages = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    candidate_approval = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name


class ScoreModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    auto_score = models.IntegerField(null=True, blank=True)
    pdf_score = models.IntegerField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExperiencesModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=True, blank=True)
    company = models.CharField(max_length=150, null=True, blank=True)
    start_at = models.CharField(max_length=150, null=True, blank=True)
    end_at = models.CharField(max_length=150, null=True, blank=True)
    duration = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.candidate.name


class PreferencesModel(models.Model):
    candidate = models.OneToOneField(CandidateModel, on_delete=models.CASCADE)
    proviences = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    job_category = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    job_level = models.CharField(max_length=150, null=True, blank=True)
    contracts_type = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    salary = models.CharField(max_length=150, null=True, blank=True)
    benefits = ArrayField(models.CharField(max_length=150), null=True, blank=True)


class EducationModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    level = models.CharField(max_length=150, null=True, blank=True)
    major = models.CharField(max_length=150, null=True, blank=True)
    university = models.CharField(max_length=150, null=True, blank=True)
    duration = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.candidate.name


class AppointmentModel(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    interview_start_time = models.DateTimeField(null=True, blank=True)
    interview_end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.interview_start_time}"


class StatusModel(models.Model):
    STATUS_CHOICES = (
        ("WI", "Waiting for interview"),
        ("R", "Rejected"),
        ("H", "Hired"),
    )
    candidate = models.OneToOneField(CandidateModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class InterviewerScore(models.Model):
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionsModel, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
