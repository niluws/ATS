# Generated by Django 4.2.6 on 2023-10-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inbox", "0007_remove_newpositionmodel_interviewer_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="newpositionmodel",
            name="is_applied",
            field=models.BooleanField(default=False),
        ),
    ]
