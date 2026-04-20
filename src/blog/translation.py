from modeltranslation.translator import (
    TranslationOptions,
    translator,
)
from src.blog.models import Article, Category


class ArticleTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'body',
        'meta_title',
        'meta_description',
        'og_title',
        'og_description'
    )


class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


translator.register(Article, ArticleTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
