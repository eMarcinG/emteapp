from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tenant, Organization, Department, Customer
from .serializers import TenantSerializer, OrganizationSerializer, DepartmentSerializer, CustomerSerializer

class TenantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
