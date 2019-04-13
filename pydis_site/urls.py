from django.urls import include, path


urlpatterns = (
    path('', include('pydis_site.apps.main.urls', namespace='home')),
)
