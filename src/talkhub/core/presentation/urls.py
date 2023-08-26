from core.presentation.views import CreateTweet, IndexView, TweetView, UpdateConfig
from django.urls import path

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("update_config/", UpdateConfig.as_view(), name="update_config"),
    path("create_tweet", CreateTweet.as_view(), name="create_tweet"),
    path("tweet/<uuid:tweet_uuid>", TweetView.as_view(), name="tweet"),
]
