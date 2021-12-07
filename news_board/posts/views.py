from api_utils.custom_pagination import CustomPagination
from api_utils.error_codes import ErrorCodes
from api_utils.views import http_response, validate_keys
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView

from .serializers import CommentSerializer, PostSerializer
from .utils import (create_post, delete_post, get_all_posts, get_post_by_id,
                    update_post)


class PostsView(APIView):
    pagination_class = CustomPagination

    def get(self, request, format=None):
        """Retrieve all posts"""

        searchQuery = dict()
        queryDict = request.query_params
        filterQuery = queryDict.copy()
        if queryDict:
            if 'q' in filterQuery:
                searchQuery = filterQuery.get('q')
                del filterQuery['q']
        
        posts = get_all_posts(searchQuery, filterQuery)
        serializer = PostSerializer(posts, many=True)
        return http_response(
            msg="Posts Retrieved Successfully",
            status=status.HTTP_200_OK,
            data=serializer.data
        )
        
