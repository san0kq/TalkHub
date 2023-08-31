from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import BigIntegerField, BooleanField, CharField, Count, F, UUIDField, Value

if TYPE_CHECKING:
    from core.business_logic.dto import (
        ProfileEditDTO,
        ProfileFollowDTO,
        SearchProfileDTO,
    )
    from uuid import UUID
    from django.contrib.auth.models import AbstractBaseUser

from accounts.models import Country, Profile
from core.business_logic.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from core.business_logic.services.common import change_file_size, replace_file_name_to_uuid
from core.business_logic.services.confirm_email import send_confirm_code
from core.models import Tweet

logger = getLogger(__name__)


def get_profile(profile_uuid: UUID) -> tuple[Profile, list[Tweet]]:
    """
    Fetching user profile information from the database.
    Retrieving a list of tweets and retweets by the user.

    Additional annotations are used to gather extra data for the HTML template.

    It returns a sorted combined array of all tweets and retweets.
    """
    profile = (
        Profile.objects.select_related("country", "user__config")
        .prefetch_related("user__tweets", "user__retweets")
        .annotate(followers_count=Count("follower", distinct=True))
        .annotate(followings_count=Count("followings", distinct=True))
        .get(pk=profile_uuid)
    )
    profile_tweets = (
        Tweet.objects.select_related("user", "parent_tweet")
        .prefetch_related("retweets", "ratings", "tweets")
        .annotate(
            rating_count=Count("rating", distinct=True),
            reply_count=Count("tweet", distinct=True),
            is_retweet=Value(False, BooleanField()),
            retweet_first_name=Value("", CharField()),
            retweet_last_name=Value("", CharField()),
            retweet_profile_pk=Value(0, UUIDField()),
            retweet_pk=Value(0, BigIntegerField()),
            sort_date=F("created_at"),
        )
        .filter(user=profile.user)
    )
    retweeted_tweets = (
        Tweet.objects.select_related("user", "parent_tweet")
        .prefetch_related("retweets", "ratings", "tweets")
        .annotate(
            rating_count=Count("rating", distinct=True),
            reply_count=Count("tweet", distinct=True),
            is_retweet=Value(True, BooleanField()),
            retweet_first_name=F("retweet__user__profile__first_name"),
            retweet_last_name=F("retweet__user__profile__last_name"),
            retweet_profile_pk=F("retweet__user__profile__pk"),
            retweet_pk=F("retweet__pk"),
            sort_date=F("retweet__created_at"),
        )
        .filter(retweet_profile_pk=profile.pk)
    )
    all_tweets = profile_tweets.union(retweeted_tweets, all=True).order_by("-sort_date")

    return profile, list(all_tweets)


def initial_profile_form(user_pk: int) -> dict[str, str]:
    """
    Function to populate a form with existing user data when editing user information.
    """
    user_model = get_user_model()
    user = user_model.objects.select_related("profile", "profile__country").get(pk=user_pk)
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
    """
    Function for editing data of an authenticated user.

    It checks whether any data has been changed and if so, it saves the changes to the database.
    """
    with transaction.atomic():
        user_model = get_user_model()

        if user_model.objects.exclude(pk=user_pk).filter(username=data.username).exists():
            raise UsernameAlreadyExistsError(f"User with this username ({data.username}) already exists.")
        if user_model.objects.exclude(pk=user_pk).filter(email=data.email).exists():
            raise EmailAlreadyExistsError(f"User with this email ({data.email}) already exists.")
        user: AbstractBaseUser = user_model.objects.get(pk=user_pk)
        profile: Profile = Profile.objects.get(user=user)
        country = Country.objects.get(name=data.country)
        logger_data = {}
        if user.username != data.username:
            logger_data["old_username"] = user.username
            logger_data["new_username"] = data.username
            user.username = data.username

        if user.email != data.email:
            send_confirm_code(user=user, email=data.email)

        if user.date_of_birth != data.date_of_birth:
            logger_data["old_date_of_birth"] = user.date_of_birth
            logger_data["new_date_of_birth"] = data.date_of_birth
            user.date_of_birth = data.date_of_birth

        if profile.first_name != data.first_name:
            logger_data["old_first_name"] = profile.first_name
            logger_data["new_first_name"] = data.first_name
            profile.first_name = data.first_name

        if profile.last_name != data.last_name:
            logger_data["old_last_name"] = profile.last_name
            logger_data["new_last_name"] = data.last_name
            profile.last_name = data.last_name

        if profile.avatar != data.avatar:
            if data.avatar:
                data.avatar = replace_file_name_to_uuid(file=data.avatar)
                data.avatar = change_file_size(file=data.avatar)
                profile.avatar = data.avatar
            elif data.avatar is False:
                profile.avatar = None

        if profile.about != data.about:
            logger_data["old_about"] = profile.about
            logger_data["new_about"] = data.about
            profile.about = data.about

        if profile.country != country:
            logger_data["old_country"] = profile.country.name
            logger_data["new_country"] = country.name
            profile.country = country

        user.save()
        profile.save()
        logger.info("Profile edited", extra={"data": logger_data})


def profile_follow(data: ProfileFollowDTO) -> None:
    """
    Function to subscribe to another user.
    """
    profile = Profile.objects.get(pk=data.user.profile.pk)
    profile_following = Profile.objects.get(pk=data.profile_uuid)
    profile.followings.add(profile_following)


def profile_unfollow(data: ProfileFollowDTO) -> None:
    """
    Function to unsubscribe from another user.
    """
    profile = Profile.objects.get(pk=data.user.profile.pk)
    profile_following = Profile.objects.get(pk=data.profile_uuid)
    profile.followings.remove(profile_following)


def profile_followings(profile_uuid: UUID) -> list[Profile | None]:
    """
    Fetching all users that another user is subscribed to.
    """
    followings = Profile.objects.prefetch_related("followings").get(pk=profile_uuid).followings.all()
    return list(followings)


def profile_followers(profile_uuid: UUID) -> list[Profile | None]:
    """
    Fetching all users who are subscribed to another user.
    """
    followers = Profile.objects.prefetch_related("followings").get(pk=profile_uuid).followers.all()
    return list(followers)


def search_profile(data: SearchProfileDTO) -> Optional[list[Profile]]:
    """
    Function for searching users.

    It returns a list of users if at least one field has been filled out.
    """
    if data.first_name or data.last_name or data.username:
        profiles = Profile.objects.select_related("user")
        if data.first_name:
            profiles = profiles.filter(first_name__icontains=data.first_name)
        if data.last_name:
            profiles = profiles.filter(last_name__icontains=data.last_name)
        if data.username:
            profiles = profiles.filter(user__username__icontains=data.username)
        return list(profiles)
    else:
        return None
