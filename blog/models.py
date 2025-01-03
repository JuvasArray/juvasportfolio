from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=Status, default='draft')
    
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title
