from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', views.PostShareView.as_view(), name='post_share'),
]
