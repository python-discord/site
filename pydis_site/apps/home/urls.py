from django_distill import distill_path

from .views import HomeView

app_name = 'home'
urlpatterns = [
    distill_path('', HomeView.as_view(), name='home'),
]
