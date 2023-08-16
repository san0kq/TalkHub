from accounts.presentation.views import LoginView, LogoutView, RegistrationConfirmationView, RegistrationView
from django.urls import path

urlpatterns = [
    path("signin/", LoginView.as_view(), name="signin"),
    path("signup/", RegistrationView.as_view(), name="signup"),
    path("confirmation/", RegistrationConfirmationView.as_view(), name="confirm-signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
