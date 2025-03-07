from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    """
    Represents a tenant with a unique identifier and domain.
    
    Attributes:
        tenant_id (int): The primary key of the tenant.
        domain (str): The domain of the tenant.
    """
    tenant_id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain

class CustomUser(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Organization(models.Model):
    """
    Represents an organization belonging to a tenant.
    
    Attributes:
        organization_id (int): The primary key of the organization.
        name (str): The name of the organization.
        tenants (ManyToManyField): The tenants to which the organization belongs.
    """
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    tenants = models.ManyToManyField(Tenant, related_name='organizations')

    def __str__(self):
        return self.name

class Department(models.Model):
    """
    Represents a department within an organization.
    
    Attributes:
        department_id (int): The primary key of the department.
        name (str): The name of the department.
        organization (ForeignKey): The organization to which the department belongs.
    """
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, related_name='departments', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'organization')

    def __str__(self):
        return self.name

class Customer(models.Model):
    """
    Represents a customer belonging to a department.
    
    Attributes:
        customer_id (int): The primary key of the customer.
        name (str): The name of the customer.
        department (ForeignKey): The department to which the customer belongs.
    """
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='customers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
