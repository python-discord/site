from django.urls import path

from . import views

app_name = "guides"
urlpatterns = [
    path("", views.GuidesView.as_view(), name='guides'),
    path("category/<str:category>/", views.CategoryView.as_view(), name='category'),
    path("category/<str:category>/<str:guide>/", views.GuideView.as_view(), name='category_guide'),
    path("<str:guide>/", views.GuideView.as_view(), name='guide')
]
