from django.conf import settings


def tenant_from_request(request) -> str:
    host = request.get_host().split(":")[0]
    suffix = getattr(settings, "TENANT_DEFAULT_DOMAIN_SUFFIX", "")
    if suffix and host.endswith(suffix):
        return host[:- len(suffix)]
    return host.split(".")[0]

