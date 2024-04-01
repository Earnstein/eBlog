from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path('<int:id>/', views.post_detail_view, name='post_detail'),
]