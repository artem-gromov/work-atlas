from django.db import models

from tenancy.models import Tenant


class Company(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self) -> str:
        return self.brand_name

