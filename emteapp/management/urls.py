from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .viewsets import TenantViewSet, OrganizationViewSet, DepartmentViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
