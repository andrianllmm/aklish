# Generated by Django 5.0.3 on 2024-03-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_profile_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(null=True),
        ),
    ]
