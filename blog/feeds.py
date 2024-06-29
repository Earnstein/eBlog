import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeeds(Feed):
    title = "Earnstein's Blog"
    link = reverse_lazy("blog:home")
    description = "New posts of my blog"

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item:Post):
        return item.title
    
    def item_description(self, item:Post):
        return truncatechars_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item:Post):
        return item.publish
    