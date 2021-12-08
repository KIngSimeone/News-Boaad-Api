from django.db import models
from rest_framework import fields, serializers
from .models import Posts, Comments
import logging
logger = logging.getLogger(__name__)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = [
            'id', 'title', 'link', 'author_name', 
            'upvotes', 'created_date'
        ]
        read_only_fields = ['id', 'created_date']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id','post', 'author_name', 'created_date'
        ]
        read_only_fields = ['id', 'created_date']