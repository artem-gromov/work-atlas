from .models import Tenant


def create_tenant(name: str, schema: str, domain: str) -> Tenant:
    tenant = Tenant(schema_name=schema, name=name, domain_url=domain)
    tenant.save()
    return tenant

