from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.response import Response
from rest_framework.views import APIView

if TYPE_CHECKING:
    from rest_framework.request import Request

from core.business_logic.services import get_tweets
from core.presentation.api_v1.serializers import IndexSerializer


class IndexApiView(APIView):
    def get(self, request: Request) -> Response:
        user = request.user
        tweets = get_tweets(user=user)
        tweets_serializer = IndexSerializer(tweets, many=True)
        return Response(data=tweets_serializer.data)
