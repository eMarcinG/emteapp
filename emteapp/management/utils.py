import threading

_tenant_local = threading.local()

def get_current_tenant():
    return getattr(_tenant_local, 'tenant', None)

def set_current_tenant(tenant):
    _tenant_local.tenant = tenant