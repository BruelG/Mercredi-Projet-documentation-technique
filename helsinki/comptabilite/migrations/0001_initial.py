# Generated by Django 4.2.6 on 2023-11-15 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cycle", "0001_initial"),
        ("utilisateur", "0004_utilisateur_cycle_utilisateur_programme_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Facture",
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
                ("montant", models.FloatField()),
                (
                    "cycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="cycle.cycle"
                    ),
                ),
                (
                    "etudiant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="utilisateur.utilisateur",
                    ),
                ),
            ],
        ),
    ]
