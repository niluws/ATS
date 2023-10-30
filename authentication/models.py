from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from job.models import Job, Role


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=False, )
    is_superuser = models.BooleanField(default=False, )
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'



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
