from accounts.models import Country
from accounts.presentation.validators import ValidateFileExtension, ValidateFileSize, ValidateMaxAge, ValidateMinAge
from django import forms

COUNTRIES = [(country.name, country.name) for country in Country.objects.all()]


class ProfileEditForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    first_name = forms.CharField(label="First name", max_length=150)
    last_name = forms.CharField(label="Last name", max_length=150)
    email = forms.EmailField(label="Email", max_length=254)
    about = forms.CharField(label="About me", max_length=400, widget=forms.Textarea, required=False)
    country = forms.ChoiceField(label="Country", choices=COUNTRIES, required=False)
    avatar = forms.ImageField(
        label="Avatar",
        allow_empty_file=False,
        validators=[ValidateFileExtension(["jpg", "jpeg", "png"]), ValidateFileSize(5_000_000)],
        required=False,
    )
    date_of_birth = forms.DateField(
        label="Date of birth",
        widget=forms.DateInput(attrs={"type": "date"}),
        validators=[ValidateMinAge(min_age=18), ValidateMaxAge(max_age=140)],
        required=False,
    )
