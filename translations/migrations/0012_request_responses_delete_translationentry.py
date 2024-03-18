# Generated by Django 5.0.3 on 2024-03-18 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("translations", "0011_remove_translationentry_target_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="responses",
            field=models.ManyToManyField(
                blank=True,
                related_name="translation_entries",
                to="translations.response",
            ),
        ),
        migrations.DeleteModel(
            name="TranslationEntry",
        ),
    ]
