from .dao import FollowersDAO, LikeDAO, NotificationDAO, ReplyDAO, RetweetDAO, TweetDAO, UserDAO
from .factories import (
    FollowingsFactory,
    LikeFactory,
    NotificationFactory,
    ReplyFactory,
    RetweetFactory,
    TweetFactory,
    UserFactory,
)
from .populate_table_command import PopulateTable
from .providers import RandomValueFromListProvider
from .rand_gen import RandEmail, RandFirstName, RandGen, RandLastName, RandText, RandWord


def run_populate_db(records_number: int) -> None:
    user_dao = UserDAO()
    user_factory = UserFactory(
        username_provider=RandGen(RandWord),
        email_profiver=RandGen(RandEmail),
        password_provider=RandGen(RandWord),
        first_name_provider=RandGen(RandFirstName),
        last_name_profivder=RandGen(RandLastName),
        about_provider=RandGen(RandText),
    )
    PopulateTable(records_number=records_number, dao=user_dao, fake_factory=user_factory).execute()

    profiles = user_dao.get_profile_ids_list()
    following_dao = FollowersDAO()
    followings_factory = FollowingsFactory(
        profile_id_provider=RandomValueFromListProvider(values=profiles),
    )
    PopulateTable(records_number=records_number * 2, dao=following_dao, fake_factory=followings_factory).execute()

    users = user_dao.get_user_ids_list()
    tweet_dao = TweetDAO()
    tweet_factory = TweetFactory(
        user_id_provider=RandomValueFromListProvider(values=users),
        text_provider=RandGen(RandText),
        tag_provider=RandGen(RandWord),
    )
    PopulateTable(records_number=records_number * 2, dao=tweet_dao, fake_factory=tweet_factory).execute()

    tweets = tweet_dao.get_tweet_ids_list()
    retweet_dao = RetweetDAO()
    retweet_factory = RetweetFactory(
        user_id_provider=RandomValueFromListProvider(values=users),
        tweet_id_provider=RandomValueFromListProvider(values=tweets),
    )
    PopulateTable(records_number=records_number, dao=retweet_dao, fake_factory=retweet_factory).execute()

    reply_dao = ReplyDAO()
    reply_factory = ReplyFactory(
        user_id_provider=RandomValueFromListProvider(values=users),
        tweet_id_provider=RandomValueFromListProvider(values=tweets),
        text_provider=RandGen(RandText),
        tag_provider=RandGen(RandWord),
    )
    PopulateTable(records_number=records_number * 2, dao=reply_dao, fake_factory=reply_factory).execute()

    like_dao = LikeDAO()
    like_factory = LikeFactory(
        user_id_provider=RandomValueFromListProvider(values=users),
        tweet_id_provider=RandomValueFromListProvider(values=tweets),
    )
    PopulateTable(records_number=records_number * 10, dao=like_dao, fake_factory=like_factory).execute()

    notification_dao = NotificationDAO()
    notification_factory = NotificationFactory(
        user_id_provider=RandomValueFromListProvider(values=users), text_provider=RandGen(RandText)
    )
    PopulateTable(records_number=records_number * 2, dao=notification_dao, fake_factory=notification_factory).execute()
