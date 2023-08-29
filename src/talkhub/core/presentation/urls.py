from core.presentation.views import (
    CreateTweet,
    DeleteTweetView,
    IndexView,
    NotificationView,
    RetweetView,
    TagsView,
    TrendingView,
    TweetLikeView,
    TweetReplyView,
    TweetView,
    UpdateConfig,
    UpdateTweetView,
)
from django.urls import path

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("update_config/", UpdateConfig.as_view(), name="update-config"),
    path("create_tweet", CreateTweet.as_view(), name="create-tweet"),
    path("tweet/<uuid:tweet_uuid>", TweetView.as_view(), name="tweet"),
    path("tweet/like/<uuid:tweet_uuid>", TweetLikeView.as_view(), name="tweet-like"),
    path("tweet/reply/<uuid:parent_tweet_uuid>", TweetReplyView.as_view(), name="tweet-reply"),
    path("tweet/retweet/<uuid:tweet_uuid>", RetweetView.as_view(), name="retweet"),
    path("tags/", TagsView.as_view(), name="tags"),
    path("trending/", TrendingView.as_view(), name="trending"),
    path("tweet/update/<uuid:tweet_uuid>", UpdateTweetView.as_view(), name="update-tweet"),
    path("tweet/delete/<uuid:tweet_uuid>", DeleteTweetView.as_view(), name="delete-tweet"),
    path("notification/", NotificationView.as_view(), name="notification"),
]
