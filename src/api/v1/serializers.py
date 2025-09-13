import math
import random

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import serializers

from companies.models import Company
from profiles.models import EmployeeProfile
from tenancy.models import Tenant


class TenantCreateSerializer(serializers.ModelSerializer):
    admin_email = serializers.EmailField(write_only=True)
    admin_password = serializers.CharField(write_only=True)

    class Meta:
        model = Tenant
        fields = ["name", "domain_url", "schema_name", "admin_email", "admin_password"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ReadOnlyField()

    class Meta:
        model = EmployeeProfile
        fields = [
            "id",
            "user",
            "title",
            "bio",
            "location",
            "city",
            "country",
            "precision",
            "visible",
            "is_active",
            "avatar",
            "avatar_url",
        ]
        read_only_fields = ["user", "avatar_url"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.visible:
            return {"id": instance.id}
        if "location" in data and instance.location:
            if instance.precision == "HIDDEN":
                # Hide exact coordinates completely
                data.pop("location")
            elif instance.precision == "CITY":
                # Randomize coordinates within a 5 km radius
                radius_km = 5
                distance = random.uniform(0, radius_km)
                angle = random.uniform(0, 2 * math.pi)
                delta_lat = (distance / 111) * math.cos(angle)
                delta_lon = (
                    (distance / 111) * math.sin(angle) / math.cos(math.radians(instance.location.y))
                )
                point = Point(
                    instance.location.x + delta_lon,
                    instance.location.y + delta_lat,
                )
                data["location"] = {
                    "type": "Point",
                    "coordinates": [point.x, point.y],
                }
        return data


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["display_name", "logo", "privacy_policy"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        EmployeeProfile.objects.create(user=user)
        return user
