from accounts.presentation.views import (
    ConfirmEmailView,
    FollowProfileView,
    LoginView,
    LogoutView,
    ProfileEditView,
    ProfileFollowersView,
    ProfileFollowingsView,
    ProfileView,
    RegistrationView,
    SearchProfileView,
    UnfollowProfileView,
)
from django.urls import path

urlpatterns = [
    path("signin/", LoginView.as_view(), name="signin"),
    path("signup/", RegistrationView.as_view(), name="signup"),
    path("confirmation/", ConfirmEmailView.as_view(), name="confirm-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<uuid:profile_uuid>/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/follow/<uuid:profile_uuid>/", FollowProfileView.as_view(), name="profile_follow"),
    path("profile/unfollow/<uuid:profile_uuid>/", UnfollowProfileView.as_view(), name="profile_unfollow"),
    path("profile/followings/<uuid:profile_uuid>/", ProfileFollowingsView.as_view(), name="profile_followings"),
    path("profile/followers/<uuid:profile_uuid>/", ProfileFollowersView.as_view(), name="profile_followers"),
    path("search/", SearchProfileView.as_view(), name="search_profile"),
]
