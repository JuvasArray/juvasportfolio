from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404



from blog.forms import EmailPostForm, CommentForm
from blog.models import Post

from taggit.models import Tag
from django.db.models import Count

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context
    

    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'
    
    def get_object(self, queryset=None):
        post = self.kwargs.get('post')
        return get_object_or_404(Post, slug=post)
    
    def get_queryset(self):
        post = self.kwargs.get('post')
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['post'] = self.object
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        # context['similar_posts'] = get_object_or_404(Post, slug=self.kwargs.get('post_slug'))
        return context
    

def post_share(request, post_id, *args, **kwargs):
    post = get_object_or_404(Post, id=kwargs.get('post_id'), status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, form_email=None, recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

    
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return HttpResponseRedirect(reverse('blog:post_detail', args=[post.slug]))