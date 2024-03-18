# Generated by Django 5.0.3 on 2024-03-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("translations", "0013_remove_request_responses_response_from_request"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="response",
            name="from_request",
        ),
        migrations.AddField(
            model_name="request",
            name="responses",
            field=models.ManyToManyField(
                blank=True, related_name="request", to="translations.response"
            ),
        ),
    ]
