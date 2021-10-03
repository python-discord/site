from django.urls import path
from django_distill import distill_path

from . import views

app_name = "content"
urlpatterns = [
    distill_path("", views.PageOrCategoryView.as_view(), name='pages'),
    path("<path:location>/", views.PageOrCategoryView.as_view(), name='page_category'),
]
