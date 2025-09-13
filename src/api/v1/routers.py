from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    CompanyView,
    EmployeeImportAPIView,
    ProfileViewSet,
    RegisterAPIView,
    TenantCreateAPIView,
    VerifyEmailAPIView,
)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profile")

app_name = "api-v1"

urlpatterns = [
    path("tenants/", TenantCreateAPIView.as_view(), name="tenants"),
    path("company/", CompanyView.as_view(), name="company"),
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/verify/", VerifyEmailAPIView.as_view(), name="auth-verify"),
    path("auth/jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("employees/import/", EmployeeImportAPIView.as_view(), name="employees-import"),
] + router.urls
