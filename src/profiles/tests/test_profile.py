import pytest
from django.contrib.gis.geos import Point

from accounts.models import User
from profiles.models import EmployeeProfile


@pytest.mark.django_db
def test_profile_creation():
    user = User.objects.create_user(username="john", password="pwd")
    profile = EmployeeProfile.objects.create(user=user, city="NY", location=Point(0, 0))
    assert profile.user.username == "john"

