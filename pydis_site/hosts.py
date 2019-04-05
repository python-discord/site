from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    # > | Subdomain | URL Module   | Host entry name |
    host(r'admin', 'pydis_site.apps.admin.urls', name="admin"),
    host(r'api', 'pydis_site.apps.api.urls', name='api'),
    # host(r"staff",    "pydis_site.apps.staff",  name="staff"),
    # host(r"wiki",     "pydis_site.apps.wiki",   name="wiki"),
    # host(r"ws",       "pydis_site.apps. ws",     name="ws"),
    host(r'.*', 'pydis_site.apps.home.urls', name=settings.DEFAULT_HOST)
)
