from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth import get_user, authenticate
from rest_framework.authentication import TokenAuthentication
from .models import Tenant
from .utils import set_current_tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [
            '/api-token-auth/',
            '/admin/',
        ]
        self.token_auth = TokenAuthentication()

    def __call__(self, request):
        if request.path.startswith('/admin') or request.path.startswith('/api-token-auth'):
            return self.get_response(request)

        user, _ = self.token_auth.authenticate(request)
        if user:
            request.user = user

        if user.is_authenticated:
            if user.is_superuser or user.groups.filter(name='Admin').exists():
                request.tenant = None
                set_current_tenant(None)
                return self.get_response(request)

        tenant = self._get_tenant(request)

        if not tenant:
            return HttpResponseBadRequest("Wrong tenant")

        if user.is_authenticated:
            if user.tenant != tenant:
                return HttpResponseBadRequest("User does not belong to this tenant")
            if tenant.domain != request.get_host().split(':')[0]:
                return HttpResponseBadRequest("Incorrect host for the user")

        request.tenant = tenant
        set_current_tenant(tenant)
        
        response = self.get_response(request)
        set_current_tenant(None)
        return response

    def _get_tenant(self, request):
        host = request.get_host().split(':')[0]
        try:
            return Tenant.objects.get(domain=host)
        except Tenant.DoesNotExist:
            pass

        tenant_domain = request.headers.get('X-Tenant-Domain')
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_domain:
            try:
                return Tenant.objects.get(domain=tenant_domain)
            except Tenant.DoesNotExist:
                pass

        if tenant_id:
            try:
                return Tenant.objects.get(tenant_id=int(tenant_id))
            except (Tenant.DoesNotExist, ValueError):
                pass

        return None
