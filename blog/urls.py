from django.urls import path
from blog import views
from blog.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from blog.feeds import LatestPostsFeed


sitemaps = {
    'posts': PostSitemap,
}

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:post>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list'),
    path('sitemap.xml', sitemap, {'sitemap': sitemaps}, name= 'django.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
