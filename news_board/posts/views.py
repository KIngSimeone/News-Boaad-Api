from api_utils.custom_pagination import CustomPagination
from api_utils.error_codes import ErrorCodes
from api_utils.views import http_response, validate_keys
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import CommentSerializer, PostSerializer
from .utils import (create_comment, create_post, delete_comment, delete_post,
                    get_all_posts, get_comment_by_id, get_post_by_id,
                    get_posts_comments, update_comment, update_post)


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

    def post(self, request, format=None):
        """Create a post"""

        payload = request.data
        # check if required fields is present
        missingKeys = validate_keys(payload=payload, requiredKeys=[
            'title', 'link', 'author_name',
        ])
        if missingKeys:
            return http_response(
                msg=f"The following key(s) are missing in the request payload: {missingKeys}",
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD,
            )

        title = payload['title']
        link = payload['link']
        author_name = payload['author_name']

        created_post, msg = create_post(title, link, author_name)
        if not created_post:
            return http_response(
                msg=msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.SERVER_ERROR
            )

        serializer = PostSerializer(created_post)

        return http_response(
            msg="Post Successfully Created",
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )

    def put(self, request, id, format=None):
        "Update a Post"

        payload = request.data
        # check if required fields is present
        missingKeys = validate_keys(payload=payload, requiredKeys=[
            'title', 'link', 'author_name',
        ])
        if missingKeys:
            return http_response(
                msg=f"The following key(s) are missing in the request payload: {missingKeys}",
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD,
            )

        post_to_update = get_post_by_id(id)
        if not post_to_update:
            return http_response(
                msg="Post not found",
                status=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        title = payload['title']
        link = payload['link']
        author_name = payload['author_name']

        updated_post, msg = update_post(
            post_to_update, title, link, author_name)
        if not updated_post:
            return http_response(
                msg=msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.SERVER_ERROR
            )

        serializer = PostSerializer(updated_post)
        return http_response(
            msg="Post Successfully Updated",
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def delete(self, request, id, format=None):
        "delete single post"

        post = get_post_by_id(id)
        if not post:
            return http_response(
                msg="Post not found",
                status=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        deleted_post, msg = delete_post(post)
        if not deleted_post:
            return http_response(
                msg=msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.SERVER_ERROR
            )

        return http_response(
            msg="Post Successfully Deleted",
            status=status.HTTP_200_OK,
            data={
                "status": True
            }
        )


class CommentsView(APIView):
    pagination_class = CustomPagination

    def get(self, request, format=None):
        """Retrieve Posts comments"""

        payload = request.data
        # check if required fields is present
        missingKeys = validate_keys(payload=payload, requiredKeys=[
            'post_id'
        ])
        if missingKeys:
            return http_response(
                msg=f"The following key(s) are missing in the request payload: {missingKeys}",
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD,
            )

        post_id = payload['post_id']
        post = get_post_by_id(post_id)
        if not post:
            return http_response(
                msg="Post not found",
                status=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        searchQuery = dict()
        queryDict = request.query_params
        filterQuery = queryDict.copy()
        if queryDict:
            if 'q' in filterQuery:
                searchQuery = filterQuery.get('q')
                del filterQuery['q']

        comments = get_posts_comments(post, searchQuery, filterQuery)
        serializer = CommentSerializer(comments, many=True)
        return http_response(
            msg="Comments Retrieved Successfully",
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def post(self, request, format=None):
        """Create a comment"""

        payload = request.data
        # check if required fields is present
        missingKeys = validate_keys(payload=payload, requiredKeys=[
            'post_id', 'content', 'author_name',
        ])
        if missingKeys:
            return http_response(
                msg=f"The following key(s) are missing in the request payload: {missingKeys}",
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD,
            )

        post_id = payload['post_id']
        content = payload['content']
        author_name = payload['author_name']

        post_id = payload['post_id']
        post = get_post_by_id(post_id)
        if not post:
            return http_response(
                msg="Post not found",
                status=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        created_comment, msg = create_comment(post, content, author_name)
        if not created_comment:
            return http_response(
                msg=msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.SERVER_ERROR
            )

        serializer = CommentSerializer(created_comment)

        return http_response(
            msg="Comment Successfully Created",
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )

    def put(self, request, id, format=None):
        "Update a Comment"

        payload = request.data
        # check if required fields is present
        missingKeys = validate_keys(payload=payload, requiredKeys=[
            'content', 'author_name',
        ])
        if missingKeys:
            return http_response(
                msg=f"The following key(s) are missing in the request payload: {missingKeys}",
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD,
            )

        commment_to_update = get_comment_by_id(id)
        if not commment_to_update:
            return http_response(
                msg="Comment not found",
                status=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        content = payload['content']
        author_name = payload['author_name']

        updated_comment, msg = update_comment(
            commment_to_update, content, author_name)
        if not updated_comment:
            return http_response(
                msg=msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.SERVER_ERROR
            )

        serializer = CommentSerializer(updated_comment)
        return http_response(
            msg="Commment Successfully Updated",
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def delete(self, request, id, format=None):
        "delete single comment"

        comment = get_comment_by_id(id)
        if not comment:
            return http_response(
                msg="Comment not found",
                status=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        deleted_comment, msg = delete_comment(comment)
        if not deleted_comment:
            return http_response(
                msg=msg,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.SERVER_ERROR
            )

        return http_response(
            msg="Comment Successfully Deleted",
            status=status.HTTP_200_OK,
            data={
                "status": True
            }
        )


@api_view(['POST'])
def upvote_post(request, id):
    post = get_post_by_id(id)
    if not post:
        return http_response(
            msg="Post not found",
            status=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCodes.NOT_FOUND,
        )

    post.upvotes = post.upvotes + 1
    post.save()

    serializer = PostSerializer(post)
    return http_response(
        msg="Post Successfully Upvoted",
        status=status.HTTP_200_OK,
        data=serializer.data
    )
