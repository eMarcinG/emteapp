from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tenant, Organization, Department, Customer
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class TenantTestCase(TestCase):
    """
    Test case for the multi-tenant management system.
    """

    def setUp(self):
        """
        Set up the initial state for the tests.
        Creates two tenants, a user, and sets up the API client with authentication.
        """
        self.tenant1 = Tenant.objects.create(domain='tenant1.com')
        self.tenant2 = Tenant.objects.create(domain='tenant2.com')

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_tenant_creation(self):
        """
        Test the creation of tenants.
        """
        self.assertEqual(Tenant.objects.count(), 2)

    def test_get_tenants(self):
        """
        Test retrieving tenants for a specific domain.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key, HTTP_HOST='tenant1.com')
        response = self.client.get('/api/tenants/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Tenant.objects.filter(domain="tenant1.com").count())

    def test_get_organizations_for_tenant(self):
        """
        Test retrieving organizations for specific tenants.
        """
        org1 = Organization.objects.create(name='Org1')
        org1.tenants.add(self.tenant1)
        org2 = Organization.objects.create(name='Org2')
        org2.tenants.add(self.tenant2)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key, HTTP_HOST='tenant1.com')
        response = self.client.get('/api/organizations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Org1')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key, HTTP_HOST='tenant2.com')
        response = self.client.get('/api/organizations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Org2')

    def test_organization_creation(self):
        """
        Test the creation of organizations for specific tenants.
        """
        org1 = Organization.objects.create(name='Org1')
        org1.tenants.add(self.tenant1)
        org2 = Organization.objects.create(name='Org2')
        org2.tenants.add(self.tenant2)
        self.assertEqual(Organization.objects.count(), 2)

    def test_department_creation(self):
        """
        Test the creation of departments for specific organizations.
        """
        org = Organization.objects.create(name='Org1')
        org.tenants.add(self.tenant1)
        dept = Department.objects.create(name='Dept1', organization=org)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(dept.organization, org)

    def test_customer_creation(self):
        """
        Test the creation of customers for specific departments.
        """
        org = Organization.objects.create(name='Org1')
        org.tenants.add(self.tenant1)
        dept = Department.objects.create(name='Dept1', organization=org)
        customer = Customer.objects.create(name='Customer1', department=dept)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(customer.department, dept)
