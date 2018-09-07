from django.urls import include, path


urlpatterns = (
    path('', include('home.urls', namespace='home')),
)
