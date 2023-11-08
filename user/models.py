from django.db import models
from job.models import Job, Role
from authentication.models import User
class Profile(models.Model):
    EDUCATION_CHOICES = (
        ("DIPLOMA", "Diploma"),
        ("BACHELORS", "Bachelor's Degree"),
        ("MASTERS", "Master's Degree"),
        ("DOCTORATE", "Doctorate"),
    )
    DEPARTMENT_CHOICES = (
        ("HR", "HR"),
        ("ML", "ML"),
        ("VOLLABOR", "Vollabor"),
        ("VISERA", "Visera"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    education = models.CharField(max_length=9, choices=EDUCATION_CHOICES, default="", null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=8, choices=DEPARTMENT_CHOICES, null=True, blank=True)

