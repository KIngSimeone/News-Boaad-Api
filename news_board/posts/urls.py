from django.urls import path

from .views import CommentsView, PostsView

urlpatterns = [
    path('', PostsView.as_view()),
    path('/<int:id>', PostsView.as_view()),
    path('/comments/<int:id>', CommentsView.as_view()),
    path('/comments', CommentsView.as_view()),
]
