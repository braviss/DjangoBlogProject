from src.blog.models import Article
from django.views.generic import (
    ListView,
    DetailView
)
from view_breadcrumbs import (
    ListBreadcrumbMixin,
    DetailBreadcrumbMixin,
)
from django.utils.translation import gettext_lazy as _
from src.blog.models import ArticleStatus


class ArticleListView(ListBreadcrumbMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    ordering = '-created_at'
    paginate_by = 10
    breadcrumb_label = _("Blog")

    def get_queryset(self):
        return Article.objects.filter(status=ArticleStatus.PUBLISHED)


class ArticleDetailView(DetailBreadcrumbMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    slug_field = "slug"
    slug_url_kwarg = "slug"
    breadcrumb_use_pk = False
    breadcrumb_label = 'title'

    def get_related_posts(self):
        """
        Related post
        """
        return (
            Article.objects
            .filter(tags__in=self.object.tags.all())
            .exclude(id=self.object.id)
            .distinct()
            .order_by('-created_at')[:3]
        )

    def get_queryset(self):
        return Article.objects.filter(status=ArticleStatus.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = self.get_related_posts()
        return context
