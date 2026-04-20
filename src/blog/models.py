import os
import uuid
from abc import abstractmethod
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from tinymce import models as tinymce_models


def article_image_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = f"{uuid.uuid4().hex}{ext.lower()}"
    return f"article_img/{filename}"


class ArticleStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    PUBLISHED = 'published', _('Published')
    REJECTED = 'rejected', _('Rejected')


class BaseModel(models.Model):
    """
    Base abstract model
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    def get_full_url(self):
        domain = Site.objects.get_current().domain
        url = "https://{domain}{path}".format(
            domain=domain,
            path=self.get_absolute_url()
        )
        return url

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(BaseModel):
    """
    Model for storing article data
    """
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=100,
        unique=True
    )
    body = tinymce_models.HTMLField()
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=ArticleStatus.choices,
        default=ArticleStatus.PENDING,
        db_index=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True
    )
    meta_title = models.CharField(
        max_length=160,
        blank=True,
        null=True
    )
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    og_title = models.CharField(
        max_length=160,
        blank=True,
        null=True
    )
    og_description = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    indexation = models.BooleanField(default=False)
    # image = models.ImageField(
    #     upload_to=article_image_upload_path,
    #     null=False,
    #     blank=False
    # )
    video_to_post = models.CharField(
        blank=True,
        null=True
    )

    class Meta:
        # verbose_name = "Blog"
        # verbose_name_plural = "Blog"
        verbose_name = _("Blog")
        verbose_name_plural = _("Blog")
        db_table_comment = "Blog table"
        get_latest_by = 'created_at'
        indexes = [
            models.Index(fields=['-created_at'], name='article_created_idx'),
            models.Index(fields=['status', '-created_at'], name='article_status_created_idx'),
        ]

    def get_absolute_url(self):
        return reverse(
            'blog:article_detail',
            kwargs={'slug': self.slug}
        )

    @property
    def image(self):
        return self.images.first()

    def __str__(self):
        return self.title


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse(
            'blog:category_detail',
            kwargs={'slug': self.slug}
        )

    def __str__(self):
        return self.name


class ArticleImage(models.Model):
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=article_image_upload_path)
    alt = models.CharField(
        max_length=255,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f"{self.article.title} - Image"
