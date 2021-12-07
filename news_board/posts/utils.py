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
                Q(full_name__icontains=search) |
                Q(email_address__iexact=search) |
                Q(phone_number__iexact=search)
            )

        return allPosts

    except Exception as e:
        logger.error('get_all_posts@Error')
        logger.error(e)
        return []