# Generated by Django 4.1.7 on 2023-05-04 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Massages",
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
                ("massages", models.CharField(blank=True, max_length=5000, null=True)),
                ("time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
