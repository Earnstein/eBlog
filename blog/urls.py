from django.urls import path
from .feeds import LatestPostFeeds
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path('tag/<slug:tag_slug>/', views.home, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail_view, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostFeeds(), name="post_feed")
]
