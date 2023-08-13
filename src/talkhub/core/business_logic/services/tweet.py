from core.models import Tweet


def get_tweets() -> list[Tweet]:
    tweets = Tweet.objects.select_related("user__profile", "parent_tweet").all()
    return list(tweets)
