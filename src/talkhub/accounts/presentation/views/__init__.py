from .login import LoginView
from .logout import LogoutView
from .registration import ConfirmEmailView, RegistrationView
from .profile import ProfileView, ProfileEditView

__all__ = [
    "RegistrationView",
    "ConfirmEmailView",
    "LoginView",
    "LogoutView",
    "ProfileView",
    "ProfileEditView",
]
