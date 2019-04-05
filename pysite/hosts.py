from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    # > | Subdomain | URL Module   | Host entry name |
    host(r'admin', 'pysite.apps.admin.urls', name="admin"),
    host(r'api', 'pysite.apps.api.urls', name='api'),
    # host(r"staff",    "pysite.apps.staff",  name="staff"),
    # host(r"wiki",     "pysite.apps.wiki",   name="wiki"),
    # host(r"ws",       "pysite.apps. ws",     name="ws"),
    host(r'.*', 'pysite.apps.home.urls', name=settings.DEFAULT_HOST)
)
