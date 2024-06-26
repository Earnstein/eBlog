from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag


def home(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {'posts': posts, 'tag': tag}
    return render(request, 'home.html', context)


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    commments = post.comments.filter(active=True)
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    print(post_tags_ids)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {
        "comments": commments,
        "form": form,
        "post": post,
        "similar_posts": similar_posts
    }
    return render(request, 'blog/details.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'bdamilola00@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {"post": post, "form": form, "sent": sent}
    return render(request, "blog/share.html", context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {"post": post, "comment": comment}
    return render(request, "blog/comment.html", context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_query=SearchQuery(query, config='spanish')
            search_vector=SearchVector('title', config='spanish', weight='A') + SearchVector('body', config='spanish', weight='B')
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
                ).filter(rank__gte=0.3).order_by('-rank')
    context = {"form": form, "query": query, "results": results}
    return render(request, "blog/search.html", context)