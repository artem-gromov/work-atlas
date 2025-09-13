import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db
def test_email_verification_marks_user_verified():
    client = APIClient()
    client.post(
        reverse("api-v1:register"),
        {"email": "verify@example.com", "password": "pwd"},
        format="json",
    )
    user = User.objects.get(email="verify@example.com")
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    resp = client.get(reverse("api-v1:auth-verify"), {"uid": uid, "token": token})
    assert resp.status_code == 200
    user.refresh_from_db()
    assert user.is_email_verified is True
