from accounts.presentation.views import (
    ConfirmEmailView,
    LoginView,
    LogoutView,
    ProfileEditView,
    ProfileView,
    RegistrationView,
)
from django.urls import path

urlpatterns = [
    path("signin/", LoginView.as_view(), name="signin"),
    path("signup/", RegistrationView.as_view(), name="signup"),
    path("confirmation/", ConfirmEmailView.as_view(), name="confirm-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<uuid:profile_uuid>", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]
