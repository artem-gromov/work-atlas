import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from companies.models import Company
from tenancy.models import Tenant


@pytest.mark.django_db
def test_tenant_admin_can_update_company():
    tenant = Tenant.objects.create(
        schema_name="acme", name="Acme", domain_url="acme.local"
    )
    company = Company.objects.create(tenant=tenant, display_name="Old")
    admin = User.objects.create_user(email="admin@example.com", password="pwd")
    group, _ = Group.objects.get_or_create(name="TENANT_ADMIN")
    admin.groups.add(group)
    client = APIClient()
    client.force_authenticate(user=admin)
    url = reverse("api-v1:company")
    resp = client.patch(
        url, {"display_name": "New"}, format="json", HTTP_HOST=tenant.domain_url
    )
    assert resp.status_code == 200
    company.refresh_from_db()
    assert company.display_name == "New"


@pytest.mark.django_db
def test_regular_user_cannot_update_company():
    tenant = Tenant.objects.create(
        schema_name="acme", name="Acme", domain_url="acme.local"
    )
    company = Company.objects.create(tenant=tenant, display_name="Old")
    user = User.objects.create_user(email="user@example.com", password="pwd")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("api-v1:company")
    resp = client.patch(
        url, {"display_name": "New"}, format="json", HTTP_HOST=tenant.domain_url
    )
    assert resp.status_code == 403
    company.refresh_from_db()
    assert company.display_name == "Old"
