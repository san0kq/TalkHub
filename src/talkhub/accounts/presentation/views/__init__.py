from .login import LoginView
from .logout import LogoutView
from .registration import RegistrationConfirmationView, RegistrationView
from .profile import ProfileView, ProfileEditView

__all__ = [
    "RegistrationView",
    "RegistrationConfirmationView",
    "LoginView",
    "LogoutView",
    "ProfileView",
    "ProfileEditView",
]
