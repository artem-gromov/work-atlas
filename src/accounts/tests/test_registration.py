import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db
def test_register_returns_tokens():
    client = APIClient()
    resp = client.post(
        reverse("api-v1:register"),
        {"email": "test@example.com", "password": "pass123"},
        format="json",
    )
    assert resp.status_code == 201
    assert "access" in resp.data
    assert User.objects.filter(email="test@example.com").exists()
