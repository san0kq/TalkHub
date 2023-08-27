from core.presentation.views import (
    CreateTweet,
    IndexView,
    RetweetView,
    TagsView,
    TrendingView,
    TweetLikeView,
    TweetReplyView,
    TweetView,
    UpdateConfig,
)
from django.urls import path

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("update_config/", UpdateConfig.as_view(), name="update_config"),
    path("create_tweet", CreateTweet.as_view(), name="create_tweet"),
    path("tweet/<uuid:tweet_uuid>", TweetView.as_view(), name="tweet"),
    path("tweet/like/<uuid:tweet_uuid>", TweetLikeView.as_view(), name="tweet_like"),
    path("tweet/reply/<uuid:parent_tweet_uuid>", TweetReplyView.as_view(), name="tweet_reply"),
    path("tweet/retweet/<uuid:tweet_uuid>", RetweetView.as_view(), name="retweet"),
    path("tags/", TagsView.as_view(), name="tags"),
    path("trending/", TrendingView.as_view(), name="trending"),
]
