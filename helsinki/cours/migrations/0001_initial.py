# Generated by Django 4.2.6 on 2023-11-01 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cycle", "0001_initial"),
        ("programme", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cours",
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
                ("nom", models.CharField(max_length=255)),
                ("designation", models.CharField(max_length=255)),
                (
                    "cycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="cycle.cycle"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Prerequis",
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
                (
                    "from_cours",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="from_cours",
                        to="cours.cours",
                    ),
                ),
                (
                    "to_cours",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="to_cours",
                        to="cours.cours",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cours",
            name="prerequis",
            field=models.ManyToManyField(
                blank=True,
                related_name="related_to",
                through="cours.Prerequis",
                to="cours.cours",
            ),
        ),
        migrations.AddField(
            model_name="cours",
            name="programme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="programme.programme"
            ),
        ),
    ]
