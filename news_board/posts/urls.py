from django.urls import path

from .views import CommentsView, PostsView, upvote_post

urlpatterns = [
    path('', PostsView.as_view()),
    path('/<int:id>', PostsView.as_view()),
    path('/comments/<int:id>', CommentsView.as_view()),
    path('/comments', CommentsView.as_view()),
    path('/upvote/<int:id>', upvote_post)
]
