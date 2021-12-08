from django.urls import path
from .views import PostsView


urlpatterns = [
    path('', PostsView.as_view()),
    path('<int:id>/', PostsView.as_view()),
]