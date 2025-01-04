from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
import markdown
from django.template.defaultfilters import truncatechars_html
from blog.models import Post


class LatestPostsFeed(Feed):
    title = "Latest Posts"
    link = reverse_lazy('blog:post_list')
    description = "Updates on the latest posts."

    def items(self):
        return Post.published.all[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars_html(markdown.markdown(item.content), 30)

    def item_publish(self, item):
        return item.publish
