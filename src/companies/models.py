from django.db import models

from tenancy.models import Tenant


class Company(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    privacy_policy = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.display_name
