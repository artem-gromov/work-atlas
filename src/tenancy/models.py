from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=255, unique=True)
    domain_url = models.CharField(max_length=253, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    paid_plan = models.CharField(
        max_length=16,
        choices=[("FREE", "FREE"), ("PRO", "PRO")],
        default="FREE",
    )

    auto_create_schema = True


class Domain(DomainMixin):
    pass

