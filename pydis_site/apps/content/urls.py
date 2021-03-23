from django.urls import path

from . import views

app_name = "content"
urlpatterns = [
    path("", views.PageOrCategoryView.as_view(), name='pages'),
    path("<path:location>/", views.PageOrCategoryView.as_view(), name='page_category'),
]
