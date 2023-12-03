from django.db import models

from authentication.models import User


class Role(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Requirement(models.Model):
    en_title = models.CharField(max_length=150, unique=True)
    fa_title = models.CharField(max_length=150, unique=True)
    score = models.IntegerField()

    def __str__(self):
        return self.en_title


class JobRequirement(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)


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
    create_at = models.DateTimeField(auto_now_add=True)
    position_title = models.OneToOneField(Job, on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=9, choices=CONTRACT_TYPE_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, null=True, blank=True)
    reason = models.CharField(max_length=8, choices=REASON_CHOICES)
    education_level = models.CharField(max_length=8, default='BACHELOR', choices=EDUCATION_LEVEL_CHOICES)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES)
    department = models.CharField(max_length=8, choices=DEPARTMENT_CHOICES)
    quantity = models.IntegerField()
    explanation = models.TextField(null=True, blank=True)
    hr_approval = models.BooleanField(default=False)
    td_approval = models.BooleanField(default=False)
    budget = models.BigIntegerField()
    assigned_to_td = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='assigned_to_td_set')
    interviewer = models.ManyToManyField(User, null=True, blank=True)
    is_advertised = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.hr_approval:
            td_user = User.objects.filter(profile__role__title='TD', profile__department=self.department).first()
            if td_user:
                self.assigned_to_td = td_user
        else:
            self.assigned_to_td = None

        super(NewPositionModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'new position'
        verbose_name_plural = 'new positions'
