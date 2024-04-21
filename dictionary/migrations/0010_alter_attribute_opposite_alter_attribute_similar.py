# Generated by Django 5.0.3 on 2024-04-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0009_attribute_opposite_attribute_similar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attribute",
            name="opposite",
            field=models.ManyToManyField(
                related_name="opposite", to="dictionary.dictentry"
            ),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="similar",
            field=models.ManyToManyField(
                related_name="similar", to="dictionary.dictentry"
            ),
        ),
    ]
