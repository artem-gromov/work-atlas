from django.conf import settings
from django.contrib.gis.db import models as gis_models


class EmployeeProfile(gis_models.Model):
    user = gis_models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=gis_models.CASCADE)
    title = gis_models.CharField(max_length=255, blank=True)
    location = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)
    city = gis_models.CharField(max_length=255, blank=True)
    country = gis_models.CharField(max_length=255, blank=True)
    precision = gis_models.CharField(
        max_length=8,
        choices=[("EXACT", "EXACT"), ("CITY", "CITY"), ("HIDDEN", "HIDDEN")],
        default="CITY",
    )
    visible = gis_models.BooleanField(default=True)

    class Meta:
        indexes = [gis_models.GiSTIndex(fields=["location"])]

