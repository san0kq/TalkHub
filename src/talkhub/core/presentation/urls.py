from core.presentation.views import IndexView, UpdateConfig
from django.urls import path

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("update_config/", UpdateConfig.as_view(), name="update_config"),
]
