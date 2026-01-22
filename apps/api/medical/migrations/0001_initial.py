# Generated migration for Patient and Medication models

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Medication",
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
                ("code", models.CharField(max_length=50, unique=True)),
                ("label", models.CharField(max_length=200)),
                (
                    "status",
                    models.CharField(
                        choices=[("actif", "Actif"), ("suppr", "Supprimé")],
                        default="actif",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "ordering": ["label"],
            },
        ),
        migrations.CreateModel(
            name="Patient",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("birth_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[("actif", "Actif"), ("suppr", "Supprimé")],
                        default="actif",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "ordering": ["last_name", "first_name"],
            },
        ),
    ]
