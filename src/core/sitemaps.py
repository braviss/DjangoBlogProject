from django.contrib.sitemaps import Sitemap
from src.blog.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'
    i18n = True
    languages = ['uk', 'ru', 'en']

    def items(self):
        return Article.objects.filter(status='pu', indexation=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
