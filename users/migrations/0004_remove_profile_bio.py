# Generated by Django 5.0.3 on 2024-03-26 15:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_profile_bio"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="bio",
        ),
    ]
