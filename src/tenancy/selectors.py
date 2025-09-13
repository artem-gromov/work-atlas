from .models import Tenant


def get_tenant_by_domain(domain: str) -> Tenant:
    return Tenant.objects.filter(domain_url=domain).first()

