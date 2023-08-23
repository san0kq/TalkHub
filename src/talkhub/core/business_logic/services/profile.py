from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import BooleanField, Count, Value

if TYPE_CHECKING:
    from core.business_logic.dto import ProfileEditDTO

from accounts.models import Country, Profile, User
from core.business_logic.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from core.models import Tweet


def get_profile(user: User) -> tuple[Profile, list[Tweet]]:
    profile = (
        User.objects.select_related("profile", "profile__country", "config")
        .prefetch_related("tweets", "retweets__tweet")
        .get(pk=user.pk)
    )
    profile_tweets = profile.tweets.annotate(
        rating_count=Count("rating"),
        retweet_count=Count("retweet"),
        reply_count=Count("tweet"),
        is_retweet=Value(False, BooleanField()),
    ).all()
    retweeted_tweets = Tweet.objects.filter(retweet__user=user).annotate(
        rating_count=Count("tweet__rating"),
        retweet_count=Count("tweet__retweet"),
        reply_count=Count("tweet__tweet"),
        is_retweet=Value(True, BooleanField()),
    )
    all_tweets = profile_tweets.union(retweeted_tweets).order_by(profile.configs.tweets_order)
    return profile, list(all_tweets)


def initial_profile_form(user_pk: int) -> dict[str, str]:
    user = User.objects.select_related("profile", "profile__country").get(pk=user_pk)
    initial_data = {
        "username": user.username,
        "first_name": user.profile.first_name,
        "last_name": user.profile.last_name,
        "email": user.email,
        "about": user.profile.about,
        "country": user.profile.country,
        "avatar": user.profile.avatar,
        "date_of_birth": user.date_of_birth,
    }
    return initial_data


def profile_edit(data: ProfileEditDTO, user_pk: int) -> None:
    with transaction.atomic():
        if User.objects.exclude(pk=user_pk).filter(username__icontains=data.username).exists():
            raise UsernameAlreadyExistsError(f"User with this username ({data.username}) already exists.")
        if User.objects.exclude(pk=user_pk).filter(email__icontains=data.email).exists():
            raise EmailAlreadyExistsError(f"User with this email ({data.email}) already exists.")
        user: User = User.objects.get(pk=user_pk)
        profile: Profile = Profile.objects.get(user=user)
        country = Country.objects.get(name=data.country)
        user.username = data.username
        user.email = data.email
        user.date_of_birth = data.date_of_birth
        profile.first_name = data.first_name
        profile.last_name = data.last_name
        profile.avatar = data.avatar
        profile.about = data.about
        profile.country = country
        user.save()
        profile.save()
