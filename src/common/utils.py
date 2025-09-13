"""Common helper utilities."""

from typing import Any


def get_client_ip(request: Any) -> str:
    """Return client IP address from request."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")

