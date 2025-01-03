from django.shortcuts import render
from django.views.generic import ListView,DetailView

from blog.models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3

    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'
    
    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Post, id=id)
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['post'] = self.object
        return context
