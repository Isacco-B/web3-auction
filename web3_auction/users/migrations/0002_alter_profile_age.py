# Generated by Django 4.2.5 on 2023-10-09 20:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="age",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]