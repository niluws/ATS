# Generated by Django 4.2.6 on 2023-11-18 13:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0005_alter_requirement_en_title_and_more"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="profile",
            unique_together={("role", "department")},
        ),
    ]
