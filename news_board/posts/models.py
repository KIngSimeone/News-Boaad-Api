from django.db import models
from django.utils.timezone import now

class Posts(models.Model):
    title = models.TextField(null=True)
    link = models.TextField(null=True)
    author_name = models.TextField(null=True)
    upvotes = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True)
    author_name = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    