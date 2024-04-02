from .models import Post
from django.views.generic import ListView, DetailView, View
from .forms import EmailPostForm
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail

class HomeView(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-publish')
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'blog/details.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'post'
    date_field = 'publish'
    year_field = 'year'
    month_field = 'month'
    day_field = 'day'
class PostShareView(View):
    template_name = 'blog/share.html'
    form_class = EmailPostForm

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class()
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'bdamilola00@gmail.com', [cd['to']])
            sent = True
        context = {'post': post, 'form': form, 'sent': sent}
        return render(request, self.template_name, context)