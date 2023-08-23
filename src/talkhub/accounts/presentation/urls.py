from accounts.presentation.views import (
    LoginView,
    LogoutView,
    ProfileEditView,
    ProfileView,
    RegistrationConfirmationView,
    RegistrationView,
)
from django.urls import path

urlpatterns = [
    path("signin/", LoginView.as_view(), name="signin"),
    path("signup/", RegistrationView.as_view(), name="signup"),
    path("confirmation/", RegistrationConfirmationView.as_view(), name="confirm-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit", ProfileEditView.as_view(), name="profile_edit"),
]
