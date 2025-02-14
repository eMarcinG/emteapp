import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from management.models import Tenant, Organization, Department, Customer  

class Command(BaseCommand):
    help = 'Creates test users with proper permissions for all models'

    def handle(self, *args, **options):
        if not settings.DEBUG or os.getenv('DJANGO_ENV') == 'production':
            self.stdout.write(self.style.WARNING('Skipping test users creation in production'))
            return

        models = [Tenant, Organization, Department, Customer]
        
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        readonly_group, _ = Group.objects.get_or_create(name='ReadOnly')

        admin_permissions = []
        readonly_permissions = []

        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            
            admin_permissions.extend(Permission.objects.filter(content_type=content_type))
            
            view_permission = Permission.objects.get(
                content_type=content_type,
                codename=f'view_{model._meta.model_name}'
            )
            readonly_permissions.append(view_permission)

        admin_group.permissions.set(admin_permissions)
        readonly_group.permissions.set(readonly_permissions)

        admin_user = User.objects.create_user(
            username='adminuser',
            password=os.getenv("ADMIN_PASSWORD", "adminpass"),
            is_staff=True
        )
        admin_user.groups.add(admin_group)

        readonly_user = User.objects.create_user(
            username='readonlyuser',
            password=os.getenv("READONLY_PASSWORD", "readonlypass"),
            is_staff=False
        )
        readonly_user.groups.add(readonly_group)

        self.stdout.write(self.style.SUCCESS('Successfully created test users with permissions'))