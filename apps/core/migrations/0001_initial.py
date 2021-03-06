# Generated by Django 3.2.9 on 2021-12-03 15:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=50)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                (
                    "team_money",
                    models.FloatField(
                        default=5000000,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Player",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                (
                    "age",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(18),
                            django.core.validators.MaxValueValidator(40),
                        ]
                    ),
                ),
                (
                    "market_value",
                    models.FloatField(
                        default=1000000,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("Goalkeeper", "Goalkeeper"),
                            ("Defender", "Defender"),
                            ("Midfielder", "Midfielder"),
                            ("Attacker", "Attacker"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.team"
                    ),
                ),
            ],
        ),
    ]
