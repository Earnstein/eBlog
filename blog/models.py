from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Assuming User model is from django.contrib.auth

class PublisedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)

class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.DRAFT)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'Published'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)  # CharField for slug
    body = models.TextField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    object = models.Manager() # default manager
    published = PublisedManager() # custom manager
    drafted = DraftManager()

    class Meta:
        ordering = ['-publish']  # Order by publish field in descending order
        indexes = [
            models.Index(fields=['-publish']),  # Index for faster querying
        ]

    def __str__(self):
        return self.title