from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    host(r'admin', 'pydis_site.apps.admin.urls', name="admin"),
    # External API ingress (over the net)
    host(r'api', 'pydis_site.apps.api.urls', name='external_api'),
    # Internal API ingress (cluster local)
    host(r'pydis-api', 'pydis_site.apps.api.urls', name='internal_api'),
    host(r'staff', 'pydis_site.apps.staff.urls', name='staff'),
    host(r'.*', 'pydis_site.apps.home.urls', name=settings.DEFAULT_HOST)
)
