# Generated by Django 4.2.6 on 2023-11-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("candidate", "0010_settingsmodel_interview_duration_hours_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="settingsmodel",
            name="end_work_time",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="settingsmodel",
            name="start_work_time",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
