from accounts.presentation.validators import ValidateMaxAge, ValidateMinAge
from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    username = forms.CharField(label="Username", max_length=150)
    date_of_birth = forms.DateField(
        label="Date of birth",
        widget=forms.DateInput(attrs={"type": "date"}),
        validators=[ValidateMinAge(min_age=18), ValidateMaxAge(max_age=140)],
    )
    password = forms.CharField(label="Password", max_length=128, widget=forms.PasswordInput)
