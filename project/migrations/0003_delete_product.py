# Generated by Django 5.1.3 on 2024-11-15 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_product_carbon"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Product",
        ),
    ]