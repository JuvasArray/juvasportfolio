from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    feature_image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=Status, default='draft')
    
    objects = models.Manager()
    published = PublishedManager()
    
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.slug)])
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
