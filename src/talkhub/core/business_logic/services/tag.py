from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.business_logic.dto import SearchTagDTO, TrendingDTO

from core.models import Tag, Tweet
from django.db.models import Count
from django.utils import timezone


def find_tags(data: SearchTagDTO) -> list[Tweet]:
    """
    Function that returns a list of tweets where a specific hashtag has been found.
    """
    tweets = (
        Tweet.objects.select_related("user", "parent_tweet")
        .prefetch_related("tags")
        .annotate(
            rating_count=Count("rating", distinct=True),
            reply_count=Count("tweet", distinct=True),
        )
        .filter(tags__name=data.name.lower())
        .order_by("-created_at")
    )
    return list(tweets)


def get_trending_tags(data: TrendingDTO) -> Optional[Tag]:
    """
    Function that returns a list of the top 10 most popular
    hashtags used in the new tweets of users from the same country
    as specified in the information of the authenticated user.

    If the user hasn't specified a country, the function returns None.
    """
    if not data.user.profile.country:
        return None

    day_start = timezone.now() - timedelta(days=1)

    tags: Tag = (
        Tag.objects.filter(
            tweet__created_at__gte=day_start,
            tweet__user__profile__country__name=data.user.profile.country.name,
        )
        .annotate(count=Count("tweet"))
        .order_by("-count")[:10]
    )

    return tags
