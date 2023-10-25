from django.db import models
from django.utils import timezone
from authentication.models import Profile
from job.models import Job


class NewPositionModel(models.Model):
    CONTRACT_TYPE_CHOICES = (
        ("FULL-TIME", "Full-time"),
        ("PART-TIME", "Part-time"),
    )
    STATUS_CHOICES = (
        ("APPROVED", "Approved"),
        ("PENDING", "Pending"),
    )
    REASON_CHOICES = (
        ("NEW-ROLE", "New role"),
        ("REPLACE", "Replace"),
    )
    EDUCATION_LEVEL_CHOICES = (
        ("DIPLOMA", "Diploma"),
        ("BACHELOR", "Bachelor"),
        ("MASTER", "Master"),
        ("DOCTORAL", "Doctoral"),
    )
    EXPERIENCE_LEVEL_CHOICES = (
        ("INTERNSHIP", "Internship"),
        ("JUNIOR", "Junior"),
        ("MID-LEVEL", "Mid-level"),
        ("SENIOR", "Senior"),
    )
    DEPARTMENT_CHOICES = (
        ("HR", "HR"),
        ("ML", "ML"),
        ("VOLLABOR", "Vollabor"),
        ("VISERA", "Visera"),
    )
    create_at = models.DateTimeField(default=timezone.now)
    position_title = models.OneToOneField(Job, on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=9, choices=CONTRACT_TYPE_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, null=True, blank=True)
    reason = models.CharField(max_length=8, choices=REASON_CHOICES)
    education_level = models.CharField(max_length=8, default='BACHELOR', choices=EDUCATION_LEVEL_CHOICES)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES)
    department = models.CharField(max_length=8, choices=DEPARTMENT_CHOICES)
    quantity = models.IntegerField()
    explanation = models.TextField(null=True, blank=True)
    hr_approval = models.BooleanField(null=True, blank=True)
    td_approval = models.BooleanField(null=True, blank=True)
    budget = models.BigIntegerField()

    # def save(self, *args, **kwargs):
    #     if self.hr_approval == True:
    #         td_users = Profile.objects.filter(role__title='TD', department=self.department)
    #         user_ids = [user.user.id for user in td_users]
    #
    #         Profile.assign = user_ids
    #         self.save()

    class Meta:
        verbose_name = 'new position'
        verbose_name_plural = 'new positions'
