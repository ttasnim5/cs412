# Generated by Django 5.1.3 on 2024-11-15 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="carbon",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]