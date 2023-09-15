from core.presentation.api_v1.views import IndexApiView
from django.urls import path

urlpatterns = [path("", IndexApiView.as_view(), name="index-api")]
