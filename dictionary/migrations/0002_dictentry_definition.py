# Generated by Django 5.0.3 on 2024-03-19 09:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dictentry",
            name="definition",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
