# Generated by Django 5.0.3 on 2024-04-20 12:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0020_alter_dictentry_lang"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dictentry",
            name="lang",
        ),
    ]