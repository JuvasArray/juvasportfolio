from django.urls import path
from blog import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:post>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment')
]
