from django.urls import path
from src.blog import views, feeds

app_name = "blog"

urlpatterns = [
    path(
        'feed/',
        feeds.LatestArticlesFeed(),
        name='feed'
    ),
    path(
        '',
        views.ArticleListView.as_view(),
        name='article_list'
    ),
    path(
        '<slug:slug>/',
        views.ArticleDetailView.as_view(),
        name='article_detail'
    ),
]
