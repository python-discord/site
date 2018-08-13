from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    # > | Subdomain | URL Module   | Host entry name |
    #host(r"admin",    "admin",  name="admin"),
    #host(r"api",      "api",    name="api"),
    #host(r"staff",    "staff",  name="staff"),
    #host(r"wiki",     "wiki",   name="wiki"),
    #host(r"ws",       "ws",     name="ws"),
    host(r'.*',       'home.urls',   name=settings.DEFAULT_HOST)
)
