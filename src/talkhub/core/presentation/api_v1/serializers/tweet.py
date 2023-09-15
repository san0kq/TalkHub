from accounts.presentation.api_v1.serializers import UserSerializer
from rest_framework import serializers


class IndexSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    user = UserSerializer()
    retweet_count = serializers.IntegerField()
    rating_count = serializers.IntegerField()
    reply_count = serializers.IntegerField()
    is_retweet = serializers.BooleanField()
    retweet_first_name = serializers.CharField()
    retweet_last_name = serializers.CharField()
    retweet_profile_pk = serializers.UUIDField()
    retweet_pk = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
