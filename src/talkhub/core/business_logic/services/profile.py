from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Optional

from django.db import transaction
from django.db.models import BooleanField, Count, Value

if TYPE_CHECKING:
    from core.business_logic.dto import ProfileEditDTO, ProfileFollowDTO, SearchProfileDTO
    from uuid import UUID

from accounts.models import Country, Profile, User
from core.business_logic.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from core.business_logic.services.common import change_file_size, replace_file_name_to_uuid
from core.business_logic.services.confirm_email import send_confirm_code
from core.models import Tweet

logger = getLogger(__name__)


def get_profile(profile_uuid: UUID) -> tuple[Profile, list[Tweet]]:
    profile = (
        Profile.objects.select_related("country", "user__config")
        .prefetch_related("user__tweets", "user__retweets")
        .annotate(followers_count=Count("follower", distinct=True))
        .annotate(followings_count=Count("followings", distinct=True))
        .get(pk=profile_uuid)
    )
    profile_tweets = Tweet.objects.annotate(
        rating_count=Count("rating", distinct=True),
        retweet_count=Count("retweet", distinct=True),
        reply_count=Count("tweet", distinct=True),
        is_retweet=Value(False, BooleanField()),
    ).filter(user=profile.user)
    retweeted_tweets = Tweet.objects.annotate(
        rating_count=Count("rating", distinct=True),
        retweet_count=Count("retweet", distinct=True),
        reply_count=Count("tweet", distinct=True),
        is_retweet=Value(True, BooleanField()),
    ).filter(retweet__user=profile.user)
    all_tweets = profile_tweets.union(retweeted_tweets, all=True).order_by("-created_at")

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
        if User.objects.exclude(pk=user_pk).filter(username=data.username).exists():
            raise UsernameAlreadyExistsError(f"User with this username ({data.username}) already exists.")
        if User.objects.exclude(pk=user_pk).filter(email=data.email).exists():
            raise EmailAlreadyExistsError(f"User with this email ({data.email}) already exists.")
        user: User = User.objects.get(pk=user_pk)
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
    profile = Profile.objects.get(pk=data.user.profile.pk)
    profile_following = Profile.objects.get(pk=data.profile_uuid)
    profile.followings.add(profile_following)


def profile_unfollow(data: ProfileFollowDTO) -> None:
    profile = Profile.objects.get(pk=data.user.profile.pk)
    profile_following = Profile.objects.get(pk=data.profile_uuid)
    profile.followings.remove(profile_following)


def profile_followings(profile_uuid: UUID) -> list[Profile | None]:
    followings = Profile.objects.prefetch_related("followings").get(pk=profile_uuid).followings.all()
    return list(followings)


def profile_followers(profile_uuid: UUID) -> list[Profile | None]:
    followers = Profile.objects.prefetch_related("followings").get(pk=profile_uuid).followers.all()
    return list(followers)


def search_profile(data: SearchProfileDTO) -> Optional[list[Profile]]:
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
