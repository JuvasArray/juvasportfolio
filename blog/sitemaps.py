from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog:post_detail', args=[obj.slug])
    
