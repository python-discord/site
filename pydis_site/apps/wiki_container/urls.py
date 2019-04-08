from django.urls import path, include

urlpatterns = [
    path('notifications/', include('django_nyt.urls')),
    path('', include('wiki.urls'))
]
