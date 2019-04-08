from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    # host(r"subdomain pattern", "URLs module", "host entry name"),
    host(r'admin', 'pydis_site.apps.admin.urls', name="admin"),
    host(r'api', 'pydis_site.apps.api.urls', name='api'),
    host(r'.*', 'pydis_site.apps.home.urls', name=settings.DEFAULT_HOST)
)
