# Generated by Django 5.1.2 on 2024-11-08 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Voter",
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
                ("voter_id", models.TextField()),
                ("last_name", models.TextField()),
                ("first_name", models.TextField()),
                ("street_num", models.IntegerField()),
                ("street_name", models.TextField()),
                ("apt_num", models.CharField(default="", max_length=6)),
                ("zip_code", models.IntegerField()),
                ("date_of_birth", models.DateField()),
                ("date_of_reg", models.DateField()),
                ("party", models.TextField()),
                ("precinct_num", models.IntegerField()),
                ("v20state", models.BooleanField(default=False)),
                ("v21town", models.BooleanField(default=False)),
                ("v21primary", models.BooleanField(default=False)),
                ("v22general", models.BooleanField(default=False)),
                ("v23town", models.BooleanField(default=False)),
                ("voterscore", models.IntegerField()),
            ],
        ),
    ]