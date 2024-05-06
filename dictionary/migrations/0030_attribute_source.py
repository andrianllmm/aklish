# Generated by Django 5.0.3 on 2024-05-05 12:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0029_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="attribute",
            name="source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="attributes",
                to="dictionary.source",
            ),
        ),
    ]
