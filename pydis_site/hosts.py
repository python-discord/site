from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    host(r'admin', 'pydis_site.apps.admin.urls', name="admin"),
    host(r'api', 'pydis_site.apps.api.urls', name='api'),
    host(r'staff', 'pydis_site.apps.staff.urls', name='staff'),
    host(r'.*', 'pydis_site.apps.home.urls', name=settings.DEFAULT_HOST)
)
