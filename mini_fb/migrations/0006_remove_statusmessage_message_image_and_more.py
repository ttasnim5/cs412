# Generated by Django 5.1.2 on 2024-10-19 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0005_rename_profile_image_message_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="statusmessage",
            name="message_image",
        ),
        migrations.AlterField(
            model_name="image",
            name="image_file",
            field=models.ImageField(upload_to=""),
        ),
    ]
