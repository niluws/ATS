from django.db import models


class Role(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=150)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class Skill(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
