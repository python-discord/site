from django.urls import include, path


urlpatterns = (
    path('', include('pydis_site.apps.home.urls', namespace='home')),
    path('staff/', include('pydis_site.apps.staff.urls', namespace='staff')),
)
