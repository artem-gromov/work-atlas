from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CompanyView, ProfileViewSet, TenantCreateAPIView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")

urlpatterns = [
    path("tenants/", TenantCreateAPIView.as_view()),
    path("company/", CompanyView.as_view()),
] + router.urls

