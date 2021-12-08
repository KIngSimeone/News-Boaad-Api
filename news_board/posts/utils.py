import logging
import uuid
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone

from .models import Comments, Posts

logger = logging.getLogger(__name__)


def get_all_posts(search=None, filter=None):
    try:
        queryset = dict()
        if filter is not None:
            for key, value in filter.items():
                if key in Posts.__dict__.keys():
                    queryset[key] = value

        allPosts = Posts.objects.all()

        if len(queryset) > 0:
            # filter allposts by queryset
            allPosts = allPosts.filter(**queryset)

        if search:
            # search allposts
            allPosts = allPosts.filter(
                Q(title__icontains=search) |
                Q(author_name__icontains=search) |
                Q(id__iexact=search)
            )

        return allPosts

    except Exception as e:
        logger.error('get_all_posts@Error')
        logger.error(e)
        return []


def get_post_by_id(id):
    try:
        post = Posts.objects.get(id=id)
        return post

    except ObjectDoesNotExist as e:
        logger.error('get_post_by_id@Error')
        logger.error(e)
        return None


def create_post(title, link, author_name):
    try:
        post = Posts.objects.create(
            title=title,
            link=link,
            author_name=author_name
        )
        return post, "success"

    except Exception as e:
        logger.error('create_post@error')
        logger.error(e)
        return None, str(e)


def update_post(post, title, link, author_name):
    try:
        post.title = title
        post.link = link
        post.author_name = author_name
        post.save()

        return post, "success"
    except Exception as e:
        logger.error('update_post@error')
        logger.error(e)
        return None, str(e)


def delete_post(post):
    try:
        post.delete()
        return True, "success"

    except Exception as e:
        logger.error('delete_post@Error')
        logger.error(e)
        return False, str(e)


########
def get_posts_comments(post, search=None, filter=None):
    try:
        queryset = dict()
        if filter is not None:
            for key, value in filter.items():
                if key in Posts.__dict__.keys():
                    queryset[key] = value

        allComments = Comments.objects.filter(post=post)

        if len(queryset) > 0:
            # filter allComments by queryset
            allComments = allComments.filter(**queryset)

        if search:
            # search allComments
            allComments = allComments.filter(
                Q(author_name__icontains=search) |
                Q(post__id__iexact=search) |
                Q(id__iexact=search) 
            )

        return allComments

    except Exception as e:
        logger.error('get_all_comments@Error')
        logger.error(e)
        return []


def get_comment_by_id(id):
    try:
        comment = Comments.objects.get(id=id)
        return comment

    except ObjectDoesNotExist as e:
        logger.error('get_comment_by_id@Error')
        logger.error(e)
        return None


def create_comment(post, content, author_name):
    try:
        comment = Comments.objects.create(
            post=post,
            content=content,
            author_name=author_name
        )
        return comment, "success"

    except Exception as e:
        logger.error('create_comment@error')
        logger.error(e)
        return None, str(e)


def update_comment(comment, content, author_name):
    try:
        comment.content = content
        comment.author_name = author_name
        comment.save()

        return comment, "success"
    except Exception as e:
        logger.error('update_comment@error')
        logger.error(e)
        return None, str(e)


def delete_comment(comment):
    try:
        comment.delete()
        return True, "success"

    except Exception as e:
        logger.error('delete_comment@Error')
        logger.error(e)
        return False. str(e)
