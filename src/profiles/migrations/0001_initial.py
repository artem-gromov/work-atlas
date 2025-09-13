import django.contrib.gis.db.models.fields
from django.conf import settings
from django.contrib.postgres.indexes import GistIndex
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        CreateExtension("postgis"),
        migrations.CreateModel(
            name="EmployeeProfile",
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
                ("title", models.CharField(blank=True, max_length=255)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, geography=True, null=True, srid=4326
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=255)),
                ("country", models.CharField(blank=True, max_length=255)),
                ("bio", models.TextField(blank=True)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars/"),
                ),
                (
                    "precision",
                    models.CharField(
                        choices=[
                            ("EXACT", "EXACT"),
                            ("CITY", "CITY"),
                            ("HIDDEN", "HIDDEN"),
                        ],
                        default="CITY",
                        max_length=8,
                    ),
                ),
                ("visible", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={},
        ),
        migrations.AddIndex(
            model_name="employeeprofile",
            index=GistIndex(fields=["location"], name="profiles_location_gist"),
        ),
    ]
