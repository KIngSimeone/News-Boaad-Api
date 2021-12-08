from celery import shared_task
from celery.utils.log import get_task_logger
from .utils import get_all_posts


logger = get_task_logger(__name__)


@shared_task
def upvote_defaulter():
    posts = get_all_posts()
    for post in posts:
        post.upvotes = 0
        post.save()
    return "success"