from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Tenant, Organization, Department, Customer

# Register the Tenant model
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('tenant_id', 'domain')
    search_fields = ('tenant_id', 'domain')

# Register the CustomUser model
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'tenant', 'is_superuser')
    list_filter = ('tenant', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('tenant',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('tenant',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Register the Organization model
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'name')
    search_fields = ('organization_id', 'name')
    filter_horizontal = ('tenants',)

# Register the Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'name', 'organization')
    search_fields = ('department_id', 'name', 'organization__name')

# Register the Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'department')
    search_fields = ('customer_id', 'name', 'department__name')
