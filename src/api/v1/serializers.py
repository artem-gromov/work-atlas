from django.contrib.auth import get_user_model
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
        if instance.precision in {"HIDDEN", "CITY"} and "location" in data:
            # Hide exact coordinates unless precision explicitly set to EXACT
            data.pop("location")
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
