# Generated by Django 5.0.3 on 2024-05-05 12:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0027_alter_attribute_classification_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attribute",
            name="source",
        ),
    ]
