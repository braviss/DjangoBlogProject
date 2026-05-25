from django.contrib.syndication.views import Feed
from django.urls import reverse
from src.blog.models import Article, ArticleStatus


class LatestArticlesFeed(Feed):
    title = "Blog"
    link = "/blog/"
    description = "Latest articles on my blog"

    def items(self):
        return (
            Article.objects
            .filter(status=ArticleStatus.PUBLISHED)
            .order_by('-created_at')[:10]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.meta_description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at