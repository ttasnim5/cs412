# Generated by Django 5.1.3 on 2024-11-21 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0008_product_causes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="brand_name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="brand",
            name="help_causes",
            field=models.ManyToManyField(blank=True, to="project.cause"),
        ),
        migrations.AlterField(
            model_name="brand",
            name="product_categories",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name="product",
            name="brands",
        ),
        migrations.AddField(
            model_name="product",
            name="brands",
            field=models.ManyToManyField(related_name="products", to="project.brand"),
        ),
    ]
