from django_distill import distill_path

from .views import HomeView, timeline

app_name = 'home'
urlpatterns = [
    distill_path('', HomeView.as_view(), name='home'),
    distill_path('timeline/', timeline, name="timeline"),
]
