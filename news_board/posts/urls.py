from django.urls import path
from .views import PostsView, CommentsView


urlpatterns = [
    path('', PostsView.as_view()),
    path('/<int:id>', PostsView.as_view()),
    path('/<int:postId>', CommentsView.as_view()),
]