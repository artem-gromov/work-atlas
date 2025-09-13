import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from profiles.models import EmployeeProfile


@pytest.mark.django_db
def test_profile_filter_by_city():
    user = User.objects.create_user(email="a@b.com", password="pwd")
    EmployeeProfile.objects.create(user=user, city="NY")
    client = APIClient()
    client.force_authenticate(user=user)
    resp = client.get(reverse("api-v1:profile-list"), {"city": "NY"})
    assert resp.status_code == 200
    assert len(resp.data) == 1
