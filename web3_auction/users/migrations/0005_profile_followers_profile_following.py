# Generated by Django 4.2.5 on 2023-10-06 19:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_profile_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="followers",
            field=models.ManyToManyField(blank=True, related_name="following", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="profile",
            name="following",
            field=models.ManyToManyField(blank=True, related_name="followers", to=settings.AUTH_USER_MODEL),
        ),
    ]
