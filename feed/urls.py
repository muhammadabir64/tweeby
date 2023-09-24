from django.urls import path
from .views import feed, tweet_publish, tweet_remover, likes_handler, tweet_comment_publish


urlpatterns = [
    path("", feed, name="feed"),
    path("tweet_publish/", tweet_publish, name="tweet_publish"),
    path("tweet_remover/<str:tweet>/<str:uri>/", tweet_remover, name="tweet_remover"),
    path("likes_handler/", likes_handler, name="likes_handler"),
    path("tweet_comment_publish/", tweet_comment_publish, name="tweet_comment_publish"),
]