# Generated by Django 4.2.6 on 2023-10-30 12:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inbox", "0008_newpositionmodel_is_applied"),
    ]

    operations = [
        migrations.RenameField(
            model_name="newpositionmodel",
            old_name="is_applied",
            new_name="is_advertised",
        ),
    ]
