# Generated by Django 5.0.3 on 2024-05-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_alter_loginsession_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="loginsession",
            name="length",
            field=models.DateTimeField(null=True),
        ),
    ]