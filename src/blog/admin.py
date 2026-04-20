from django.contrib import admin
from src.blog.models import Article, Category, Tag, ArticleImage, ArticleStatus
from django.utils import timezone
from modeltranslation.admin import TranslationAdmin

from django.template.response import TemplateResponse
from django.urls import path


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status=ArticleStatus.PUBLISHED)


@admin.action(description="Raise article")
def raise_article(modeladmin, request, queryset):
    queryset.update(created_at=timezone.now())


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ["title", "created_at", "slug", "status"]
    inlines = [ArticleImageInline]
    # list_filter = ('status', 'created_at')
    ordering = ["-created_at"]
    exclude = ["last_modify_time"]
    actions = [make_published, raise_article]
    list_editable = ('status',)
    list_display_links = ["title"]
    readonly_fields = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (
            None,
            {
                "fields": ["title", "slug", "body"],
            },
        ),
        (
            "Seo options",
            {
                "classes": ["wide"],
                # "fields": ["meta_title", "meta_description", "og_title", "og_description"],
                "fields": (
                    ("meta_title", "og_title"),
                    ("meta_description", "og_description"),
                ),
            },
        ),
        (
            "Settings",
            {
                "fields": ["category", "status", "tags", "indexation", "video_to_post"],
            },
        ),
    ]
    search_fields = ['title', 'slug', 'status']
    filter_horizontal = ('tags', )
    view_on_site = True
    save_on_top = True

    # Custom admin page
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("my_view/", self.admin_site.admin_view(self.my_view))]
        return my_urls + urls

    def my_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            key="value",
        )
        return TemplateResponse(request, "sometemplate.html", context)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {'slug': ('name',)}
    fields = (
        'name',
        'slug'
    )


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ["article", "alt", "created_at"]
