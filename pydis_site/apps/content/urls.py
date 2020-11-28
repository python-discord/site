from django.urls import path

from . import views

app_name = "content"
urlpatterns = [
    path("", views.ArticlesView.as_view(), name='articles'),
    path("<path:location>/", views.ArticleOrCategoryView.as_view(), name='article_category'),
]
