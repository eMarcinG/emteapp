from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth import get_user
from .models import Tenant
from .utils import set_current_tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [
            '/api-token-auth/',
            '/admin/',
        ]

    def __call__(self, request):
        if request.path.startswith('/admin') or request.path.startswith('/api-token-auth'):
            return self.get_response(request)

        user = get_user(request)

        if user.is_authenticated and user.is_superuser:
            return self.get_response(request)

        tenant = self._get_tenant(request)
        
        if not tenant:
            return HttpResponseBadRequest("Wrong tenant")

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
