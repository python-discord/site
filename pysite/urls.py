from django.urls import include, path


urlpatterns = (
    path('', include('pysite.apps.home.urls', namespace='home')),
)
