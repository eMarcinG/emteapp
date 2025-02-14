from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from .models import Tenant, Organization, Department, Customer
from .serializers import TenantSerializer, OrganizationSerializer, DepartmentSerializer, CustomerSerializer

class IsAdminOrSuperuser(BasePermission):
    """
    Allows editing only by superusers or users belonging to the "Admin" group..
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Admin').exists()
        )

class TenantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    serializer_class = TenantSerializer

    def get_queryset(self):
        # Only current tenant
        return Tenant.objects.filter(pk=self.request.tenant.pk)

class OrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        # Filter by tenant
        return Organization.objects.filter(tenants=self.request.tenant)

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        # Filter by tenant organization
        return Department.objects.filter(organization__tenants=self.request.tenant)

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        # Filter by department - organization tenant
        return Customer.objects.filter(
            department__organization__tenants=self.request.tenant
        )