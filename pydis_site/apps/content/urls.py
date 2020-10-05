from django.urls import path

from . import views

app_name = "content"
urlpatterns = [
    path("", views.ArticlesView.as_view(), name='content'),
    path("category/<str:category>/", views.CategoryView.as_view(), name='category'),
    path(
        "category/<str:category>/<str:article>/",
        views.ArticleView.as_view(),
        name='category_article'
    ),
    path("<str:article>/", views.ArticleView.as_view(), name='article')
]
