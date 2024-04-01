from django.http import Http404
from .models import Post
from django.shortcuts import render, get_object_or_404


def home(request):
    return render(request, 'home.html')

def post_list_view(request):
    posts = Post.objects.all()
    published_posts = Post.published.all()
    draft_posts = Post.drafted.all()
    context = {
        'posts': posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts
    }
    return render(request, 'blog/posts.html', context)


def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    context = {'post': post}
    return render(request, 'blog/details.html', context)

