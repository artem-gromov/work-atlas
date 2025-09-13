from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.indexes import GistIndex


class EmployeeProfile(gis_models.Model):
    user = gis_models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=gis_models.CASCADE)
    title = gis_models.CharField(max_length=255, blank=True)
    location = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)
    city = gis_models.CharField(max_length=255, blank=True)
    country = gis_models.CharField(max_length=255, blank=True)
    bio = gis_models.TextField(blank=True)
    avatar = gis_models.ImageField(upload_to="avatars/", blank=True, null=True)
    precision = gis_models.CharField(
        max_length=8,
        choices=[("EXACT", "EXACT"), ("CITY", "CITY"), ("HIDDEN", "HIDDEN")],
        default="CITY",
    )
    visible = gis_models.BooleanField(default=True)
    is_active = gis_models.BooleanField(default=True)

    class Meta:
        indexes = [GistIndex(fields=["location"])]

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url
        import hashlib

        email = (self.user.email or "").strip().lower().encode("utf-8")
        digest = hashlib.md5(email).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon"

    def delete(
        self, using=None, keep_parents=False
    ):  # pragma: no cover - simple soft delete
        self.is_active = False
        self.save(update_fields=["is_active"])
