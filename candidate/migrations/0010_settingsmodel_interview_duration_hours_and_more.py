# Generated by Django 4.2.6 on 2023-11-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("candidate", "0009_rename_settings_settingsmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="settingsmodel",
            name="interview_duration_hours",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="settingsmodel",
            name="pass_score",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]