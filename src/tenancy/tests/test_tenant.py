import pytest

from tenancy.models import Tenant


@pytest.mark.django_db
def test_tenant_creation():
    tenant = Tenant.objects.create(schema_name="acme", name="Acme", domain_url="acme.app.local")
    assert tenant.schema_name == "acme"

