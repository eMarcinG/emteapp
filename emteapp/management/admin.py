from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Tenant

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'tenant')
    list_filter = ('tenant',)
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('tenant',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('tenant',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tenant)
