# Generated by Django 5.0.5 on 2024-08-09 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("translate", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Origin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=5, null=True, unique=True)),
                ("meaning", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Classification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=5, unique=True)),
                ("meaning", models.CharField(max_length=64)),
            ],
            options={
                "unique_together": {("code", "meaning")},
            },
        ),
        migrations.CreateModel(
            name="Attribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("definition", models.TextField()),
                (
                    "examples",
                    models.ManyToManyField(
                        blank=True, related_name="example_of", to="translate.entry"
                    ),
                ),
                (
                    "classification",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="attributes",
                        to="dictionary.classification",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DictEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("word", models.CharField(max_length=100)),
                ("last_selected", models.DateField(blank=True, null=True)),
                (
                    "attributes",
                    models.ManyToManyField(
                        blank=True, related_name="entry", to="dictionary.attribute"
                    ),
                ),
                (
                    "lang",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dict_entries",
                        to="translate.language",
                    ),
                ),
            ],
            options={
                "unique_together": {("word", "lang")},
            },
        ),
        migrations.AddField(
            model_name="attribute",
            name="opposite",
            field=models.ManyToManyField(
                blank=True, related_name="opposite", to="dictionary.dictentry"
            ),
        ),
        migrations.AddField(
            model_name="attribute",
            name="similar",
            field=models.ManyToManyField(
                blank=True, related_name="similar", to="dictionary.dictentry"
            ),
        ),
        migrations.AddField(
            model_name="attribute",
            name="origin",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="attributes",
                to="dictionary.origin",
            ),
        ),
        migrations.CreateModel(
            name="PartsOfSpeech",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=10, unique=True)),
                ("meaning", models.CharField(max_length=64)),
            ],
            options={
                "unique_together": {("code", "meaning")},
            },
        ),
        migrations.AddField(
            model_name="attribute",
            name="pos",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="attributes",
                to="dictionary.partsofspeech",
            ),
        ),
        migrations.AddField(
            model_name="attribute",
            name="sources",
            field=models.ManyToManyField(
                blank=True, related_name="attributes", to="dictionary.source"
            ),
        ),
    ]
